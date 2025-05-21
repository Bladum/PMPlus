class TTerrain:
    """
    Represents a terrain type, it is used to generate map for battle
    Each terrain may be linked with BIOME or be separated
    Terrain has list of map blocks and map script used to generate battle map
    """
    def __init__(self, terrain_id, data):
        self.id = terrain_id
        self.name = data.get('name', terrain_id)
        self.description = data.get('description', '')
        self.tileset = data.get('tileset', '')
        self.script = data.get('script', None)
        self.units_civilian = data.get('units_civilian', [])
        self.map_blocks = []  # Will be filled later

        # Process map blocks (these are at the top level in array format)
        map_blocks = []
        for map_block in data.get('map_blocks', []):
            if map_block:
                map_blocks.append(TMapBlockEntry(map_block))

        self.map_blocks = map_blocks