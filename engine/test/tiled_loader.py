"""
Tiled Map Loader for XCOM game
Handles loading Tiled TMX files and extracting layer data
"""

import os
import pytmx
from pytmx.util_pygame import load_pygame

class TiledMap:
    def __init__(self, filename):
        """
        Load a TMX file using pytmx

        Args:
            filename: Path to the TMX file
        """
        self.path = filename
        self.tmx_data = load_pygame(filename)

        # Store layers by name for easy access
        self.layers = {}
        self.floor_tiles = []
        self.wall_tiles = []
        self.roof_tiles = []

        # Process and organize layers
        self._process_layers()

    def _process_layers(self):
        """Extract and organize tile data from the TMX layers"""
        # First, categorize all layers
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, 'name'):
                self.layers[layer.name] = layer

        # Process specific layers we're interested in
        self._extract_layer_tiles('floor', self.floor_tiles)
        self._extract_layer_tiles('wall', self.wall_tiles)
        self._extract_layer_tiles('roof', self.roof_tiles)

    def _extract_layer_tiles(self, layer_name, target_list):
        """
        Extract tile information from a specific layer

        Args:
            layer_name: Name of the layer to process
            target_list: List to store the extracted tile data
        """
        if layer_name in self.layers:
            layer = self.layers[layer_name]
            for x, y, gid in layer:
                if gid:  # Skip empty tiles (gid == 0)
                    # Get tile properties
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    props = self.tmx_data.get_tile_properties_by_gid(gid) or {}

                    # Store tile data
                    tile_data = {
                        'x': x,
                        'y': y,
                        'gid': gid,
                        'image': tile,
                        'properties': props
                    }
                    target_list.append(tile_data)

    def get_tile_properties(self, x, y, layer_name):
        """
        Get properties of a specific tile

        Args:
            x: Tile X coordinate
            y: Tile Y coordinate
            layer_name: Name of the layer

        Returns:
            Dictionary of tile properties or None if not found
        """
        if layer_name in self.layers:
            gid = self.layers[layer_name].toml_data[y][x]
            if gid:
                return self.tmx_data.get_tile_properties_by_gid(gid)
        return None

    def get_layer_data(self, layer_name):
        """
        Get all tile data for a specific layer

        Args:
            layer_name: Name of the layer

        Returns:
            List of tiles or empty list if layer doesn't exist
        """
        if layer_name == 'floor':
            return self.floor_tiles
        elif layer_name == 'wall':
            return self.wall_tiles
        elif layer_name == 'roof':
            return self.roof_tiles
        return []

    def get_map_size(self):
        """
        Get the dimensions of the map

        Returns:
            Tuple of (width, height) in tiles
        """
        return self.tmx_data.width, self.tmx_data.height

    def get_tile_size(self):
        """
        Get the dimensions of a single tile

        Returns:
            Tuple of (width, height) in pixels
        """
        return self.tmx_data.tilewidth, self.tmx_data.tileheight

# Example usage:
if __name__ == "__main__":
    # Replace with the path to your TMX file
    tmx_file = "MOD/maps/urban/example_map.tmx"

    if os.path.exists(tmx_file):
        tiled_map = TiledMap(tmx_file)
        print(f"Map size: {tiled_map.get_map_size()}")
        print(f"Tile size: {tiled_map.get_tile_size()}")
        print(f"Floor tiles: {len(tiled_map.floor_tiles)}")
        print(f"Wall tiles: {len(tiled_map.wall_tiles)}")
        print(f"Roof tiles: {len(tiled_map.roof_tiles)}")
    else:
        print(f"Error: Map file not found at {tmx_file}")
