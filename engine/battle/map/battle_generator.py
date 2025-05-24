from battle.terrain.terrain import TTerrain
from engine.battle.map.battle_script import TBattleScript
from engine.battle.tile.battle_tile import TBattleTile
from typing import List
import pathlib
from PIL import Image

class TBattleGenerator:
    """
    Generates a battle map using terrain's map blocks and map script.
    Mimics XCOM/OpenXcom map generation using map blocks and scripts.
    """
    def __init__(self, terrain: TTerrain, script: TBattleScript = None, blocks_x=4, blocks_y=4):
        from engine.engine.game import TGame  # Import here to avoid circular references
        self.game = TGame()

        self.terrain = terrain
        self.script = script if script else terrain.script
        self.blocks_x = blocks_x  # Number of map blocks horizontally
        self.blocks_y = blocks_y  # Number of map blocks vertically
        self.block_size = 15  # Default block size (can be overridden by block)
        self.block_grid = []  # 2D array of TMapBlock
        self.battle_map: List[List[TBattleTile]] = []  # 2D array of TBattleTile objects

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

    def render_to_png(self, filename=None):
        """
        Render the battle map to a PNG file using Pillow.
        Similar to how map blocks are rendered, but for the entire battle map.

        Args:
            filename (str, optional): Name for the output file. If None, a default name will be used.

        Returns:
            str: Path to the saved PNG file
        """
        if not self.battle_map:
            return None

        # Calculate dimensions
        map_height = len(self.battle_map)
        map_width = len(self.battle_map[0]) if map_height > 0 else 0

        if map_width == 0 or map_height == 0:
            return None

        # Get tileset manager from game
        tileset_manager = self.game.mod.tileset_manager
        tile_size = 16  # Standard tile size in pixels

        # Create output image
        width_px = map_width * tile_size
        height_px = map_height * tile_size
        out_img = Image.new('RGBA', (width_px, height_px), (0, 0, 0, 0))

        # Collect all used tilesets
        used_tilesets = set()
        for y in range(map_height):
            for x in range(map_width):
                tile = self.battle_map[y][x]
                if tile.floor_id:
                    # Extract tileset info (this would need to be implemented based on your system)
                    # For now, we'll assume all tiles are from the same tileset
                    pass
                if tile.wall_id:
                    pass
                if tile.roof_id:
                    pass

        # Load all tileset images
        processed_images = {}

        # Find used tilesets from the terrain object if available
        for block in getattr(self.terrain, 'blocks', []):
            for tileset in getattr(block, 'used_tilesets', []):
                used_tilesets.add(tileset)

        # Load all images once
        for name, firstid, lastid, countid in used_tilesets:
            for x in range(countid):
                gid = firstid + x
                img = tileset_manager.get_tile_image('battle', name, x + 1)
                if img:
                    # Pre-process images to avoid repeated conversions
                    if img.mode != 'RGBA':
                        img = img.convert('RGBA')
                    mask = img.split()[3] if img.mode == 'RGBA' else None
                    processed_images[gid] = (img, mask)

        # Helper function to draw a tile layer
        def draw_layer(gid, x, y):
            if not gid:
                return

            if gid in processed_images:
                img, mask = processed_images[gid]
                pixel_x, pixel_y = x * tile_size, y * tile_size
                out_img.paste(img, (pixel_x, pixel_y), mask)

        # Draw all tiles
        for y in range(map_height):
            for x in range(map_width):
                tile = self.battle_map[y][x]

                # Draw layers in order: floor, wall, (roof is typically hidden initially)
                if tile.floor_id:
                    draw_layer(tile.floor_id, x, y)
                if tile.wall_id:
                    draw_layer(tile.wall_id, x, y)
                # Optional: draw the roof layer
                # if tile.roof_id:
                #     draw_layer(tile.roof_id, x, y)

        # Create output path and save
        user_docs = pathlib.Path.home() / 'Documents' / 'export' / 'battles'
        user_docs.mkdir(parents=True, exist_ok=True)

        map_name = filename or f"battle_map_{self.terrain.name}_{self.blocks_x}x{self.blocks_y}"
        out_path = user_docs / f"{map_name}.png"
        out_img.save(out_path)

        print(f"Saved battle map image to {out_path}")
        return str(out_path)
