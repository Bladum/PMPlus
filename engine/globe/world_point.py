class TWorldPoint:
    """
    Represents a position on the world map (tile coordinates).
    Provides utility methods for position handling.
    """
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def to_tuple(self):
        return (self.x, self.y)

    def distance_to(self, other):
        import math
        return math.hypot(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"WorldPoint({self.x}, {self.y})"

