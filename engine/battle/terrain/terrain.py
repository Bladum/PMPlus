# terrain.py
# This module defines the TTerrain class, which represents a terrain type for battle map generation.
# Each terrain has a list of map block entries, a map script, and loads TMX map files for use in map generation.

from pathlib import Path
import pytmx

from battle.terrain.map_block import TMapBlock
from battle.terrain.map_block_entry import TMapBlockEntry

class TTerrain:
    """
    Represents a terrain type for battle map generation.
    Each terrain may be linked with a biome or be separated.
    Terrain has a list of map block entries and a map script used to generate the battle map.
    Loads TMX map files and creates TMapBlock objects for each entry.
    """
    def __init__(self, pid, data):
        from engine.engine.game import TGame
        self.game = TGame()

        self.pid = pid
        self.name = data.get('name', pid)
        self.description = data.get('description', '')
        self.tileset = data.get('tileset', '')
        self.script = data.get('script', None)
        self.maps_folder = data.get('maps_folder', None)
        self.units_civilian = data.get('units_civilian', [])

        self.map_blocks_entries : list[TMapBlockEntry] = []  # List of TMapBlockEntry
        self.map_blocks: list[TMapBlock] = []  # List of loaded TMapBlock objects

        # Process map blocks (these are at the top level in array format)
        map_blocks : list[TMapBlockEntry] = []
        for map_block in data.get('map_blocks', []):
            if map_block:
                map_blocks.append(TMapBlockEntry(map_block))

        self.map_tmx_files = {}
        self.map_blocks_entries = map_blocks
        self.tileset_manager = self.game.mod.tileset_manager

    def load_maps_and_blocks(self, maps_path):
        """
        Loads all TMX map files from the given folder, creates TMapBlock objects for each entry.
        1. Scans its own folder for maps and loads all content to dict called map_files.
        2. Loads all map_blocks and creates TMapBlockEntry for each (already done in __init__).
        3. For each mapblockentry, gets map from map_files and creates the actual map_block (tiles from tmx layers).
        4. Renders all map blocks to PNG for debugging/visualization.
        """
        maps_path = Path(maps_path)
        tmx_files = list(maps_path.glob('*.tmx'))
        self.map_tmx_files = {}

        # Step 1: Scan the folder for TMX files and load them
        for tmx_file in tmx_files:
            file_name = tmx_file.stem
            try:
                tmx_data = pytmx.TiledMap(str(tmx_file))
                self.map_tmx_files[file_name] = tmx_data
            except Exception as e:
                print(f"Error loading TMX file {file_name}: {e}")
                self.map_tmx_files[file_name] = None

        print(f"Scanning folder for tmx files in {maps_path}, found {len(tmx_files)} files")

        # Step 2: MapBlockEntry creation is done in __init__

        # Step 3: For each mapblockentry, get map from map_files and create the actual map_block
        self.map_blocks.clear()
        for entry in self.map_blocks_entries:
            tmx_details = self.map_tmx_files.get(entry.map)
            if tmx_details is None:
                continue
            map_block = TMapBlock.from_tmx(tmx_details)
            if map_block is None:
                continue
            map_block.name = entry.map
            self.map_blocks.append(map_block)
            self.game.mod.map_blocks[entry.map] = map_block

        # Step 4. Render all map blocks to PNG
        for map_block in self.map_blocks:
            map_block.render_to_png()

        print(f"Based on terrain map block entries, created {len(self.map_blocks)} map blocks")

    def get_map_block(self, entry: TMapBlock):
        """
        Get a map block by entry.

        Args:
            entry: The map block entry to look up

        Returns:
            The corresponding map block, or None if not found
        """
        if entry in self.map_blocks_entries:
            return entry  # In our mock, entries are the blocks themselves
        return None