from pathlib import Path
import yaml  # Replacing tomli with yaml

from battle.map.battle_generator import TBattleGenerator
from battle.tile.tileset_manager import TTilesetManager


class TModLoader:
    """
    Class to load mod from files and folders. Loads all YAML files in the mod's rules3 folder,
    parses them, and builds a multilevel dict with all data.
    """
    def __init__(self, mod_name, mod_path):
        self.mod_name = mod_name
        self.mod_path = Path(mod_path)
        self.yaml_data = {}  # Renamed from toml_data to yaml_data

    def load_all_yaml_files(self):  # Renamed from load_all_toml_files
        """Load all YAML files from the rules3 directory in the mod folder"""
        rules3_path = self.mod_path / 'rules'
        if not rules3_path.is_dir():
            raise FileNotFoundError(f"Rules folder not found: {rules3_path}")

        for file_path in rules3_path.rglob('*.yaml'):
            with open(file_path, 'r', encoding='utf-8') as f:
                yaml_data = yaml.safe_load(f)
                if yaml_data:  # Check if the file actually contained data
                    for top_key, value in yaml_data.items():
                        if top_key not in self.yaml_data:
                            self.yaml_data[top_key] = {}
                        # Properly merge nested dictionaries
                        if isinstance(value, dict) and isinstance(self.yaml_data[top_key], dict):
                            self.yaml_data[top_key].update(value)
                        else:
                            self.yaml_data[top_key] = value


# Example usage:
if __name__ == "__main__":

    mod_name = 'xcom'

    from engine.engine.game import TGame
    game = TGame()

    current_dir = Path(__file__).resolve().parent
    root_dir = current_dir.parent.parent
    mod_path = root_dir / 'mods' / mod_name

    loader = TModLoader(mod_name, mod_path)
    loader.load_all_yaml_files()  # Changed to load YAML files

    # load mod data from yaml files
    from engine.engine.mod import TMod
    game.mod = TMod(loader.yaml_data, mod_path)  # Changed to use yaml_data
    game.mod.load_objects_from_data()

    # load all graphics tilesets
    game.mod.tileset_manager = TTilesetManager(game.mod.tiles_path)
    game.mod.tileset_manager.load_all_tilesets_from_folder()

    # # load all map blocks
    # game.mod.load_all_terrain_map_blocks()
    # game.mod.render_all_map_blocks()

    # Load world from TMX file
    from engine.globe.world import TWorld
    world_tmx_path = mod_path / 'worlds' / 'earth.tmx'
    if world_tmx_path.exists():
        game.mod.world = TWorld.from_tmx(world_tmx_path)
        print(f"Loaded world from {world_tmx_path}")
    else:
        print(f"World TMX file not found: {world_tmx_path}")
    game.mod.world.render_tile_map_to_text(mod_path / 'export' / 'world_map.txt')



    # ter = game.mod.terrains.get('farmland')
    # script = game.mod.map_scripts.get('polar')
    #
    # for x in range(9):
    #     gg = TBattleGenerator(ter, script, blocks_x=6, blocks_y=6)
    #     gg.generate()
    #     gg.render_to_png(f'battle_map_{x}.png')

