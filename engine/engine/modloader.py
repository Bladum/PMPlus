from pathlib import Path
import yaml  # Replacing tomli with yaml

from battle.map.battle_generator import TBattleGenerator
from engine.engine.tiled.tileset_manager import TTileManager


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
        rules3_path = self.mod_path / 'rules3'
        if not rules3_path.is_dir():
            raise FileNotFoundError(f"Rules3 folder not found: {rules3_path}")

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

    from engine.engine.mod import TMod
    game.mod = TMod(loader.yaml_data, mod_path)  # Changed to use yaml_data

    game.mod.load_objects_from_data()
    game.mod.tileset_manager = TTileManager(mod_name, game.mod.tiles_path)
    game.mod.tileset_manager.export_all_images()

    game.mod.load_all_terrain_map_blocks()

    ter = game.mod.terrains.get('farmland')
    script = game.mod.map_scripts.get('polar')
    gg = TBattleGenerator(ter, script, blocks_x=6, blocks_y=6)
    gg.generate()
    gg.print_used_map_blocks()
    gg.render_to_png('battle_map')
    gg.render_to_csv('battle_map')

