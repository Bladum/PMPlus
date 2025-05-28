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

