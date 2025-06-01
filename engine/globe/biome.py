class TBiome:
    """
    Each tile on worls map is assigned to a biome like forest, desert, ocean
    Biomes are used to generate battle with specific terrain type
    """
    def __init__(self, pid, data : dict = {}):
        self.pid = pid

        # Required fields
        self.name = data.get("name", "")

        # Optional fields with defaults
        self.description = data.get("description", "")
        self.image = data.get("sprite", None)
        self.type = data.get("type", 'land')
        self.terrains = data.get("terrains", {})

    def get_random_terrain(self):
        """
        Randomly select a terrain for this biome based on weights in self.terrains.
        Returns the terrain key (str) or None if no terrains defined.
        """
        import random
        if not self.terrains:
            return None
        terrain_keys = list(self.terrains.keys())
        weights = [self.terrains[k] for k in terrain_keys]
        return random.choices(terrain_keys, weights=weights, k=1)[0]

