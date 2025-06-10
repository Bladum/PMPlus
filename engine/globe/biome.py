"""
TBiome: Represents a biome type assigned to each tile on the world map.
Last update: 2025-06-10
"""

class TBiome:
    '''
    TBiome represents a biome type assigned to each tile on the world map (e.g., forest, desert, ocean).
    Biomes are used to generate battles with specific terrain types.

    Attributes:
        pid (str|int): Unique biome identifier.
        name (str): Name of the biome.
        description (str): Description of the biome.
        image (str|None): Sprite/image reference for the biome.
        type (str): Type of biome ('land', 'water', etc.).
        terrains (dict): Mapping of terrain keys to weights for random selection.
    '''
    def __init__(self, pid, data: dict = None):
        """
        Initialize a TBiome instance.

        Args:
            pid (str|int): Unique biome identifier.
            data (dict, optional): Dictionary with biome properties. Keys:
                - name (str)
                - description (str)
                - sprite (str|None)
                - type (str)
                - terrains (dict)
        """
        if data is None:
            data = {}
        self.pid = pid
        self.name = data.get("name", "")
        self.description = data.get("description", "")
        self.image = data.get("sprite", None)
        self.type = data.get("type", 'land')
        self.terrains = data.get("terrains", {})

    def get_random_terrain(self):
        """
        Randomly select a terrain for this biome based on weights in self.terrains.
        Returns:
            str|None: The selected terrain key, or None if no terrains defined.
        """
        import random
        if not self.terrains:
            return None
        terrain_keys = list(self.terrains.keys())
        weights = [self.terrains[k] for k in terrain_keys]
        return random.choices(terrain_keys, weights=weights, k=1)[0]
