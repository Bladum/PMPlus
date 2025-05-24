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
        self.pid: Any = pid
        self.steps: List[TBattleScriptStep] = []

        if 'steps' in data and isinstance(data['steps'], list):
            for step_data in data['steps']:
                self.steps.append(TBattleScriptStep(step_data))

    def apply_to(self, generator) -> None:
        """
        Apply the script to the generator, filling the block grid according to the steps.

        For every step:
        1. Filter available map blocks based on step properties (size, group)
        2. Apply the step based on its type (add_line, add_block, fill_block, etc.)

        Args:
            generator: The battle map generator to apply this script to
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
                name = step.ufo
            elif step.type == 'add_craft':
                name = step.craft

            filtered_blocks = self._filter_blocks(generator, group, size, name)

            # Skip if no valid blocks and not filling
            if not filtered_blocks and step.type != 'fill_block':
                continue

            # Process step based on type
            if step.type == 'add_line':
                self._process_add_line(generator, step, filtered_blocks)
            elif step.type == 'add_block':
                self._process_add_block(generator, step, filtered_blocks, block_counts)
            elif step.type == 'fill_block':
                self._process_fill_block(generator, step, filtered_blocks)
            elif step.type == 'add_ufo':
                self._process_add_special(generator, step, filtered_blocks, 'ufo')
            elif step.type == 'add_craft':
                self._process_add_special(generator, step, filtered_blocks, 'craft')

    def _filter_blocks(self, generator, group: Any = None, size: Any = None, name: str = None) -> list:
        """
        Filter available map block entries by group, size, and/or name.

        Args:
            generator: The battle map generator
            group: Filter by group
            size: Filter by size
            name: Filter by name

        Returns:
            List of matching map block entries
        """
        blocks = generator.terrain.map_blocks_entries

        if group is not None:
            blocks = [b for b in blocks if b.group == group]
        if size is not None:
            blocks = [b for b in blocks if b.size == size]
        if name is not None:
            blocks = [b for b in blocks if b.name == name]

        return blocks

    def _process_add_line(self, generator, step: TBattleScriptStep, blocks: list) -> None:
        """
        Add blocks in a line according to direction (horizontal, vertical, or both).

        Args:
            generator: The battle map generator
            step: The script step to process
            blocks: The filtered blocks to choose from
        """
        import random
        direction = step.direction
        runs = step.runs
        row = getattr(step, 'row', None)
        col = getattr(step, 'col', None)

        for _ in range(runs):
            if direction == 'horizontal' or direction == 'both':
                # Select row: use step.row if set, else random
                y = row if row is not None else random.randint(0, generator.blocks_y - 1)

                # Place blocks along the row
                for x in range(generator.blocks_x):
                    if generator.block_grid[y][x] is None and blocks:
                        block_entry = random.choice(blocks)
                        block = generator._find_map_block_by_entry(block_entry)
                        if block:
                            generator.block_grid[y][x] = block

            if direction == 'vertical' or direction == 'both':
                # Select column: use step.col if set, else random
                x = col if col is not None else random.randint(0, generator.blocks_x - 1)

                # Place blocks along the column
                for y in range(generator.blocks_y):
                    if generator.block_grid[y][x] is None and blocks:
                        block_entry = random.choice(blocks)
                        block = generator._find_map_block_by_entry(block_entry)
                        if block:
                            generator.block_grid[y][x] = block

    def _process_add_block(self, generator, step: TBattleScriptStep, blocks: list, block_counts: Dict) -> None:
        """
        Add a random block to the first available position.
        Take into account max count if specified.

        Args:
            generator: The battle map generator
            step: The script step to process
            blocks: The filtered blocks to choose from
            block_counts: Dictionary tracking block placement counts
        """
        import random

        # Check max count
        max_count = step.runs if hasattr(step, 'runs') else 1
        group_key = f"block_{step.group}_{step.size}"

        current_count = block_counts.get(group_key, 0)
        runs = min(max_count, generator.blocks_x * generator.blocks_y - current_count)

        placed = 0
        for _ in range(runs):
            if blocks:
                block_entry = random.choice(blocks)
                block = generator._find_map_block_by_entry(block_entry)
                if block:
                    for y in range(generator.blocks_y):
                        for x in range(generator.blocks_x):
                            if generator.block_grid[y][x] is None:
                                generator.block_grid[y][x] = block
                                placed += 1
                                break
                        if placed > current_count:
                            break
            block_counts[group_key] = block_counts.get(group_key, 0) + 1
            current_count = block_counts[group_key]
            if current_count >= max_count:
                break
    def _process_fill_block(self, generator, step: TBattleScriptStep, blocks: list) -> None:
        """
        Fill all remaining empty positions with random blocks.

        Args:
            generator: The battle map generator
            step: The script step to process
            blocks: The filtered blocks to choose from
        """
        import random

        # Fill all empty spaces with random blocks
        for y in range(generator.blocks_y):
            for x in range(generator.blocks_x):
                if generator.block_grid[y][x] is None and blocks:
                    block_entry = random.choice(blocks)
                    block = generator._find_map_block_by_entry(block_entry)
                    if block:
                        generator.block_grid[y][x] = block

    def _process_add_special(self, generator, step: TBattleScriptStep, blocks: list, special_type: str) -> None:
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
            block = generator._find_map_block_by_entry(block_entry)
            if block:
                # Try to place in the center first, then anywhere available
                center_y = generator.blocks_y // 2
                center_x = generator.blocks_x // 2

                # Check center and surrounding area first
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        y = center_y + dy
                        x = center_x + dx
                        if (0 <= y < generator.blocks_y and
                            0 <= x < generator.blocks_x and
                            generator.block_grid[y][x] is None):
                            generator.block_grid[y][x] = block
                            return

                # If center area is full, try anywhere
                for y in range(generator.blocks_y):
                    for x in range(generator.blocks_x):
                        if generator.block_grid[y][x] is None:
                            generator.block_grid[y][x] = block
                            return
