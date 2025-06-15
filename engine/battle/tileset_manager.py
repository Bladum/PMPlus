"""
engine/battle/tileset_manager.py

Defines the TTilesetManager class, which loads and manages all tile images from tilesets and individual images for the battle system.

Classes:
    TTilesetManager: Loads, processes, and provides access to all tile images and masks for the battle map.

Last standardized: 2025-06-15
"""

import xml.etree.ElementTree as ET
from PIL import Image
import os
import glob

class TTilesetManager:
    """
    Loads and manages all tile images from tilesets and individual images.

    Attributes:
        folder_path (str): Path to the folder containing tilesets.
        all_tiles (dict): Dictionary mapping tile keys to (image, mask) tuples.
    """

    def __init__(self):
        """
        Initialize the tileset manager.
        """
        self.folder_path = ''
        self.all_tiles = {}

    def load_tileset(self, tsx_path):
        """
        Load a single tileset from a TSX file and add its tiles to all_tiles.

        Args:
            tsx_path (str): Path to the TSX file.
        """
        tree = ET.parse(tsx_path)
        root = tree.getroot()
        image_elem = root.find('image')
        image_path = image_elem.get('source')
        tsx_dir = os.path.dirname(tsx_path)
        image_full_path = os.path.join(tsx_dir, image_path)
        image = Image.open(image_full_path)
        tilewidth = int(root.get('tilewidth')) + 2
        tileheight = int(root.get('tileheight')) + 2
        columns = int(root.get('columns', 10))
        tilecount = int(root.get('tilecount', 100))
        tileset_name = os.path.splitext(os.path.basename(tsx_path))[0]

        for i in range(min(tilecount, 100)):
            row = i // columns
            col = i % columns
            left = col * tilewidth + 1
            upper = row * tileheight + 1
            right = left + tilewidth - 2
            lower = upper + tileheight - 2
            tile_img = image.crop((left, upper, right, lower))

            # Preprocess: convert to RGBA and extract mask
            if tile_img.mode != 'RGBA':
                tile_img = tile_img.convert('RGBA')
            mask = tile_img.split()[3] if tile_img.mode == 'RGBA' else None

            # Store directly in all_tiles with the key format tileset_name_XXX
            key = f"{tileset_name}_{i+1:03d}"
            self.all_tiles[key] = (tile_img, mask)

    def load_all_tilesets_from_folder(self):
        """
        Load all tilesets from the folder_path and add their tiles to all_tiles.
        """
        self.all_tiles = {}
        tsx_files = glob.glob(os.path.join(self.folder_path, '**', '*.tsx'), recursive=True)
        print(f"Found {len(tsx_files)} TSX files in {self.folder_path} (recursive)")
        for tsx_file in tsx_files:
            self.load_tileset(tsx_file)

    def load_individual_images_from_folder(self, images_folder, recursive=True):
        """
        Load individual PNG files from a folder and its subfolders.
        Each PNG is loaded as a separate tile and added to all_tiles.

        Args:
            images_folder (str): Path to the folder containing PNG files.
            recursive (bool): Whether to search recursively in subfolders.
        """
        images_folder = str(images_folder)
        search_pattern = os.path.join(images_folder, '**', '*.png') if recursive else os.path.join(images_folder, '*.png')
        png_files = glob.glob(search_pattern, recursive=recursive)
        print(f"Found {len(png_files)} PNG files in {images_folder} ({'recursive' if recursive else 'non-recursive'})")

        for png_file in png_files:
            try:
                # Get just the file name without extension for the key
                file_name = os.path.basename(png_file)
                key = os.path.splitext(file_name)[0]

                # Load image
                img = Image.open(png_file)
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')

                # Extract mask from alpha channel
                mask = img.split()[3] if img.mode == 'RGBA' else None

                # Store the image in all_tiles
                self.all_tiles[key] = (img, mask)

            except Exception as e:
                print(f"Error loading image {png_file}: {e}")

    def load_all_images(self, tilesets_folder, individual_images_folder=None):
        """
        Comprehensive method to load all image resources at once.

        Args:
            tilesets_folder (str): Path to folder containing tileset files.
            individual_images_folder (str, optional): Path to folder containing individual PNG files.
        """
        self.folder_path = str(tilesets_folder)
        self.load_all_tilesets_from_folder()

        if individual_images_folder:
            self.load_individual_images_from_folder(individual_images_folder)

    def get_tile(self, key):
        """
        Get a tile by its key from all available tiles.

        Args:
            key (str): The key for the tile.
        Returns:
            tuple: (image, mask) or None if not found.
        """
        return self.all_tiles.get(key)

    def save_tiles_to_folders(self, output_root):
        """
        Save all loaded tiles to folders by tileset name.

        Args:
            output_root (str): Root directory to save tiles into.
        """
        for key, tile_tuple in self.all_tiles.items():
            img, mask = tile_tuple
            if '_' in key:
                tileset, num = key.rsplit('_', 1)
                folder_name = f"{tileset}"
                folder_path = os.path.join(output_root, folder_name)
                os.makedirs(folder_path, exist_ok=True)
                file_path = os.path.join(folder_path, f"{tileset}_{int(num):03d}.png")
                img.save(file_path)

    def print_tileset_info(self):
        """
        Print all tile keys currently loaded in the manager.
        """
        print("Tileset contains the following tile keys:")
        for key in self.all_tiles.keys():
            print("   ", key)

#
# Example usage:
# mgr = TTilesetManager()
# mgr.load_all_images('../../../mods/xcom/tiles', '../../../mods/xcom/images')
# tile_img = mgr.all_tiles.get('desert_07')
# individual_img = mgr.all_tiles.get('ui_buttons_confirm')
#
# manager = TTilesetManager(tileset_folder_path)
#
# # Load both tilesets and individual images
#
# manager.load_all_tilesets_from_folder()  # Loads tile-based images
# manager.load_individual_images_from_folder('mods/xcom/images')  # Loads individual PNGs
#
# # Now all images are accessible through the same all_tiles dictionary
#
# confirm_button = manager.all_tiles['ui_buttons_confirm']  # From individual PNG
# wounded_icon = manager.all_tiles['icons_wounded']         # From individual PNG
# terrain_tile = manager.all_tiles['desert_001']            # From tileset
#
