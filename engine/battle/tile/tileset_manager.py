import xml.etree.ElementTree as ET
from PIL import Image
import os
import glob

class TTilesetManager:
    def __init__(self, folder_path):
        self.folder_path = str(folder_path)
        self.all_tiles = {}  # flat dict: key -> (tile_img, mask)
        self.tilesets = {}   # dict: tileset_name -> {key -> (tile_img, mask)}

    def load_tileset(self, tsx_path):
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
        tiles = {}
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

            key = f"{tileset_name}_{i+1:03d}"
            tiles[key] = (tile_img, mask)
        return tiles

    def load_all_tilesets_from_folder(self, ):
        self.tilesets = {}
        self.all_tiles = {}

        tsx_files = glob.glob(os.path.join(self.folder_path, '**', '*.tsx'), recursive=True)
        print(f"Found {len(tsx_files)} TSX files in {self.folder_path} (recursive)")
        for tsx_file in tsx_files:
            tileset_name = os.path.splitext(os.path.basename(tsx_file))[0]
            tiles = self.load_tileset(tsx_file)
            self.tilesets[tileset_name] = {}
            for i, (key, tile_tuple) in enumerate(tiles.items(), 1):
                tile_key = f"{tileset_name}_{i:03d}"
                self.all_tiles[tile_key] = tile_tuple
                self.tilesets[tileset_name][tile_key] = tile_tuple

    def save_tiles_to_folders(self, output_root):
        for key, tile_tuple in self.all_tiles.items():
            img, mask = tile_tuple
            if '_' in key:
                tileset, num = key.rsplit('_', 1)
                folder_name = f"{tileset}"
                folder_path = os.path.join(output_root, folder_name)
                os.makedirs(folder_path, exist_ok=True)
                file_path = os.path.join(folder_path, f"{tileset}_{int(num):03d}.png")
                img.save(file_path)

# Example usage:
# mgr = TTilesetManager()
# mgr.load_all_tilesets_from_folder('../../../mods/xcom/tiles')
# mgr.save_tiles_to_folders('output_tiles')
# tile_img = mgr.all_tiles.get('desert_07')
# print(mgr.tilesets['desert'].keys())
