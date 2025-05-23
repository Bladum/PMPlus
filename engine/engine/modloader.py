from pathlib import Path
import tomli

from engine.engine.tiled.tiled_tileset_loader import TilesetLoader


class TModLoader:
    """
    Class to load mod from files and folders. Loads all TOML files in the mod's folder,
    parses them, and builds a multilevel dict with all data.
    """
    def __init__(self, mod_name, mod_path):
        self.mod_name = mod_name
        self.mod_path = Path(mod_path)
        self.toml_data = {}

    def load_all_toml_files(self):
        if not self.mod_path.is_dir():
            raise FileNotFoundError(f"Mod folder not found: {self.mod_path}")
        for file_path in self.mod_path.rglob('*.toml'):
            with open(file_path, 'rb') as f:
                toml_data = tomli.load(f)
                for top_key, value in toml_data.items():
                    if top_key not in self.toml_data:
                        self.toml_data[top_key] = {}
                    # Properly merge nested dictionaries
                    if isinstance(value, dict) and isinstance(self.toml_data[top_key], dict):
                        self.toml_data[top_key].update(value)
                    else:
                        self.toml_data[top_key] = value


# Example usage:
if __name__ == "__main__":

    mod_name = 'xcom'

    current_dir = Path(__file__).resolve().parent
    root_dir = current_dir.parent.parent
    mod_path = root_dir / 'mods' / mod_name

    loader = TModLoader(mod_name, mod_path)
    loader.load_all_toml_files()

    from engine.engine.mod import TMod
    mod = TMod(loader.toml_data, mod_path)

    mod.load_objects_from_data()
    mod.load_all_terrain_map_blocks()

    aaa = TilesetLoader(mod_name, mod.tiles_path)
    aaa.export_all_images()

