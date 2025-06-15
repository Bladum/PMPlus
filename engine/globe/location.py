"""
location.py

Defines the TLocation class, representing a single location on the world map (base, city, crash site, etc.). Handles radar detection, visibility, and cover mechanics for world map locations.

Classes:
    TLocation: World map location entity.

Last standardized: 2025-06-14
"""

from engine.globe.world_point import TWorldPoint

class TLocation:
    """
    TLocation represents a single location on the world map, such as a base, city, or UFO crash site.
    Locations may or may not be detected by XCOM, depending on radar coverage.

    Attributes:
        pid (str|int): Unique location identifier.
        name (str): Name of the location.
        description (str): Description of the location.
        position (TWorldPoint): Position of the location on the world map.
        initial_cover (int): Maximum cover value (for radar detection).
        cover (int): Current cover value.
        cover_change (int): Amount of cover recovered per turn.
        visible (bool): Whether the location is visible to the player.
    """
    def __init__(self, pid,  data: dict = None):
        """
        Initialize a TLocation instance.

        Args:
            pid (str|int): Unique location identifier.
            data (dict, optional): Dictionary with location properties.
        """
        if data is None:
            data = {}
        self.pid = pid
        self.name = data.get("name", "")
        self.description = data.get("description", "")
        pos = data.get("position", (0, 0))
        self.position = TWorldPoint.from_tuple(pos)
        self.initial_cover = data.get("initial_cover", 0)
        self.cover = data.get("cover", self.initial_cover)
        self.cover_change = data.get("cover_change", 0)
        self.visible = False

    def update_visibility(self):
        """
        Update the visibility status of the location based on its cover value.
        """
        self.visible = self.cover <= 0

    def replenish_cover(self):
        """
        Replenish the cover value for the location by cover_change amount.
        """
        self.cover = min(self.initial_cover, self.cover + self.cover_change)

    def get_position(self):
        """
        Returns the position of the location as a TWorldPoint.
        """
        return self.position

    def distance_to(self, other):
        """
        Returns the Euclidean distance to another TLocation, TWorldPoint, or (x, y) tuple.

        Args:
            other: TLocation, TWorldPoint, or (x, y) tuple.

        Returns:
            float: Euclidean distance.
        """
        if isinstance(other, TLocation):
            other = other.get_position()
        return self.position.distance_to(other)
