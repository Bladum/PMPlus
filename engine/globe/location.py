"""
TLocation: Represents a single location on the world map (base, city, crash site, etc.).
Last update: 2025-06-10
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
            data (dict, optional): Dictionary with location properties. Keys:
                - name (str)
                - description (str)
                - position (tuple)
                - initial_cover (int)
                - cover (int)
                - cover_change (int)
        """
        if data is None:
            data = {}
        # Required fields
        self.pid = pid

        self.name = data.get("name", "")
        self.description = data.get("description", "")
        pos = data.get("position", (0, 0))  # Default position (0, 0) if not provided
        self.position = TWorldPoint.from_tuple(pos)

        # Radar detection fields
        self.initial_cover = data.get("initial_cover", 0)  # max cover value
        self.cover = data.get("cover", self.initial_cover)  # current cover
        self.cover_change = data.get("cover_change", 0)  # how much cover recovers per turn
        self.visible = False  # is visible to player

    def update_visibility(self):
        """
        Update the visibility status of the location based on its cover value.
        """
        self.visible = self.cover <= 0

    def replenish_cover(self):
        """
        Replenish the cover value up to the initial maximum, then update visibility.
        """
        if self.cover < self.initial_cover:
            self.cover = min(self.initial_cover, self.cover + self.cover_change)
        self.update_visibility()

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
