"""
XCOM Location Module: city.py

Represents a city location on the world map.

Classes:
    TCity: City location with name, size, description, and terrain selection logic.

Last updated: 2025-06-14
"""

from engine.globe.location import TLocation
import random


class TCity(TLocation):
    """
    Represents a city on the world map as a location.
    Inherits from TLocation and adds city-specific attributes.
    """
    def __init__(self, loc_id, data: dict = None):
        """
        Initialize a TCity instance.
        Args:
            loc_id (str): Unique identifier for the city location.
            data (dict, optional): Dictionary with city attributes (size, name, description, terrains).
        """
        if data is None:
            data = {}
        super().__init__(loc_id, data)
        self.size = data.get("size", 4)  # Size of the city (default 4)
        self.name = data.get("name", '')  # Name of the city
        self.description = data.get("description", '')  # Description of the city
        self.terrains = data.get("terrains", {})  # Terrains available in the city

    def get_random_terrain(self):
        """
        Randomly select a terrain for this city based on self.terrains.
        Returns:
            str or None: Selected terrain string, or None if no terrains defined.
        """
        if not self.terrains:
            return None
        if isinstance(self.terrains, dict):
            terrain_keys = list(self.terrains.keys())
            weights = [self.terrains[k] for k in terrain_keys]
            return random.choices(terrain_keys, weights=weights, k=1)[0]
        elif isinstance(self.terrains, list):
            return random.choice(self.terrains)
        return None