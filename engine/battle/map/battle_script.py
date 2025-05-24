"""
Battle script module for defining map assembly logic.
"""
from typing import List, Optional, Any, Dict
from engine.battle.map.battle_script_step import TBattleScriptStep
from battle.terrain.map_block import TMapBlock

class TBattleScript:
    """
    Represents a script for map block placement.
    Used to generate a battle map from map blocks in a specific way (by group, size, etc).
    Each script consists of steps, each step describes how to fill part of the map grid.
    """
    def __init__(self, pid: Any, data: dict):

        from engine.engine.game import TGame  # Avoid circular import
        self.game = TGame()

        self.pid: Any = pid
        self.steps: List[TBattleScriptStep] = []

        if 'steps' in data and isinstance(data['steps'], list):
            for step_data in data['steps']:
                self.steps.append(TBattleScriptStep(step_data))

    def apply_to(self, generator ) -> None:
        """
        Apply the script to the generator, filling the block grid according to the steps.
        """
        import random
        block_counts = {}

        for step in self.steps:

            # Check chance (probability of applying this step)
            chance = step.chance
            if random.random() > chance:
                continue

            # Filter blocks based on step properties
            group = step.group
            size = step.size
            name = None

            if step.type == 'add_ufo':
                name = 'small_scout' # step.ufo TODO fix me
            elif step.type == 'add_craft':
                name = 'interceptor' # step.craft TODO fix me

            filtered_blocks = self.filter_blocks(generator, group, size, name)

            # Skip if no valid blocks and not filling
            if not filtered_blocks and step.type != 'fill_block':
                continue

            # Process step based on type
            if step.type == 'add_line':
                self.process_add_line(generator, step, filtered_blocks)
            elif step.type == 'add_block':
                self.process_add_block(generator, step, filtered_blocks, block_counts)
            elif step.type == 'fill_block':
                self.process_fill_block(generator, step, filtered_blocks)
            elif step.type == 'add_ufo':
                self.process_add_special(generator, step, filtered_blocks, 'ufo')
            elif step.type == 'add_craft':
                self.process_add_special(generator, step, filtered_blocks, 'craft')

    def filter_blocks(self, generator, group: Any = None, size: Any = None, name: str = None) -> list:
        """
        Filter available map block entries by group, size, and/or name.
        """
        blocks = generator.terrain.map_blocks_entries.copy()  # Start with all available blocks

        if group is not None:
            blocks = [b for b in blocks if b.group == group]
        if size is not None:
            blocks = [b for b in blocks if b.size == size]
        if name is not None:
            blocks = [b for b in blocks if b.map == name]

        return blocks

    def process_add_line(self, generator, step: TBattleScriptStep, blocks: list) -> None:
        """
        Add blocks in a line according to direction (horizontal, vertical, or both).
        """
        import random
        direction = step.direction
        runs = step.runs
        row = getattr(step, 'row', None)
        col = getattr(step, 'col', None)

        for _ in range(runs):
            if direction == 'horizontal' or direction == 'both':
                # Select row: use step.row if set, else random
                y = row if row is not None else random.randint(0, generator.map_height - 1)

                # Place blocks along the row
                for x in range(generator.map_width):
                    if generator.block_grid[y][x] is None and blocks:
                        block_entry = random.choice(blocks)
                        generator.block_grid[y][x] = block_entry.map

            if direction == 'vertical' or direction == 'both':
                # Select column: use step.col if set, else random
                x = col if col is not None else random.randint(0, generator.map_width - 1)

                # Place blocks along the column
                for y in range(generator.map_height):
                    if generator.block_grid[y][x] is None and blocks:
                        block_entry = random.choice(blocks)
                        generator.block_grid[y][x] = block_entry.map

    def process_add_block(self, generator, step: TBattleScriptStep, blocks: list, block_counts: Dict) -> None:
        """
        Add a random block to the first available position.
        Take into account max count if specified.
        Handles large blocks by only assigning the top-left cell, and marking the rest with '-'.
        """
        import random

        max_count = step.runs if hasattr(step, 'runs') else 1
        group_key = f"block_{step.group}_{step.size}"

        current_count = block_counts.get(group_key, 0)
        runs = min(max_count, generator.map_width * generator.map_height - current_count)

        placed = 0
        for _ in range(runs):
            if blocks:
                block_entry = random.choice(blocks)

                width = block_entry.size
                height = block_entry.size
                found = False

                for y in range(generator.map_height - height + 1):
                    for x in range(generator.map_width - width + 1):
                        # Check if all cells are empty
                        can_place = True
                        for dy in range(height):
                            for dx in range(width):
                                if generator.block_grid[y+dy][x+dx] is not None:
                                    can_place = False
                                    break
                            if not can_place:
                                break
                        if can_place:
                            # Place block only at top-left, mark others with '-'
                            generator.block_grid[y][x] = block_entry.map
                            for dy in range(height):
                                for dx in range(width):
                                    if dy != 0 or dx != 0:
                                        generator.block_grid[y+dy][x+dx] = '-'
                            placed += 1
                            found = True
                            break
                    if found:
                        break
            block_counts[group_key] = block_counts.get(group_key, 0) + 1
            current_count = block_counts[group_key]
            if current_count >= max_count:
                break

    def process_fill_block(self, generator, step: TBattleScriptStep, blocks: list) -> None:
        """
        Fill all remaining empty positions with random blocks.
        Handles large blocks by only assigning the top-left cell, and marking the rest with '-'.
        """
        import random
        if not blocks:
            blocks = generator.terrain.map_blocks_entries
        if not blocks:
            return
        for y in range(generator.map_height):
            for x in range(generator.map_width):
                if generator.block_grid[y][x] is None:
                    for _ in range(len(blocks)):
                        block_entry = random.choice(blocks)

                        width = block_entry.size
                        height = block_entry.size

                        # Check if block fits
                        if y + height <= generator.map_height and x + width <= generator.map_width:
                            can_place = True
                            for dy in range(height):
                                for dx in range(width):
                                    if generator.block_grid[y+dy][x+dx] is not None:
                                        can_place = False
                                        break
                                if not can_place:
                                    break
                            if can_place:
                                generator.block_grid[y][x] = block_entry.map
                                for dy in range(height):
                                    for dx in range(width):
                                        if dy != 0 or dx != 0:
                                            generator.block_grid[y+dy][x+dx] = '-'
                                break


    def process_add_special(self, generator, step: TBattleScriptStep, blocks: list, special_type: str) -> None:
        """
        Add a special block (UFO or craft) to the first available position.

        Args:
            generator: The battle map generator
            step: The script step to process
            blocks: The filtered blocks to choose from
            special_type: Type of special block ('ufo' or 'craft')
        """
        import random

        if blocks:
            block_entry = random.choice(blocks)

            # Try to place in the center first, then anywhere available
            center_y = generator.map_height // 2
            center_x = generator.map_width // 2

            # Check center and surrounding area first
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    y = center_y + dy
                    x = center_x + dx
                    if (0 <= y < generator.map_height and
                        0 <= x < generator.map_width and
                        generator.block_grid[y][x] is None):
                        generator.block_grid[y][x] = block_entry.map
                        return

            # If center area is full, try anywhere
            for y in range(generator.map_height):
                for x in range(generator.map_width):
                    if generator.block_grid[y][x] is None:
                        generator.block_grid[y][x] = block_entry.map
                        return
