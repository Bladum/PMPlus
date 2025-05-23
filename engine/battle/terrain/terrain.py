from pathlib import Path
import pytmx

import xml.etree.ElementTree as ET

from battle.terrain.map_block import TMapBlock
from battle.terrain.map_block_entry import TMapBlockEntry


class TTerrain:
    """
    Represents a terrain type, it is used to generate map for battle
    Each terrain may be linked with BIOME or be separated
    Terrain has list of map blocks and map script used to generate battle map
    """
    def __init__(self, pid, data):
        self.pid = pid
        self.name = data.get('name', pid)

        self.description = data.get('description', '')
        self.tileset = data.get('tileset', '')
        self.script = data.get('script', None)
        self.maps_folder = data.get('maps_folder', None)
        self.units_civilian = data.get('units_civilian', [])

        self.map_blocks_entries : list[TMapBlockEntry] = []  # Will be filled later
        self.map_blocks: list[TMapBlock] = []

        # Process map blocks (these are at the top level in array format)
        map_blocks = []
        for map_block in data.get('map_blocks', []):
            if map_block:
                map_blocks.append(TMapBlockEntry(map_block))

        self.map_tmx_files = {}
        self.map_blocks_entries = map_blocks


    def load_maps_and_blocks(self, maps_path):
        """
        1. Scan its own folder for maps and load all content to dict called map_files
        2. Load all map_blocks and create TMapBlockEntry for each (already done in __init__)
        3. For each mapblockentry, get map from map_files and create the actual map_block (tiles from tmx layers)
        """
        maps_path = Path(maps_path)
        tmx_files = list(maps_path.glob('*.tmx'))
        print("Scanning folder for tmx files", maps_path)
        self.map_tmx_files = {}
        for tmx_file in tmx_files:
            file_name = tmx_file.stem
            try:
                tmx_data = pytmx.TiledMap(str(tmx_file))
                self.map_tmx_files[file_name] = tmx_data
            except Exception as e:
                print(f"Error loading TMX file {file_name}: {e}")
                self.map_tmx_files[file_name] = None

        # Step 2: MapBlockEntry creation is done in __init__

        # Step 3: For each mapblockentry, get map from map_files and create the actual map_block

        self.map_blocks = []
        for entry in self.map_blocks_entries:
            tmx_details = self.map_tmx_files.get(entry.map)
            if tmx_details is None:
                self.map_blocks.append(None)
                continue

            map_block = TMapBlock.from_tmx(tmx_details)
            self.map_blocks.append(map_block)

