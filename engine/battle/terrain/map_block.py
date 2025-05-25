# map_block.py
# This module defines the TMapBlock class, which represents a block of the battle map (e.g., 15x15 or larger).
# Each TMapBlock is a 2D array of TBattleTile objects, loaded from a TMX file, and can be rendered to PNG for debugging.

import os
from PIL import Image
from pytmx import TiledMap, TiledTileLayer
import pathlib

from engine.battle.tile.battle_tile import TBattleTile

class TMapBlock:
    """
    Represents a block of map, which is a 2D array of battle tiles (default 15x15, can be larger).
    Used to generate map for battle. Each block can be placed on the battle map grid.
    """
    def __init__(self, size=15):
        from engine.engine.game import TGame  # Avoid circular import
        self.game = TGame()

        self.name = ''  # Name of the block (usually the TMX file name)
        self.group = 0  # Group identifier for filtering blocks
        self.size = size  # Size of the block (e.g., 15 for 15x15)

        # 2D array of TBattleTile
        self.tiles = [[TBattleTile() for _ in range(size)] for _ in range(size)]
        self.used_tilesets = set()  # Set of tilesets used in the block

    def get_tile(self, x, y):
        """Return the TBattleTile at (x, y) in this block."""
        return self.tiles[y][x]

    @classmethod
    def from_tmx(cls, tmx : TiledMap):
        """
        Create a TMapBlock from a TMX map object and optional gid_map.
        """
        # Only process layers: floor, wall, roof
        layers = {l.name: l for l in tmx.visible_layers if hasattr(l, 'data') and l.name in ('floor', 'wall', 'roof')}
        floor_layer :TiledTileLayer = layers.get('floor')
        wall_layer:TiledTileLayer = layers.get('wall')
        roof_layer:TiledTileLayer = layers.get('roof')

        if floor_layer is None:
            return None

        width = floor_layer.width
        height = floor_layer.height

        # Calculate used tilesets for this block
        used_tilesets = {
                (tileset.name,
                 tileset.firstgid,
                 tileset.firstgid + (getattr(tileset, 'tilecount', 0) or getattr(tileset, 'tile_count', 0) or 0) - 1,
                 getattr(tileset, 'tilecount', 0) or getattr(tileset, 'tile_count', 0) or 0)
                for tileset in tmx.tilesets
            }

        # Helper function to process layer data
        def process_layer(layer):
            if layer is None:
                return None

            data = [[0 for _ in range(width)] for _ in range(height)]
            # Pre-compute the division factor (1/18) for better performance
            div_factor = 1.0 / 18

            for x, y, image in layer.tiles():
                ix, iy, _, __ = image[1]
                # Use multiplication instead of division for better performance
                dx = (ix - 1) * div_factor
                dy = (iy - 1) * div_factor
                dn = dy * 10 + dx + 1
                data[y][x] = dn

            return data

        floor_layer_data = process_layer(floor_layer)
        wall_layer_data = process_layer(wall_layer)
        roof_layer_data = process_layer(roof_layer)

        # Create TBattleTile objects for each tile
        tiles = [[None for _ in range(width)] for _ in range(height)]
        for y in range(height):
            for x in range(width):
                floor_gid = floor_layer_data[y][x] if floor_layer_data else 0
                wall_gid = wall_layer_data[y][x] if wall_layer_data else 0
                roof_gid = roof_layer_data[y][x] if roof_layer_data else 0
                tiles[y][x] = TBattleTile.from_gids(floor_gid, wall_gid, roof_gid, used_tilesets)

        block = cls(size=width)
        block.tiles = tiles
        block.name = ''
        block.group = None          # Get group from TMX properties
        block.size = width // 15    # Assuming square blocks, size is width but divided by 15
        block.used_tilesets = used_tilesets

        return block

    def render_to_png(self):
        """
        Render the map block to a PNG file using Pillow.
        Output directory: User Documents/export/maps
        Output PNG name: self.name + ".png"
        """
        tileset_manager = self.game.mod.tileset_manager
        tile_size = 16
        width_px = self.size * tile_size * 15
        height_px = self.size * tile_size * 15
        out_img = Image.new('RGBA', (width_px, height_px), (0, 0, 0, 0))

        # Optimized draw_layer function
        def draw_layer(gid, x, y):
            if not gid:  # Combine None and 0 checks
                return

            img, mask = tileset_manager.all_tiles.get(gid)
            if img:
                pixel_x, pixel_y = x * tile_size, y * tile_size
                out_img.paste(img, (pixel_x, pixel_y), mask)

        # Draw all layers for each tile
        for y in range(self.size * 15):
            for x in range(self.size * 15):
                tile = self.tiles[y][x]
                if tile.floor_id:
                    draw_layer(tile.floor_id, x, y)
                if tile.wall_id:
                    draw_layer(tile.wall_id, x, y)
                #if tile.roof_id:
                #    draw_layer(tile.roof_id, x, y)

        # Save the image
        user_docs = self.game.mod.mod_path / 'export' / 'maps'
        user_docs.mkdir(parents=True, exist_ok=True)
        out_path = user_docs / f"{self.name}.png"
        out_img.save(out_path)
        print(f"Saved map block image to {out_path}")

