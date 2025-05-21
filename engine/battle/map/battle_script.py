from engine.battle.map.battle_script_step import TBattleScriptStep

class TBattleScript:
    """
    Represents a script for map block,
    it is used to generate map for battle from map block in specific way
    """
    def __init__(self, script_id, data):
        self.id = script_id
        # Process steps
        self.steps = []
        if 'steps' in data and isinstance(data['steps'], list):
            for step_data in data['steps']:
                self.steps.append(TBattleScriptStep(step_data))

    def _add_line_blocks(self, generator, step, direction='horizontal'):
        import random
        group = getattr(step, 'group', None)
        size = getattr(step, 'size', generator.block_size)
        blocks = self._filter_blocks(generator, group=group, size=size)
        runs = getattr(step, 'runs', 1)
        row_idx = getattr(step, 'row', None)
        col_idx = getattr(step, 'col', None)
        if direction == 'horizontal':
            for _ in range(runs):
                y = row_idx if row_idx is not None else random.randint(0, generator.blocks_y - 1)
                for x in range(generator.blocks_x):
                    if generator.block_grid[y][x] is None:
                        entry = random.choice(blocks) if blocks else None
                        if entry:
                            generator.block_grid[y][x] = TMapBlock(size=entry.size)
        elif direction == 'vertical':
            for _ in range(runs):
                x = col_idx if col_idx is not None else random.randint(0, generator.blocks_x - 1)
                for y in range(generator.blocks_y):
                    if generator.block_grid[y][x] is None:
                        entry = random.choice(blocks) if blocks else None
                        if entry:
                            generator.block_grid[y][x] = TMapBlock(size=entry.size)
        elif direction == 'both':
            for _ in range(runs):
                y = row_idx if row_idx is not None else random.randint(0, generator.blocks_y - 1)
                x = col_idx if col_idx is not None else random.randint(0, generator.blocks_x - 1)
                for xi in range(generator.blocks_x):
                    if generator.block_grid[y][xi] is None:
                        entry = random.choice(blocks) if blocks else None
                        if entry:
                            generator.block_grid[y][xi] = TMapBlock(size=entry.size)
                for yi in range(generator.blocks_y):
                    if generator.block_grid[yi][x] is None:
                        entry = random.choice(blocks) if blocks else None
                        if entry:
                            generator.block_grid[yi][x] = TMapBlock(size=entry.size)

    def _add_random_block(self, generator, step):
        group = getattr(step, 'group', None)
        size = getattr(step, 'size', generator.block_size)
        blocks = self._filter_blocks(generator, group=group, size=size)
        import random
        entry = random.choice(blocks) if blocks else None
        if entry:
            for y in range(generator.blocks_y):
                for x in range(generator.blocks_x):
                    if generator.block_grid[y][x] is None:
                        generator.block_grid[y][x] = TMapBlock(size=entry.size)
                        return

    def _add_special_block(self, generator, step, special_type):
        name = getattr(step, special_type, None)
        blocks = self._filter_blocks(generator, name=name)
        import random
        entry = random.choice(blocks) if blocks else None
        if entry:
            for y in range(generator.blocks_y):
                for x in range(generator.blocks_x):
                    if generator.block_grid[y][x] is None:
                        generator.block_grid[y][x] = TMapBlock(size=entry.size)
                        return

    def _fill_remaining_blocks(self, generator, step):
        group = getattr(step, 'group', None)
        size = getattr(step, 'size', generator.block_size)
        blocks = self._filter_blocks(generator, group=group, size=size)
        import random
        for y in range(generator.blocks_y):
            for x in range(generator.blocks_x):
                if generator.block_grid[y][x] is None:
                    entry = random.choice(blocks) if blocks else None
                    if entry:
                        generator.block_grid[y][x] = TMapBlock(size=entry.size)

    def _filter_blocks(self, generator, group=None, size=None, name=None):
        blocks = generator.terrain.map_blocks
        if group is not None:
            blocks = [b for b in blocks if getattr(b, 'group', None) == group]
        if size is not None:
            blocks = [b for b in blocks if getattr(b, 'size', generator.block_size) == size]
        if name is not None:
            blocks = [b for b in blocks if getattr(b, 'name', None) == name]
        return blocks

    def apply_to(self, generator):
        for step in self.steps:
            if step.type == 'add_block':
                self._add_line_blocks(generator, step, direction='horizontal')
            elif step.type == 'add_block_vertical':
                self._add_line_blocks(generator, step, direction='vertical')
            elif step.type == 'add_block_both':
                self._add_line_blocks(generator, step, direction='both')
            elif step.type == 'add_random_block':
                self._add_random_block(generator, step)
            elif step.type == 'add_ufo':
                self._add_special_block(generator, step, special_type='ufo')
            elif step.type == 'add_craft':
                self._add_special_block(generator, step, special_type='craft')
            elif step.type == 'fill_block':
                self._fill_remaining_blocks(generator, step)
