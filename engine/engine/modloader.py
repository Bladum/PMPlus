import os
import tomli

class TModLoader:
    """
    Class to load mod from files and folders. Loads all TOML files in the mod's folder,
    parses them, and builds a multilevel dict with all data.
    """
    def __init__(self, mod_name):
        self.mod_name = mod_name
        # Find the current file's directory and build the mods path relative to it
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.abspath(os.path.join(current_dir, '../..'))
        self.mod_path = os.path.join(root_dir, 'mods', mod_name)
        self.data = {}
        self._load_all_toml_files()

    def _load_all_toml_files(self):
        if not os.path.isdir(self.mod_path):
            raise FileNotFoundError(f"Mod folder not found: {self.mod_path}")
        for root, _, files in os.walk(self.mod_path):
            for file in files:
                if file.lower().endswith('.toml'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'rb') as f:
                        toml_data = tomli.load(f)
                        for top_key, value in toml_data.items():
                            if top_key not in self.data:
                                self.data[top_key] = {}
                            # Properly merge nested dictionaries
                            if isinstance(value, dict) and isinstance(self.data[top_key], dict):
                                self.data[top_key].update(value)
                            else:
                                self.data[top_key] = value

    def display_top_structure(self):
        """Displays the top-level structure of the loaded mod data."""
        print(f"Loaded data structure for mod '{self.mod_name}':")
        for top_key, value in self.data.items():
            print(f"  {top_key}:")
            if isinstance(value, dict):
                for sub_key in value.keys():
                    print(f"    {sub_key}")
            else:
                print(f"    {type(value).__name__}: {value}")

    def get_data(self):
        """Returns the loaded mod data as a multilevel dict."""
        return self.data

    def test_load_and_display_files(self):
        """
        Test method: Loads and prints all found TOML files in the mod folder.
        """
        print(f"Scanning mod folder: {self.mod_path}")
        if not os.path.isdir(self.mod_path):
            print(f"Mod folder not found: {self.mod_path}")
            return
        found_files = []
        for root, _, files in os.walk(self.mod_path):
            for file in files:
                if file.lower().endswith('.toml'):
                    file_path = os.path.join(root, file)
                    found_files.append(file_path)
        if not found_files:
            print("No TOML files found.")
        else:
            print("Found TOML files:")
            for f in found_files:
                print(f" - {f}")
        print(f"Total TOML files found: {len(found_files)}")

    @staticmethod
    def get_mods_list():
        """
        Loads mods.toml from the mods folder and returns a dict of mods info.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.abspath(os.path.join(current_dir, '../..'))
        mods_toml_path = os.path.join(root_dir, 'mods', 'mods.toml')
        if not os.path.isfile(mods_toml_path):
            raise FileNotFoundError(f"mods.toml not found: {mods_toml_path}")
        with open(mods_toml_path, 'rb') as f:
            mods_data = tomli.load(f)
        return mods_data

    @classmethod
    def from_mods_toml(cls, mod_key=None):
        """
        Loads mods.toml and instantiates TModLoader for the given mod_key (e.g. 'xcom').
        If mod_key is None, loads the first mod found.
        """
        mods_data = cls.get_mods_list()
        if not mods_data:
            raise Exception("No mods found in mods.toml")
        if mod_key is None:
            mod_key = next(iter(mods_data))
        mod_info = mods_data.get(mod_key)
        if not mod_info:
            raise Exception(f"Mod '{mod_key}' not found in mods.toml")
        mod_name = mod_info.get('path', mod_key)
        return cls(mod_name)



# Example usage:
if __name__ == "__main__":
    loader = TModLoader.from_mods_toml('xcom')
    loader.test_load_and_display_files()

    loader.display_top_structure()