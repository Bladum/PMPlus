class TWorldPoint:
    """
    Represents a position on the world map (tile coordinates).
    Provides utility methods for position handling.
    """
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    @classmethod
    def from_tuple(cls, tuple_pos):
        """Create a WorldPoint from a tuple (x, y)"""
        return cls(tuple_pos[0], tuple_pos[1])

    @classmethod
    def from_iterable(cls, iterable):
        """Create a TWorldPoint from any iterable with two elements (x, y)."""
        x, y = iterable
        return cls(x, y)

    def to_tuple(self):
        return (self.x, self.y)

    def distance_to(self, other):
        import math
        return math.hypot(self.x - other.x, self.y - other.y)

    def manhattan_distance(self, other):
        """Calculate Manhattan distance between two points"""
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"WorldPoint({self.x}, {self.y})"

    def __add__(self, other):
        """Add two points together"""
        return TWorldPoint(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """Subtract one point from another"""
        return TWorldPoint(self.x - other.x, self.y - other.y)

    def scale(self, factor):
        """Scale the point by a factor"""
        return TWorldPoint(self.x * factor, self.y * factor)

    def is_within_bounds(self, width, height):
        """Check if the point is within map boundaries"""
        return 0 <= self.x < width and 0 <= self.y < height

    def midpoint(self, other):
        """Find the midpoint between this point and another"""
        return TWorldPoint((self.x + other.x) // 2, (self.y + other.y) // 2)

    def get_adjacent_points(self):
        """Get the four adjacent points (N, E, S, W)"""
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # N, E, S, W
        return [TWorldPoint(self.x + dx, self.y + dy) for dx, dy in directions]

    def get_adjacent_points_with_diagonals(self):
        """Get all eight adjacent points (including diagonals)"""
        directions = [
            (-1, -1), (0, -1), (1, -1),
            (-1, 0),           (1, 0),
            (-1, 1),  (0, 1),  (1, 1)
        ]
        return [TWorldPoint(self.x + dx, self.y + dy) for dx, dy in directions]

    def round_to_grid(self, grid_size):
        """Round coordinates to the nearest grid position"""
        return TWorldPoint(
            round(self.x / grid_size) * grid_size,
            round(self.y / grid_size) * grid_size
        )
