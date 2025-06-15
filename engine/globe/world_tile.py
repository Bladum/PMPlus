"""
TWorldTile: Represents a single tile on the world map.
Each tile is assigned to a region, may belong to a country, and has a biome.
May also have one or more locations (e.g., cities, bases, crash sites).

Classes:
    TWorldTile: Main class for world map tiles.

Last standardized: 2024-06-11
"""

class TWorldTile:
    """
    Represents a single tile on the world map.
    Each tile is assigned to a region, may belong to a country, and has a biome.
    May also have one or more locations (e.g., cities, bases, crash sites).

    Attributes:
        x (int): X coordinate of the tile.
        y (int): Y coordinate of the tile.
        region_id (int|str|None): Region identifier for this tile.
        country_id (int|str|None): Country identifier for this tile.
        biome_id (int|str|None): Biome identifier for this tile.
        locations (list): List of location IDs or objects present on this tile.
    """
    def __init__(self, x, y, data=None):
        """
        Initialize a TWorldTile instance.

        Args:
            x (int): X coordinate of the tile.
            y (int): Y coordinate of the tile.
            data (dict, optional): Optional dictionary containing initial values for
                region_id, country_id, biome_id, and locations.
        """
        self.x = x
        self.y = y
        self.region_id = None
        self.country_id = None
        self.biome_id = None
        self.locations = []
        if data:
            self.region_id = data.get('region_id', None)
            self.country_id = data.get('country_id', None)
            self.biome_id = data.get('biome_id', None)
            self.locations = data.get('locations', [])

    def __repr__(self):
        """
        Return a string representation of the TWorldTile instance.

        Returns:
            str: Informal string representation of the TWorldTile instance,
            including x, y, region_id, country_id, biome_id, and locations.
        """
        return f"TWorldTile(x={self.x}, y={self.y}, region_id={self.region_id}, country_id={self.country_id}, biome_id={self.biome_id}, locations={self.locations})"
