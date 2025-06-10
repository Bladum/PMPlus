"""
Battle generator module for creating battle maps from map blocks according to a script.
"""
import pathlib
from typing import List, Optional, Dict, Tuple, Any
import random
from PIL import Image
import csv
import os

from battle.terrain.terrain import TTerrain
from engine.battle.map.battle_script import TBattleScript
from engine.battle.tile.battle_tile import TBattleTile
from battle.terrain.map_block import TMapBlock


class TBattleGenerator:
    """
    Generates a battle map using terrain's map blocks and map script.
    Follows the XCOM/OpenXcom map generation approach using map blocks and scripts.

    Attributes:
        terrain (TTerrain): The terrain object containing map blocks and settings.
        script (TBattleScript|None): The map script that defines how to assemble the map.
        map_width (int): Number of map blocks horizontally (4-7).
        map_height (int): Number of map blocks vertically (4-7).
        block_size (int): Standard map block size (15x15 tiles).
        block_grid (list[list[str]]): 2D array of block names.
        battle_map (list[list[TBattleTile]]): 2D array of TBattleTile objects.
    """
    def __init__(self, terrain: TTerrain, script: TBattleScript = None, blocks_x: int = 4, blocks_y: int = 4):
        """
        Initialize the battle generator with terrain, script, and map size.

        Args:
            terrain: The terrain object containing map blocks and settings
            script: The map script that defines how to assemble the map
            blocks_x: Number of map blocks horizontally (4-7)
            blocks_y: Number of map blocks vertically (4-7)
        """


        from engine.engine.game import TGame  # Avoid circular import
        self.game = TGame()

        self.terrain = terrain
        self.script = script
        self.map_width = max(4, min(blocks_x, 7))  # Ensure between 4-7
        self.map_height = max(4, min(blocks_y, 7))  # Ensure between 4-7

        self.block_size = 15  # Standard map block size (15x15 tiles)
        self.block_grid: List[List[str]] = []
        self.battle_map: List[List[TBattleTile]] = []

        # Initialize empty block grid
        self.initialize_block_grid()

    def initialize_block_grid(self) -> None:
        """
        Initialize an empty map block grid.
        """
        self.block_grid = [[None for _ in range(self.map_width)] for _ in range(self.map_height)]
        self.battle_map = [[TBattleTile() for _ in range(self.map_width * 15)] for _ in range(self.map_height * 15)]

    def generate(self) -> List[List[TBattleTile]]:
        """
        Main method to generate the battle map using the map script.

        1. Apply the script to fill the block grid
        2. Print the block grid for debugging
        3. Build the final battle map by copying tiles from each block
        4. Validate the battle map

        Returns:
            The complete battle map as a 2D array of TBattleTile objects
        """

        import random
        import time
        random.seed(time.time())

        # Apply script to fill the block grid
        self.script.apply_to(self)

        # Print block grid for debugging
        self.print_block_grid()

        # Build the final battle map
        self.build_battle_map()

        # Validate the battle map
        if not self.validate_battle_map():
            print("ERROR: Battle map validation failed!")

        return self.battle_map


    def build_battle_map(self) -> None:
        """
        Build the final battle map by copying tiles from each block in the grid.
        Each entry in block_grid is a block name (string). Get the TMapBlock from mod.map_blocks.
        """
        battle_map_width = self.map_width * self.block_size
        battle_map_height = self.map_height * self.block_size
        self.battle_map = [[TBattleTile() for _ in range(battle_map_width)] for _ in range(battle_map_height)]

        # Get the map_blocks dictionary from the terrain's mod
        map_blocks = self.game.mod.map_blocks

        for by in range(self.map_height):
            for bx in range(self.map_width):
                block_name = self.block_grid[by][bx]
                if block_name == '-':
                    continue
                if not block_name or block_name not in map_blocks.keys():
                    print(f"ERROR: Block '{block_name}' not found in map_blocks at {bx},{by}")
                    continue
                map_block = map_blocks[block_name]
                for ty in range(map_block.size * 15):
                    for tx in range(map_block.size * 15):
                        map_x = bx * self.block_size + tx
                        map_y = by * self.block_size + ty
                        if 0 <= map_x < battle_map_width and 0 <= map_y < battle_map_height:
                            block_tile = map_block.get_tile(tx, ty)
                            if block_tile:
                                self.battle_map[map_y][map_x] = block_tile.copy()
                            else:
                                print(f"ERROR: Missing tile at {tx},{ty} in block '{block_name}' at {bx},{by}")

    def validate_battle_map(self) -> bool:
        """
        Validate that the battle map is correctly built.
        Each tile must have a valid floor_id.

        Returns:
            True if validation passes, False otherwise
        """
        map_width = self.map_width * self.block_size
        map_height = self.map_height * self.block_size

        for y in range(map_height):
            for x in range(map_width):
                tile = self.battle_map[y][x]
                try:
                    if tile.floor_id is None:
                        print(f"ERROR: Missing floor_id at {x},{y}")
                        return False
                except AttributeError:
                    print(f"ERROR: Invalid tile at {x},{y} - missing floor_id attribute")
                    return False
        return True

    def print_block_grid(self) -> None:
        """
        Print the block grid to console, representing each block by its
        top left corner tile ID or '-' if empty.
        """
        print("MAP BLOCK GRID:")
        for y in range(self.map_height):
            row = []
            for x in range(self.map_width):
                if self.block_grid[y][x] is None:
                    row.append('-')
                else:
                    block = self.block_grid[y][x]
                    try:
                        if block:  # Direct attribute access with error handling
                            row.append(block[:12].ljust(12))  # Fill to 12 characters
                        else:
                            row.append('B')  # Generic 'B' for block
                    except AttributeError:
                        row.append('B')  # Generic 'B' for block
            print(' '.join(row))

    def render_to_png(self, filepath: str) -> None:
        """
        Render the battle map to a PNG image.

        """
        user_docs =  self.game.mod.mod_path / 'export' / 'generator'
        user_docs.mkdir(parents=True, exist_ok=True)
        out_path = user_docs / f"{filepath}.png"

        map_width = self.map_width * self.block_size
        map_height = self.map_height * self.block_size
        tile_pixel_size = 16  # Assuming each tile is 16x16 pixels in the tileset

        # Create image with the right dimensions
        img = Image.new('RGB', (map_width * tile_pixel_size, map_height * tile_pixel_size), (0, 0, 0))

        # Get tileset manager from game.mod
        from engine.engine.game import TGame
        game = TGame()
        tileset_manager = game.mod.tileset_manager

        if not tileset_manager:
            print("WARNING: No tileset manager available, rendering blank image")
            img.save(out_path)
            return

        # Draw each tile layer by layer
        for y in range(map_height):
            for x in range(map_width):
                tile = self.battle_map[y][x]

                # Draw floor layer
                if tile.floor_id is not None:
                    tile_img, tile_mask = tileset_manager.all_tiles.get(tile.floor_id, (None, None))
                    if tile_img:
                        img.paste( tile_img,(x * tile_pixel_size, y * tile_pixel_size), tile_mask )

                # Draw wall layer
                if tile.wall_id is not None:
                    tile_img, tile_mask = tileset_manager.all_tiles.get(tile.wall_id, (None, None))
                    if tile_img:
                        img.paste( tile_img,(x * tile_pixel_size, y * tile_pixel_size), tile_mask )

                # # Draw roof layer
                # if tile.roof_id is not None:
                #     tile_img, tile_mask = tileset_manager.all_tiles.get(tile.roof_id, (None, None))
                #     if tile_img:
                #         img.paste( tile_img,(x * tile_pixel_size, y * tile_pixel_size), tile_mask )

        # Save the image
        img.save(out_path)
        print(f"Battle map rendered to {out_path}")

    def export_to_csv(self, filepath: str) -> None:
        """
        Export the battle map to a CSV file.
        Only the floor_id is exported.

        Args:
            filepath: Path to save the CSV file
        """
        map_width = self.map_width * self.block_size
        map_height = self.map_height * self.block_size

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for y in range(map_height):
                row = []
                for x in range(map_width):
                    tile = self.battle_map[y][x]
                    try:
                        row.append(tile.floor_id)
                    except AttributeError:
                        row.append(0)  # Default if floor_id doesn't exist
                writer.writerow(row)
        print(f"Battle map exported to {filepath}")
