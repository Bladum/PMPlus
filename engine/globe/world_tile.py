class TWorldTile:
    """
    TWorldTile represents a single tile on the world map.
    Each tile is assigned to a region, may belong to a country, and has a biome.
    It may also have one or more locations (e.g., cities, bases, crash sites).

    Attributes:
        x (int): X coordinate of the tile.
        y (int): Y coordinate of the tile.
        region_id (int|str|None): Region identifier for this tile.
        country_id (int|str|None): Country identifier for this tile.
        biome_id (int|str|None): Biome identifier for this tile.
        locations (list): List of location IDs or objects present on this tile.
    """
    def __init__(self, x, y, data=None):
        self.x = x
        self.y = y

        self.region_id = None
        self.country_id = None  # country id or None
        self.biome_id = None
        self.locations = []

        if data:
            self.region_id = data.get('region_id', None)
            self.country_id = data.get('country_id', None)
            self.biome_id = data.get('biome_id', None)
            self.locations = data.get('locations', [])

    def __repr__(self):
        return f"TWorldTile(x={self.x}, y={self.y}, region_id={self.region_id}, country_id={self.country_id}, biome_id={self.biome_id}, locations={self.locations})"
