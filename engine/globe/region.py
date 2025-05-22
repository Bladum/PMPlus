class TRegion:
    """
    Each tile on worls map is assigned to a region
    Regions are used to control location of missions
    Regions have analytics for score
    """

    def __init__(self, pid, data : dict = {}):
        # Required fields
        self.pid = pid
        self.name = data.get("name", "")
        self.is_land = data.get("is_land", False)

        # Optional fields with defaults
        self.description = data.get("description", "")
        self.color = data.get("color", "#000000")
        self.mission_weight = data.get("mission_weight", 10)
        self.base_cost = data.get("base_cost", 500)

        # Lists
        self.service_provided = data.get("service_provided", [])
        self.service_forbidden = data.get("service_forbidden", [])

    def calculate_region_tiles(self, tiles, width, height, region_neighbors):
        """
        Calculate and assign this region's tiles and neighbors.
        tiles: 2D array of TWorldTile
        width, height: dimensions of the world
        region_neighbors: dict of region_id -> set of neighbor region_ids
        """
        # Find all tiles belonging to this region
        region_tiles = set()
        for y in range(height):
            for x in range(width):
                tile = tiles[y][x]
                if tile.region_id == self.id:
                    region_tiles.add((x, y))
        # Expand: add all neighboring tiles (8-way)
        expanded = set(region_tiles)
        for x, y in region_tiles:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        expanded.add((nx, ny))
        self.region_tiles = list(expanded)
        self.neighbors = list(region_neighbors.get(self.id, []))

