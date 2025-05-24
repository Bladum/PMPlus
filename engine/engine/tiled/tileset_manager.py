# Requires: pip install pytmx pillow
import os
from pathlib import Path
from pytmx import TiledTileset
from PIL import Image
from collections import defaultdict
import functools

class TTileManager:
    """
    Loads and splits Tiled (.tsx) tilesets and their PNGs into tile images using pytmx.
    Stores them in three dicts: battle, unit, world.
    """
    def __init__(self, mod_name, path_tiles=None):
        """
        mod_name: name of the mod (folder inside mods/)
        mods_root: optional, path to mods root. Can be relative (e.g. '../../mods') or absolute.
            If not given, will resolve relative to project root.
        """
        print(f"Loading tilesets from mod: {mod_name} in {path_tiles}")
        self.mod_name = mod_name
        self.path_tiles = path_tiles

        # Use dictionaries with tuple keys for faster lookups
        self.battle = {}
        self.unit = {}
        self.world = {}

        # Cache for loaded tileset images to avoid reloading
        self._image_cache = {}

        # Store tileset metadata to avoid re-parsing TSX files
        self._tileset_metadata = {}

        # Map of tileset paths to category for faster lookup
        self._tileset_categories = {}

        # Cache processed tile locations for faster cropping
        self._tile_locations = {}

        # Lazy loading - we'll scan the mod directory but only load tilesets when needed
        self._scan_mod_tiles()

    def _scan_mod_tiles(self):
        """Scan for tileset files but don't load them yet"""
        tiles_dir = Path(self.path_tiles)
        if not tiles_dir.is_dir():
            return

        for root, dirs, files in os.walk(tiles_dir):
            for fname in files:
                if fname.endswith('.tsx'):
                    tsx_path = Path(root) / fname

                    # Determine category based on parent folder
                    rel_path = tsx_path.relative_to(self.path_tiles)
                    rel_parts = rel_path.parts
                    rel_parts_lower = [p.lower() for p in rel_parts]

                    # Only check the immediate parent folder for group assignment
                    parent_folder = rel_parts_lower[-2] if len(rel_parts_lower) > 1 else ''

                    if 'battle' in parent_folder:
                        category = 'battle'
                    elif 'unit' in parent_folder:
                        category = 'unit'
                    elif 'world' in parent_folder:
                        category = 'world'
                    else:
                        continue  # Skip if not in a recognized category

                    # Store the category for this tileset path
                    self._tileset_categories[str(tsx_path)] = category

                    # Read and store metadata now to avoid parsing the file multiple times
                    try:
                        metadata = self._read_tsx_info(tsx_path)
                        self._tileset_metadata[str(tsx_path)] = metadata
                    except Exception as e:
                        print(f"Error reading tileset metadata for {tsx_path}: {e}")

    @functools.lru_cache(maxsize=32)
    def _get_tileset_image(self, image_path):
        """Load and cache tileset image"""
        if image_path in self._image_cache:
            return self._image_cache[image_path]

        try:
            image = Image.open(image_path)
            self._image_cache[image_path] = image
            return image
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            return None

    def _calculate_tile_positions(self, metadata, image_size):
        """Precompute all tile positions in a tileset"""
        key = (metadata['name'],
               metadata['tilewidth'],
               metadata['tileheight'],
               metadata['spacing'],
               metadata['margin'],
               image_size[0],
               image_size[1])

        # Return cached positions if available
        if key in self._tile_locations:
            return self._tile_locations[key]

        tilewidth = metadata['tilewidth']
        tileheight = metadata['tileheight']
        spacing = metadata['spacing']
        margin = metadata['margin']
        img_width, img_height = image_size

        # Defensive: avoid division by zero
        if tilewidth <= 0 or tileheight <= 0:
            return {}

        columns = (img_width - 2 * margin + spacing) // (tilewidth + spacing)
        rows = (img_height - 2 * margin + spacing) // (tilewidth + spacing)

        # Precompute all positions
        positions = {}
        tile_id = 1

        for y in range(rows):
            for x in range(columns):
                left = margin + x * (tilewidth + spacing)
                upper = margin + y * (tileheight + spacing)
                right = left + tilewidth
                lower = upper + tileheight

                if right <= img_width and lower <= img_height:
                    positions[tile_id] = (left, upper, right, lower)
                    tile_id += 1

        # Cache the positions
        self._tile_locations[key] = positions
        return positions

    def _load_tileset_on_demand(self, tsx_path):
        """Load a tileset only when tiles from it are requested"""
        category = self._tileset_categories.get(str(tsx_path))
        if not category or str(tsx_path) not in self._tileset_metadata:
            return None

        metadata = self._tileset_metadata[str(tsx_path)]
        name = metadata['name']

        # Check if already loaded
        if name in getattr(self, category):
            return name

        # Now we need to load the image and extract tiles
        try:
            # If image_source is an absolute path, use it directly; otherwise, join with tiles_dir
            tiles_dir = Path(tsx_path).parent
            image_source = metadata['image_source']
            image_path = Path(image_source) if Path(image_source).is_absolute() else (tiles_dir / image_source).resolve()

            if not image_path.is_file():
                print(f"Warning: Image file not found for tileset {name}: {image_path}")
                return None

            image = self._get_tileset_image(str(image_path))
            if not image:
                return None

            # Calculate positions for all tiles at once
            positions = self._calculate_tile_positions(metadata, image.size)

            # Extract all tiles at once
            tiles = {}
            for tile_id, crop_box in positions.items():
                tile_img = image.crop(crop_box)
                tiles[tile_id] = tile_img

            # Store in the appropriate category
            getattr(self, category)[name] = tiles

            return name
        except Exception as e:
            print(f"Error loading tileset {tsx_path}: {e}")
            return None

    def _read_tsx_info(self, tsx_path):
        """Read metadata from a TSX file without loading the entire tileset"""
        import xml.etree.ElementTree as ET
        tree = ET.parse(str(tsx_path))
        root = tree.getroot()
        if root.tag != 'tileset':
            raise ValueError("Root element is not <tileset>")
        name = root.attrib.get('name')
        tilewidth = int(root.attrib.get('tilewidth', 0))
        tileheight = int(root.attrib.get('tileheight', 0))
        spacing = int(root.attrib.get('spacing', 0))
        margin = int(root.attrib.get('margin', 0))
        image_elem = root.find('image')
        if image_elem is None or 'source' not in image_elem.attrib:
            raise ValueError("No <image> with source attribute found")
        image_source = image_elem.attrib['source']
        image_width = int(image_elem.attrib.get('width', 0))
        image_height = int(image_elem.attrib.get('height', 0))
        return {
            'name': name,
            'tilewidth': tilewidth,
            'tileheight': tileheight,
            'spacing': spacing,
            'margin': margin,
            'image_source': image_source,
            'image_width': image_width,
            'image_height': image_height,
        }

    def get_tile_image(self, group, tileset_name, tile_id):
        """
        Return the PIL image for a specific tile.
        group: 'battle', 'unit', or 'world'
        tileset_name: name of the tileset (e.g. 'farm')
        tile_id: integer tile index
        """
        group_dict = getattr(self, group, None)
        if group_dict is None:
            raise ValueError(f"Unknown group: {group}")

        # Check if the tileset is already loaded
        if tileset_name not in group_dict:
            # Lazy load - find and load the tileset now
            for tsx_path, metadata in self._tileset_metadata.items():
                if metadata['name'] == tileset_name and self._tileset_categories.get(tsx_path) == group:
                    self._load_tileset_on_demand(Path(tsx_path))
                    break

        return group_dict.get(tileset_name, {}).get(tile_id)

    def export_all_images(self, export_folder=None):
        """
        Export all tile images from all categories to a folder in user's Documents/export.
        Images are saved in subfolders: <category>/<tileset>/<tileid>.png
        """
        # First ensure all tilesets are loaded
        for tsx_path in self._tileset_metadata:
            self._load_tileset_on_demand(Path(tsx_path))

        if export_folder is None:
            documents = Path.home() / 'Documents'
            export_folder = documents / 'export'

        # Process each category in parallel
        for category in ['battle', 'unit', 'world']:
            group = getattr(self, category)
            for tileset_name, tiles in group.items():
                tileset_folder = export_folder / category / tileset_name
                tileset_folder.mkdir(parents=True, exist_ok=True)
                for tile_id, img in tiles.items():
                    filename = f"{tile_id:03d}.png"
                    path = tileset_folder / filename
                    img.save(str(path))

        print(f"Exported all images to {export_folder}")

    # Add a method to clear the image cache if memory usage becomes a concern
    def clear_cache(self):
        """Clear the image cache to free up memory"""
        self._image_cache.clear()
        # Also clear the lru_cache for _get_tileset_image
        self._get_tileset_image.cache_clear()
