"""
TCountry: Represents a country on the world map, manages funding and relations with XCOM.
Last update: 2025-06-10
"""



class TCountry:
    '''
    TCountry represents a country that owns tiles on the world map.
    The country's score is used to calculate XCOM's funding, and countries can join or leave XCOM.

    Attributes:
        pid (str|int): Unique country identifier.
        name (str): Name of the country.
        description (str): Description of the country.
        color (str): Color code for the country.
        funding (int): Current funding provided by the country.
        funding_cap (int): Maximum funding the country can provide.
        service_provided (list): List of services provided.
        service_forbidden (list): List of forbidden services.
        owned_tiles (list): List of (x, y) tuples or tile ids owned by the country.
        initial_relation (int): Initial relation value.
        relation (int): Current relation value.
        active (bool): Whether the country is still funding XCOM.
    '''
    def __init__(self, pid, data: dict = None):
        """
        Initialize a TCountry instance.

        Args:
            pid (str|int): Unique country identifier.
            data (dict, optional): Dictionary with country properties. Keys:
                - name (str)
                - description (str)
                - color (str)
                - funding (int)
                - funding_cap (int)
                - service_provided (list)
                - service_forbidden (list)
                - owned_tiles (list)
                - initial_relation (int)
        """
        if data is None:
            data = {}
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
        Args:
            month_score (int): Sum of mission results on this country's tiles.
        """
        import random
        if not self.active:
            self.funding = 0
            return
        # Relation change
        if month_score > 0:
            chance = min(1.0, (month_score / 1000.0))  # 100 points = 10% chance
            if random.random() < chance:
                self.relation = min(9, self.relation + 1)
        elif month_score < 0:
            chance = min(1.0, (abs(month_score) / 500.0))  # 50 points = 10% chance
            if random.random() < chance:
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
        """
        Add a tile to the country's owned tiles.
        Args:
            tile_pos (tuple): (x, y) position or tile id.
        """
        if tile_pos not in self.owned_tiles:
            self.owned_tiles.append(tile_pos)

    def remove_tile(self, tile_pos):
        """
        Remove a tile from the country's owned tiles.
        Args:
            tile_pos (tuple): (x, y) position or tile id.
        """
        if tile_pos in self.owned_tiles:
            self.owned_tiles.remove(tile_pos)

    def calculate_owned_tiles(self, tiles=None):
        """
        Calculate and assign this country's owned tiles based on the world tile grid.
        Args:
            tiles (list): 2D array of TWorldTile.
        """
        self.owned_tiles = []
        if tiles is None:
            return
        for row in tiles:
            for tile in row:
                if hasattr(tile, 'country_id') and tile.country_id == self.pid:
                    self.owned_tiles.append((tile.x, tile.y))