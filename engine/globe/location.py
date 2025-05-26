from engine.globe.world_point import TWorldPoint

class TLocation:
    """
    Single location on world map, it could be a base, a city, a UFO crash site
    it may or may not be detected by xcom
    """
    def __init__(self, pid,  data : dict = {}):
        # Required fields
        self.pid = pid

        self.name = data.get("name", "")
        self.description = data.get("description", "")
        pos = data.get("position", [])
        self.position = TWorldPoint(pos[0], pos[1]) if pos else TWorldPoint(0, 0)

        # Radar detection fields
        self.initial_cover = data.get("initial_cover", 0)  # max cover value
        self.cover = data.get("cover", self.initial_cover)  # current cover
        self.cover_change = data.get("cover_change", 0)  # how much cover recovers per turn
        self.visible = False  # is visible to player

    def update_visibility(self):
        self.visible = self.cover <= 0

    def replenish_cover(self):
        if self.cover < self.initial_cover:
            self.cover = min(self.initial_cover, self.cover + self.cover_change)
        self.update_visibility()

    def get_position(self):
        """
        Returns the position of the location as a WorldPoint.
        """
        return self.position

    def distance_to(self, other):
        """
        Returns the Euclidean distance to another TLocation or WorldPoint or (x, y) tuple.
        """
        if isinstance(other, TLocation):
            other = other.get_position()
        return self.position.distance_to(other)
