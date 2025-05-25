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
        self.context: set = set()  # Set of executed step labels

        if 'steps' in data and isinstance(data['steps'], list):
            for step_data in data['steps']:
                self.steps.append(TBattleScriptStep(step_data))

    def apply_to(self, generator ) -> None:
        """
        Apply the script to the generator, filling the block grid according to the steps.
        """
        import random
        import time
        random.seed(time.time())

        block_counts = {}

        for step in self.steps:

            # Check chance (probability of applying this step)
            chance = step.chance
            if chance < 1:
                if random.random() > chance:
                    if step.label:
                        self.context.add(-step.label)
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

            # check label / condition system
            if step.condition:
                if not self.meets_conditions(step):
                    if step.label:
                        self.context.add(-step.label)
                    continue

            # Skip if no valid blocks and not filling
            if not filtered_blocks and step.type != 'fill_block':
                if step.label:
                    self.context.add(-step.label)
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

            # Mark this step as executed
            if step.label:
                self.context.add(step.label)

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

    def place_large_block(self, generator, block_entry, x, y):
        """
        Place a large block on the map grid at (x, y), marking the top-left with the block name and the rest with '-'.
        Returns True if placed, False if not possible.
        """
        width = block_entry.size
        height = block_entry.size
        # Check if block fits
        if y + height > generator.map_height or x + width > generator.map_width:
            return False
        for dy in range(height):
            for dx in range(width):
                if generator.block_grid[y+dy][x+dx] is not None:
                    return False
        # Place block only at top-left, mark others with '-'
        generator.block_grid[y][x] = block_entry.map
        for dy in range(height):
            for dx in range(width):
                if dy != 0 or dx != 0:
                    generator.block_grid[y+dy][x+dx] = '-'
        return True

    def process_add_line(self, generator, step: TBattleScriptStep, blocks: list) -> None:
        """
        Add blocks in a line according to direction (horizontal, vertical, or both).
        For 'both', fill both a random row and a random column independently.
        """
        import random
        direction = step.direction
        runs = step.runs
        row = getattr(step, 'row', None)
        col = getattr(step, 'col', None)

        for _ in range(runs):
            if direction == 'horizontal':
                y = row if row is not None else random.randint(0, generator.map_height - 1)
                for x in range(generator.map_width):
                    if generator.block_grid[y][x] is None and blocks:
                        block_entry = random.choice(blocks)
                        self.place_large_block(generator, block_entry, x, y)
            elif direction == 'vertical':
                x = col if col is not None else random.randint(0, generator.map_width - 1)
                for y in range(generator.map_height):
                    if generator.block_grid[y][x] is None and blocks:
                        block_entry = random.choice(blocks)
                        self.place_large_block(generator, block_entry, x, y)
            elif direction == 'both':
                # Fill a random row
                y = row if row is not None else random.randint(0, generator.map_height - 1)
                for x in range(generator.map_width):
                    if generator.block_grid[y][x] is None and blocks:
                        block_entry = random.choice(blocks)
                        self.place_large_block(generator, block_entry, x, y)
                # Fill a random column
                x = col if col is not None else random.randint(0, generator.map_width - 1)
                for y in range(generator.map_height):
                    if generator.block_grid[y][x] is None and blocks:
                        block_entry = random.choice(blocks)
                        self.place_large_block(generator, block_entry, x, y)

    def process_add_block(self, generator, step: TBattleScriptStep, blocks: list, block_counts: Dict) -> None:
        """
        Add a random block to a random available position on the map.
        Take into account max count if specified (runs).
        Handles large blocks by only assigning the top-left cell, and marking the rest with '-'.
        Ensures blocks are placed in random positions, not always from top-left.
        """
        import random
        max_count = step.runs if hasattr(step, 'runs') else 1
        group_key = f"block_{step.group}_{step.size}"
        current_count = block_counts.get(group_key, 0)
        runs = min(max_count, generator.map_width * generator.map_height - current_count)
        placed = 0
        for _ in range(runs):
            if not blocks:
                break
            block_entry = random.choice(blocks)
            width = block_entry.size
            height = block_entry.size
            # Collect all possible positions where the block fits
            possible_positions = []
            for y in range(generator.map_height - height + 1):
                for x in range(generator.map_width - width + 1):
                    fits = True
                    for dy in range(height):
                        for dx in range(width):
                            if generator.block_grid[y+dy][x+dx] is not None:
                                fits = False
                                break
                        if not fits:
                            break
                    if fits:
                        possible_positions.append((x, y))
            if possible_positions:
                x, y = random.choice(possible_positions)
                self.place_large_block(generator, block_entry, x, y)
                placed += 1
            block_counts[group_key] = block_counts.get(group_key, 0) + 1
            current_count = block_counts[group_key]
            if current_count >= max_count:
                break

    def process_fill_block(self, generator, step: TBattleScriptStep, blocks: list) -> None:
        """
        Fill all remaining empty positions with random blocks.
        Handles large blocks by only assigning the top-left cell, and marking the rest with '-'.
        Runs up to 1000 times or until all cells are filled.
        """
        import random

        if not blocks or len(blocks) == 0:
            return

        for _ in range(1000):
            empty_found = False
            for y in range(generator.map_height):
                for x in range(generator.map_width):
                    if generator.block_grid[y][x] is None:
                        empty_found = True
                        block_entry = random.choice(blocks)
                        width = block_entry.size
                        height = block_entry.size
                        placed = False
                        for yy in range(generator.map_height - height + 1):
                            for xx in range(generator.map_width - width + 1):
                                if all(generator.block_grid[yy+dy][xx+dx] is None for dy in range(height) for dx in range(width)):
                                    self.place_large_block(generator, block_entry, xx, yy)
                                    placed = True
                                    break
                            if placed:
                                break
                        if not placed:
                            # fallback to 1x1 block if available
                            single_blocks = [b for b in blocks if b.size == 1]
                            if single_blocks:
                                self.place_large_block(generator, single_blocks[0], x, y)
                        break
                if empty_found:
                    break
            if not empty_found:
                break

    def process_add_special(self, generator, step: TBattleScriptStep, blocks: list, special_type: str) -> None:
        """
        Add a special block (by name) to the first available position where it fits, replacing any existing block.
        The special block name is provided as special_type.
        """
        import random
        # Find the special block entry by name
        special_blocks = [b for b in blocks if b.map == special_type]
        if not special_blocks:
            return
        block_entry = special_blocks[0]
        width = block_entry.size
        height = block_entry.size
        for y in range(generator.map_height - height + 1):
            for x in range(generator.map_width - width + 1):
                # Always replace existing blocks, so no need to check if empty
                self.place_large_block(generator, block_entry, x, y)
                return

    def meets_conditions(self, step : TBattleScriptStep) -> bool:
        """
        Check if all conditions for this step are met based on a set of numeric labels.

        Args:
            context: Set of integers representing executed (positive) or
                    skipped (negative) step labels

        Returns:
            True if all conditions are met, False otherwise
        """
        # If no conditions, always proceed
        if not step.condition:
            return True

        # Process each condition
        for condition in step.condition:
            try:
                # Convert string condition to integer
                condition_value = int(condition)

                # Positive condition: step must have been executed
                if condition_value > 0:
                    if condition_value not in self.context:
                        return False
                # Negative condition: step must NOT have been executed
                elif condition_value < 0:
                    if abs(condition_value) in self.context:
                        return False
            except ValueError:
                # If condition isn't a number, ignore it
                continue

        return True
