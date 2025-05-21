from engine.battle.tile.battle_tile import TBattleTile

class TMapBlock:
    """
    Represents a block of map, which is a 2D array of battle tiles (default 15x15, can be larger)
    Used to generate map for battle. Each block can be placed on the battle map grid.
    """
    def __init__(self, size=15):
        self.size = size  # Size of the block (e.g., 15 for 15x15)
        # 2D array of TBattleTile
        self.tiles = [[TBattleTile() for _ in range(size)] for _ in range(size)]

    def get_tile(self, x, y):
        return self.tiles[y][x]

    # Additional logic for loading block data, items, units, etc. can be added here

