class WorldPoint:
    """
    Represents a position on the world map (tile coordinates).
    Provides utility methods for position handling.
    """
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    @classmethod
    def from_iterable(cls, pos):
        if isinstance(pos, WorldPoint):
            return pos
        if isinstance(pos, (list, tuple)) and len(pos) == 2:
            return cls(pos[0], pos[1])
        raise ValueError("Invalid position format for WorldPoint")

    def to_tuple(self):
        return (self.x, self.y)

    def distance_to(self, other):
        other = WorldPoint.from_iterable(other)
        import math
        return math.hypot(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        if not isinstance(other, WorldPoint):
            other = WorldPoint.from_iterable(other)
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"WorldPoint({self.x}, {self.y})"

