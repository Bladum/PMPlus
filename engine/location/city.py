from engine.globe.location import TLocation
import yaml
from pathlib import Path


# TODO if city is inside a country then it can contain country specific elements e.g. units or tiles

class TCity(TLocation):
    """
    Represents a city on the world map as location
    It is a subclass of TLocation
    It may have a name, size, location, specific terrains
    """
    def __init__(self, loc_id, data : dict = {}):
        super().__init__(loc_id, data)

        self.size = data.get("size", 4)
        self.name = data.get("name", '')
        self.description = data.get("description", '')
        self.terrains = data.get("terrains", {} )

    def get_random_terrain(self):
        """
        Randomly select a terrain for this city based on self.terrains dict of weights.
        Returns a terrain string or None if no terrains defined.
        """
        import random
        if not self.terrains:
            return None
        if isinstance(self.terrains, dict):
            terrain_keys = list(self.terrains.keys())
            weights = [self.terrains[k] for k in terrain_keys]
            return random.choices(terrain_keys, weights=weights, k=1)[0]
        elif isinstance(self.terrains, list):
            return random.choice(self.terrains)
        return None