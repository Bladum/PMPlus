"""
Battle generator module for creating battle maps from map blocks according to a script.
"""
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
        self.terrain = terrain
        self.script = script if script else terrain.script
        self.blocks_x = max(4, min(blocks_x, 7))  # Ensure between 4-7
        self.blocks_y = max(4, min(blocks_y, 7))  # Ensure between 4-7

        self.block_size = 15  # Standard map block size (15x15 tiles)
        self.block_grid: List[List[Optional[TMapBlock]]] = []
        self.battle_map: List[List[TBattleTile]] = []

        # Initialize empty block grid
        self.initialize_block_grid()

    def initialize_block_grid(self) -> None:
        """
        Initialize an empty map block grid.
        """
        self.block_grid = [[None for _ in range(self.blocks_x)] for _ in range(self.blocks_y)]

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
        # Apply script to fill the block grid
        self.script.apply_to(self)

        # Print block grid for debugging
        self._print_block_grid()

        # Build the final battle map
        self._build_battle_map()

        # Validate the battle map
        if not self._validate_battle_map():
            print("ERROR: Battle map validation failed!")

        return self.battle_map

    def _print_block_grid(self) -> None:
        """
        Print the block grid to console, representing each block by its
        top left corner tile ID or '-' if empty.
        """
        print("MAP BLOCK GRID:")
        for y in range(self.blocks_y):
            row = []
            for x in range(self.blocks_x):
                if self.block_grid[y][x] is None:
                    row.append('-')
                else:
                    block = self.block_grid[y][x]
                    try:
                        if block.name:  # Direct attribute access with error handling
                            row.append(block.name[:3])  # First 3 chars of name
                        else:
                            row.append('B')  # Generic 'B' for block
                    except AttributeError:
                        row.append('B')  # Generic 'B' for block
            print(' '.join(row))

    def _build_battle_map(self) -> None:
        """
        Build the final battle map by copying tiles from each block in the grid.
        """
        # Calculate dimensions of the final battle map
        map_width = self.blocks_x * self.block_size
        map_height = self.blocks_y * self.block_size

        # Initialize battle map with empty tiles
        self.battle_map = [[TBattleTile() for _ in range(map_width)] for _ in range(map_height)]

        # Copy tiles from each block to the battle map
        for by in range(self.blocks_y):
            for bx in range(self.blocks_x):
                block = self.block_grid[by][bx]
                if block:
                    for ty in range(self.block_size):
                        for tx in range(self.block_size):
                            # Calculate position in the battle map
                            map_x = bx * self.block_size + tx
                            map_y = by * self.block_size + ty

                            # Check if position is within map bounds
                            if 0 <= map_x < map_width and 0 <= map_y < map_height:
                                # Get the tile from the block and copy it to the battle map
                                block_tile = block.get_tile(tx, ty)
                                if block_tile:
                                    self.battle_map[map_y][map_x] = block_tile.copy()
                                else:
                                    print(f"ERROR: Missing tile at {tx},{ty} in block at {bx},{by}")

    def _validate_battle_map(self) -> bool:
        """
        Validate that the battle map is correctly built.
        Each tile must have a valid floor_id.

        Returns:
            True if validation passes, False otherwise
        """
        map_width = self.blocks_x * self.block_size
        map_height = self.blocks_y * self.block_size

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

    def render_to_png(self, filepath: str) -> None:
        """
        Render the battle map to a PNG image.

        Args:
            filepath: Path to save the PNG file
        """
        map_width = self.blocks_x * self.block_size
        map_height = self.blocks_y * self.block_size
        tile_pixel_size = 16  # Assuming each tile is 16x16 pixels in the tileset

        # Create image with the right dimensions
        img = Image.new('RGB', (map_width * tile_pixel_size, map_height * tile_pixel_size), (0, 0, 0))

        # Get tileset manager from game.mod
        from engine.engine.game import TGame
        game = TGame()
        tileset_manager = game.mod.tileset_manager

        if not tileset_manager:
            print("WARNING: No tileset manager available, rendering blank image")
            img.save(filepath)
            return

        # Draw each tile layer by layer
        for y in range(map_height):
            for x in range(map_width):
                tile = self.battle_map[y][x]

                # Draw floor layer
                try:
                    if tile.floor_id is not None:
                        tile_img = tileset_manager.get_tile_image(tile.floor_id, 'floor')
                        if tile_img:
                            img.paste(
                                tile_img,
                                (x * tile_pixel_size, y * tile_pixel_size),
                                tile_img if tile_img.mode == 'RGBA' else None
                            )
                except AttributeError:
                    pass  # Skip if floor_id doesn't exist

                # Draw wall layer
                try:
                    if tile.wall_id is not None:
                        tile_img = tileset_manager.get_tile_image(tile.wall_id, 'wall')
                        if tile_img:
                            img.paste(
                                tile_img,
                                (x * tile_pixel_size, y * tile_pixel_size),
                                tile_img if tile_img.mode == 'RGBA' else None
                            )
                except AttributeError:
                    pass  # Skip if wall_id doesn't exist

                # Draw roof layer
                try:
                    if tile.roof_id is not None:
                        tile_img = tileset_manager.get_tile_image(tile.roof_id, 'roof')
                        if tile_img:
                            img.paste(
                                tile_img,
                                (x * tile_pixel_size, y * tile_pixel_size),
                                tile_img if tile_img.mode == 'RGBA' else None
                            )
                except AttributeError:
                    pass  # Skip if roof_id doesn't exist

        # Save the image
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        img.save(filepath)
        print(f"Battle map rendered to {filepath}")

    def export_to_csv(self, filepath: str) -> None:
        """
        Export the battle map to a CSV file.
        Only the floor_id is exported.

        Args:
            filepath: Path to save the CSV file
        """
        map_width = self.blocks_x * self.block_size
        map_height = self.blocks_y * self.block_size

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

    def _find_map_block_by_entry(self, entry: Any) -> Optional[TMapBlock]:
        """
        Find a map block instance by its entry.

        Args:
            entry: The map block entry to search for

        Returns:
            The corresponding map block or None if not found
        """
        from typing import Protocol

        class TerrainWithGetMapBlock(Protocol):
            def get_map_block(self, entry: Any) -> Optional[TMapBlock]:
                ...

        # If entry is already a TMapBlock, return it directly
        if isinstance(entry, TMapBlock):
            return entry

        # Try to get map block via terrain's get_map_block method
        try:
            terrain_with_get_map_block = self.terrain  # type: TerrainWithGetMapBlock
            return terrain_with_get_map_block.get_map_block(entry)
        except (AttributeError, TypeError):
            pass

        return None

