"""
abase.py

Defines the TBaseAlien class, representing an alien base on the world map as a location. Implements growth, mission generation, and scoring logic for alien bases.

Classes:
    TBaseAlien: Alien base location and mission logic.

Last standardized: 2025-06-14
"""

from globe.location import TLocation


class TBaseAlien(TLocation):
    """
    Represents an alien base on the world map as a location.
    Handles base growth, mission generation, and scoring logic for alien bases.

    Attributes:
        level (int): Current level of the base (starts at 1).
        level_max (int): Maximum level the base can reach.
        level_up_pending (bool): Whether a level up is pending (after supply mission).
        month_progress (int): Days since last mission cycle (resets monthly).
        missions_this_month (int): Number of missions launched this month.
        supply_pending (bool): Whether a supply mission is pending (triggers growth).
        score_per_day (int): Score penalty per day for XCOM, per base level.
        units_per_level (dict): Number of units per base level.
        map_size_per_level (dict): Map size per base level.
        max_missions_per_month (dict): Max missions per month per level.
        days_in_month (int): Number of days in a month (for mission planning).
        missions_types (list): List of possible mission types.
        region_id: Region identifier for the base.
        pending_missions (list): Missions to be launched this month.
        game: Reference to the game object.
    """
    def __init__(self, pid, data : dict = {}):
        """
        Initialize an alien base at a world location.

        Args:
            pid: Unique base identifier.
            data (dict): Dictionary with base properties (location, name, etc).
        """
        super().__init__( pid, data )

        from engine.engine.game import TGame
        self.game = TGame()

        self.level = 1  # Always starts at level 1
        self.level_max = 4
        self.level_up_pending = False
        self.month_progress = 0  # Days since last mission cycle
        self.missions_this_month = 0
        self.supply_pending = False
        self.score_per_day = 5  # Per level
        self.units_per_level = {1: 20, 2: 30, 3: 40, 4: 50}
        self.map_size_per_level = {1: 4, 2: 5, 3: 6, 4: 7}
        self.max_missions_per_month = {1: 1, 2: 2, 3: 3, 4: 4}
        self.days_in_month = 30
        self.missions_types = [
            'research', 'supply', 'hunt', 'infiltration', 'retaliation', 'create_base'
        ]
        self.region_id = getattr(self, 'region_id', None)
        self.pending_missions = []  # Missions to be launched this month

    def tick_day(self):
        """
        Advance base logic by one day. Handles score penalty, mission planning, supply, and growth.
        Should be called once per in-game day.
        """
        # Score penalty for XCOM
        if hasattr(self.game, 'score'):
            self.game.score -= self.level * self.score_per_day
        # Progress month
        self.month_progress += 1
        # Supply mission logic: if pending, try to grow
        if self.supply_pending:
            self.try_grow()
            self.supply_pending = False
        # Every month, plan missions
        if self.month_progress >= self.days_in_month:
            self.plan_monthly_missions(self.game)
            self.month_progress = 0
            self.missions_this_month = 0

    def plan_monthly_missions(self):
        """
        Plan missions for this month based on base level.
        Always includes a supply mission, and randomly selects other mission types.
        Populates self.pending_missions and launches them.
        """
        num_missions = self.max_missions_per_month.get(self.level, 1)
        self.pending_missions = []
        # Always include supply mission
        self.pending_missions.append('supply')
        # Add other missions (randomly pick from types, can be improved)
        import random
        other_types = [t for t in self.missions_types if t != 'supply']
        for _ in range(num_missions - 1):
            self.pending_missions.append(random.choice(other_types))
        # Launch missions (stub: integrate with campaign/mission system)
        for mission_type in self.pending_missions:
            self.launch_mission(mission_type, self.game)

    def launch_mission(self, mission_type, game):
        """
        Launch a mission of the given type. Integrate with campaign/mission system.

        Args:
            mission_type (str): Type of mission to launch.
            game: Reference to the game object.
        """
        if mission_type == 'supply':
            self.supply_pending = True  # If not intercepted, will grow next month
        # TODO: Integrate with actual mission/campaign logic
        # print(f"Alien base at {self.loc_id} launches {mission_type} mission.")

    def try_grow(self):
        """
        If supply mission was not intercepted, grow base by 1 level (up to max).
        """
        if self.level < self.level_max:
            self.level += 1

    def get_battle_map_size(self):
        """
        Returns the map size for battles at this base, based on current level.

        Returns:
            int: Map size (width/height in blocks).
        """
        return self.map_size_per_level.get(self.level, 4)

    def get_units_count(self):
        """
        Returns the number of units present at this base, based on current level.

        Returns:
            int: Number of units.
        """
        return self.units_per_level.get(self.level, 20)

    def get_score_penalty(self):
        """
        Returns the daily score penalty for XCOM caused by this base.

        Returns:
            int: Score penalty per day.
        """
        return self.level * self.score_per_day

    def get_missions_per_month(self):
        """
        Returns the number of missions this base can launch per month.

        Returns:
            int: Number of missions per month.
        """
        return self.max_missions_per_month.get(self.level, 1)

    def get_battle_levels(self):
        """
        Returns the number of battle levels (always 2: surface and underground).

        Returns:
            int: Number of battle levels (2).
        """
        return 2
