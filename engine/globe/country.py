class TCountry:
    """
    Most tiles are owned by a country
    score in his tiles is used to calculate funding of XCOM
    Country may be part or leave XCOM
    """
    def __init__(self, pid, data : dict = {}):
        # Required fields
        self.pid = pid
        self.name = data.get("name", "")

        # Optional fields with defaults
        self.description = data.get("description", "")
        self.color = data.get("color", "#000000")
        self.funding = data.get("funding", 10)
        self.funding_cap = data.get("funding_cap", 500)

        # Lists
        self.service_provided = data.get("service_provided", [])
        self.service_forbidden = data.get("service_forbidden", [])

        # Advanced funding model fields
        self.owned_tiles = data.get("owned_tiles", [])  # list of (x, y) tuples or tile ids
        self.initial_relation = data.get("initial_relation", 5)
        self.relation = self.initial_relation
        self.active = True  # Whether country is still funding XCOM

    def monthly_update(self, month_score):
        """
        Update relation and funding based on monthly score.
        month_score: int, sum of mission results on this country's tiles
        """
        import random
        if not self.active:
            self.funding = 0
            return

        # Relation change
        if month_score > 0:
            chance = min(1.0, (month_score / 1000.0))  # 100 points = 10% chance
            if random.random() < (month_score / 1000.0):
                self.relation = min(9, self.relation + 1)
        elif month_score < 0:
            chance = min(1.0, (abs(month_score) / 500.0))  # 50 points = 10% chance
            if random.random() < (abs(month_score) / 500.0):
                self.relation = max(0, self.relation - 1)

        # Funding adjustment
        if self.relation > 5:
            increase = (self.relation - 5) * 0.05
            self.funding = min(self.funding_cap, int(self.funding * (1 + increase)))
            self.funding = max(self.funding, self.funding_cap)  # minimum is funding cap
        elif self.relation < 5:
            decrease = (5 - self.relation) * 0.05
            self.funding = max(0, int(self.funding * (1 - decrease)))
        # If relation hits 0, country leaves
        if self.relation == 0:
            self.active = False
            self.funding = 0
        # If relation > 0, funding may still reach 0
        if self.relation > 0 and self.funding < 0:
            self.funding = 0

    def add_tile(self, tile_pos):
        if tile_pos not in self.owned_tiles:
            self.owned_tiles.append(tile_pos)

    def remove_tile(self, tile_pos):
        if tile_pos in self.owned_tiles:
            self.owned_tiles.remove(tile_pos)

    def calculate_owned_tiles(self, tiles, width, height):
        """
        Calculate and assign this country's owned tiles based on the world tile grid.
        tiles: 2D array of TWorldTile
        width, height: dimensions of the world
        """
        self.owned_tiles = []
        for y in range(height):
            for x in range(width):
                tile = tiles[y][x]
                if tile.owner_country_id == self.id:
                    self.owned_tiles.append((x, y))
