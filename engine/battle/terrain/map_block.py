import os

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


    @classmethod
    def from_tmx(cls, tmx):
        """
        Create a TMapBlock from a TMX map object and optional gid_map.
        """

        # Only process layers: floor, wall, roof
        layers = {l.name: l for l in tmx.visible_layers if hasattr(l, 'data') and l.name in ('floor', 'wall', 'roof')}
        floor_layer = layers.get('floor')
        wall_layer = layers.get('wall')
        roof_layer = layers.get('roof')
        if floor_layer is None:
            return None
        width = floor_layer.width
        height = floor_layer.height

        def layer_to_2d(layer):
            data = list(layer.toml_data)
            return [data[y*width:(y+1)*width] for y in range(height)]

        floor_data = layer_to_2d(floor_layer) if floor_layer else [[0]*width for _ in range(height)]
        wall_data = layer_to_2d(wall_layer) if wall_layer else [[0]*width for _ in range(height)]
        roof_data = layer_to_2d(roof_layer) if roof_layer else [[0]*width for _ in range(height)]

        tiles = []
        for y in range(height):
            row = []
            for x in range(width):
                floor_id = floor_data[y][x] if floor_layer else 0
                wall_id = wall_data[y][x] if wall_layer else 0
                roof_id = roof_data[y][x] if roof_layer else 0
                tile = TBattleTile.from_layer_ids(floor_id, wall_id, roof_id)
                row.append(tile)
            tiles.append(row)

        block = cls(size=width)
        block.tiles = tiles
        return block
