import logging
from pathlib import Path
import yaml  # Replacing tomli with yaml

from battle.map.battle_generator import TBattleGenerator
from battle.tile.tileset_manager import TTilesetManager


class TModLoader:
    """
    Loads mod data from YAML files in the mod's rules directory.
    Parses all YAML files and merges them into a unified dictionary (yaml_data).
    This data is used by TMod to instantiate and manage all game entities.

    Attributes:
        mod_name (str): Name of the mod being loaded.
        mod_path (Path): Path to the mod directory.
        yaml_data (dict): Parsed and merged data from all YAML files.
    """
    def __init__(self, mod_name, mod_path):
        """
        Initialize the mod loader.
        Args:
            mod_name (str): Name of the mod.
            mod_path (str or Path): Path to the mod directory.
        """
        self.mod_name = mod_name
        self.mod_path = Path(mod_path)
        self.yaml_data = {}
        logging.debug(f"TModLoader initialized for mod: {mod_name} at {mod_path}")

    def load_all_yaml_files(self):
        """
        Load and merge all YAML files from the rules directory in the mod folder.
        Raises:
            FileNotFoundError: If the rules directory does not exist.
        """
        rules_path = self.mod_path / 'rules'
        if not rules_path.is_dir():
            logging.error(f"Rules folder not found: {rules_path}")
            raise FileNotFoundError(f"Rules folder not found: {rules_path}")

        loaded_files = 0
        for file_path in rules_path.rglob('*.yaml'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    yaml_data = yaml.safe_load(f)
                    if yaml_data:
                        for top_key, value in yaml_data.items():
                            if top_key not in self.yaml_data:
                                self.yaml_data[top_key] = {}
                            if isinstance(value, dict) and isinstance(self.yaml_data[top_key], dict):
                                self.yaml_data[top_key].update(value)
                            else:
                                self.yaml_data[top_key] = value
                        loaded_files += 1
                        logging.info(f"Loaded YAML: {file_path}")
            except Exception as e:
                logging.error(f"Failed to load YAML file {file_path}: {e}")
        logging.info(f"Total YAML files loaded: {loaded_files}")
