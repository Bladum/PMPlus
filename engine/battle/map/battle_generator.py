from engine.battle.terrain import TTerrain
from engine.battle.terrain.map_block import TMapBlock
from engine.battle.terrain.map_block_entry import TMapBlockEntry
from engine.battle.map.battle_script import TBattleScript

class TBattleGenerator:
    """
    Generates a battle map using terrain's map blocks and map script.
    Mimics XCOM/OpenXcom map generation using map blocks and scripts.
    """
    def __init__(self, terrain: TTerrain, script: TBattleScript = None, blocks_x=4, blocks_y=4):
        self.terrain = terrain
        self.script = script if script else terrain.script
        self.blocks_x = blocks_x  # Number of map blocks horizontally
        self.blocks_y = blocks_y  # Number of map blocks vertically
        self.block_size = 15  # Default block size (can be overridden by block)
        self.block_grid = []  # 2D array of TMapBlock
        self.battle_map = []  # 2D array of TBattleTile

    def generate(self):
        """
        Main method to generate the battle map using the map script.
        Fills self.battle_map with TBattleTile instances.
        """
        self._init_block_grid()
        self.script.apply_to(self)
        self._build_battle_map()
        return self.battle_map

    def _init_block_grid(self):
        """
        Initializes the grid for map blocks. The grid is empty at the start.
        """
        self.block_grid = [[None for _ in range(self.blocks_x)] for _ in range(self.blocks_y)]

    def _build_battle_map(self):
        """
        Build the final battle map by copying tiles from map blocks into the full map.
        Handles blocks of different sizes and ensures no tile is lost.
        """
        # Calculate total map size
        total_width = sum(self.block_grid[0][x].size if self.block_grid[0][x] else self.block_size for x in range(self.blocks_x))
        total_height = sum(self.block_grid[y][0].size if self.block_grid[y][0] else self.block_size for y in range(self.blocks_y))
        self.battle_map = [[None for _ in range(total_width)] for _ in range(total_height)]
        y_offset = 0
        for by, block_row in enumerate(self.block_grid):
            x_offset = 0
            block_height = block_row[0].size if block_row[0] else self.block_size
            for bx, block in enumerate(block_row):
                block_width = block.size if block else self.block_size
                if block:
                    for i in range(block_height):
                        for j in range(block_width):
                            self.battle_map[y_offset + i][x_offset + j] = block.tiles[i][j]
                x_offset += block_width
            y_offset += block_height

