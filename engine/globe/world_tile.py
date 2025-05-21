class TWorldTile:
    """
    Single tile on world map
    Its assigned to region, can be to country, it has biome
    It may have locations on it
    """
    def __init__(self, x, y, data=None):
        self.x = x
        self.y = y
        self.region_id = None
        self.owner_country_id = None  # country id or None
        self.biome = None
        self.locations = []
        if data:
            self.region_id = data.get('region_id', None)
            self.owner_country_id = data.get('owner_country_id', None)
            self.biome = data.get('biome', None)
            self.locations = data.get('locations', [])

