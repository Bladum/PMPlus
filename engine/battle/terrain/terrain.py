import os
import glob
import xml.etree.ElementTree as ET
import pytmx

from battle.terrain.map_block import TMapBlock
from battle.terrain.map_block_entry import TMapBlockEntry
from engine.battle.tile.battle_tile import TBattleTile
from engine.battle.tile.battle_floor import TBattleFloor
from engine.battle.tile.battle_wall import TBattleWall
from battle.terrain.tmx_map_loader import TMXMapLoader


class TTerrain:
    """
    Represents a terrain type, it is used to generate map for battle
    Each terrain may be linked with BIOME or be separated
    Terrain has list of map blocks and map script used to generate battle map
    """
    def __init__(self, terrain_id, data):
        self.id = terrain_id
        self.name = data.get('name', terrain_id)
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

        self.map_files = {}
        self.map_blocks_entries = map_blocks


    def load_maps_and_blocks(self, mod_name):
        """
        1. Scan its own folder for maps and load all content to dict called map_files
        2. Load all map_blocks and create TMapBlockEntry for each (already done in __init__)
        3. For each mapblockentry, get map from map_files and create the actual map_block (tiles from tmx layers)
        """
        # Step 1: Scan for TMX files and load them
        maps_path = os.path.join('mods', mod_name, 'maps', self.maps_folder)
        tmx_files = glob.glob(os.path.join(maps_path, '*.tmx'))
        self.map_files = {}
        for tmx_file in tmx_files:
            file_name = os.path.splitext(os.path.basename(tmx_file))[0]
            try:
                tmx_data = pytmx.TiledMap(tmx_file)
                self.map_files[file_name] = tmx_data
            except Exception as e:
                self.map_files[file_name] = None

        # Step 2: MapBlockEntry creation is done in __init__

        # Step 3: For each mapblockentry, get map from map_files and create the actual map_block
        self.map_blocks = []
        for entry in self.map_blocks_entries:
            tmx = self.map_files.get(entry.map)
            if tmx is None:
                self.map_blocks.append(None)
                continue

            gid_map = TMXMapLoader.load_tilesets(tmx)
            map_block = TMapBlock.from_tmx(tmx, gid_map)
            self.map_blocks.append(map_block)
