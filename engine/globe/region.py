"""
region.py

Defines the TRegion class, representing a region on the world map. Used for mission control, analytics, and region-based gameplay mechanics.

Classes:
    TRegion: Region entity for world map and mission control.

Last standardized: 2025-06-14
"""

from globe.world_tile import TWorldTile


class TRegion:
    """
    TRegion represents a region on the world map. Each tile is assigned to a region.
    Regions are used to control mission locations and provide analytics for score.

    Attributes:
        pid (str|int): Unique region identifier.
        name (str): Name of the region.
        is_land (bool): Whether the region is land.
        tiles (list): List of TWorldTile instances in the region.
        neighbors (list): List of neighboring TRegion instances.
        description (str): Description of the region.
        color (str): Color code for the region.
        mission_weight (int): Weight for mission generation.
        base_cost (int): Cost to build a base in this region.
        service_provided (list): List of services provided.
        service_forbidden (list): List of forbidden services.
    """

    def __init__(self, pid, data: dict = None):
        """
        Initialize a TRegion instance.

        Args:
            pid (str|int): Unique region identifier.
            data (dict, optional): Dictionary with region properties.
        """
        if data is None:
            data = {}
        self.pid = pid
        self.name = data.get("name", "")
        self.is_land = data.get("is_land", False)
        self.tiles: list[TWorldTile] = []
        self.neighbors: list[TRegion] = []
        self.description = data.get("description", "")
        self.color = data.get("color", "#000000")
        self.mission_weight = data.get("mission_weight", 10)
        self.base_cost = data.get("base_cost", 500)
        self.service_provided = data.get("service_provided", [])
        self.service_forbidden = data.get("service_forbidden", [])

    def calculate_region_tiles(self, tiles, width, height, region_neighbors):
        """
        Calculate and assign this region's tiles and neighbors.
        """
        # Find all tiles belonging to this region
        region_tiles = set()
        for y in range(height):
            for x in range(width):
                tile = tiles[y][x]
                if tile.region_id == self.pid:
                    region_tiles.add((x, y))
        # Expand: add all neighboring tiles (8-way)
        expanded = set(region_tiles)
        for x, y in region_tiles:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        expanded.add((nx, ny))
        self.tiles = list(expanded)
        self.neighbors = list(region_neighbors.get(self.pid, []))
