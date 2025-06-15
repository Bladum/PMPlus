"""
TBattleObjective: Represents a single mission objective for the battle (eliminate, escape, defend, rescue, etc.).

Encapsulates the type, parameters, status, and progress of an objective, and provides methods to check completion based on battle state.

Classes:
    TBattleObjective: Main class for battle mission objectives.

Last standardized: 2025-06-14
"""

from typing import Any

OBJECTIVE_TYPES = [
    # Core
    "eliminate",
    "escape",
    # Time Limited
    "hold",
    "blitz",
    # Territory
    "defend",
    "conquer",
    "explore",
    # Unit-based
    "rescue",
    "capture",
    "hunt",
    "recon",
    "protect",
    # Object-based
    "sabotage",
    "retrieve",
    # Other
    "escort",
    "ambush",
]

class TBattleObjective:
    """
    Represents a single mission objective for the battle.

    Attributes:
        type (str): Objective type identifier (e.g. 'eliminate', 'escape', etc.).
        params (dict): Dictionary with objective parameters (unit ids, tile coords, turns, etc.).
        status (str): 'incomplete', 'complete', or 'failed'.
        progress (int): Progress value for objectives with progress (e.g. explore %).
    """
    def __init__(self, pid, data = {}):
        """
        Initialize a TBattleObjective instance with type and parameters.

        Args:
            pid (str): Objective type identifier.
            data (dict, optional): Dictionary with objective parameters.
        """
        self.type = pid
        self.params = data
        self.status = 'incomplete'
        self.progress = 0  # For objectives with progress (e.g. explore %)

    def check_status(self, battle):
        """
        Dispatch to the specific check method for this objective type, updating status and progress.
        Args:
            battle: The current battle instance.
        """
        # Dispatch to specific check method based on type
        method = getattr(self, f'_check_{self.type}', None)
        if method:
            method(battle)
        else:
            self.status = 'incomplete'  # Unknown type

    # --- CORE OBJECTIVES ---
    def _check_eliminate(self, battle):
        """
        Check if all enemy units have been eliminated.
        Args:
            battle: The current battle instance.
        """
        # Defeat all enemy units
        enemies = battle.find_units(side=battle.SIDE_ENEMY, alive=True)
        if not enemies:
            self.status = 'complete'
        else:
            self.status = 'incomplete'

    def _check_escape(self, battle):
        """
        Check if escape objective is complete.
        Args:
            battle: The current battle instance.
        """
        # Move all player units to extraction point(s)
        extraction_tiles = battle.find_tiles(objective_marker='extraction')
        player_units = battle.find_units(side=battle.SIDE_PLAYER, alive=True)
        if not player_units:
            self.status = 'failed'
            return
        all_extracted = all(any((unit.x, unit.y) == (x, y) for (x, y, _) in extraction_tiles) for unit in player_units)
        self.status = 'complete' if all_extracted else 'incomplete'

    # --- TIME LIMITED OBJECTIVES ---
    def _check_hold(self, battle):
        """
        Check if hold objective is complete.
        Args:
            battle: The current battle instance.
        """
        # Survive for specified number of turns
        turns = self.params.get('turns', 10)
        if battle.turn >= turns:
            self.status = 'complete'
        else:
            self.status = 'incomplete'

    def _check_blitz(self, battle):
        """
        Check if blitz objective is complete.
        Args:
            battle: The current battle instance.
        """
        # Eliminate all enemies before time limit
        turns = self.params.get('turns', 10)
        enemies = battle.find_units(side=battle.SIDE_ENEMY, alive=True)
        if not enemies and battle.turn <= turns:
            self.status = 'complete'
        elif battle.turn > turns and enemies:
            self.status = 'failed'
        else:
            self.status = 'incomplete'

    # --- TERRITORY OBJECTIVES ---
    def _check_defend(self, battle):
        """
        Check if defend objective is complete.
        Args:
            battle: The current battle instance.
        """
        # Prevent enemies from capturing marked POC
        poc_tiles = battle.find_tiles(objective_marker='poc')
        for (x, y, tile) in poc_tiles:
            if tile.unit and tile.unit.side == battle.SIDE_ENEMY:
                self.status = 'failed'
                return
        self.status = 'complete'

    def _check_conquer(self, battle):
        """
        Check if conquer objective is complete.
        Args:
            battle: The current battle instance.
        """
        # Conquer marked POC from enemy forces
        poc_tiles = battle.find_tiles(objective_marker='poc')
        for (x, y, tile) in poc_tiles:
            if not tile.unit or tile.unit.side != battle.SIDE_PLAYER:
                self.status = 'incomplete'
                return
        self.status = 'complete'

    def _check_explore(self, battle):
        """
        Check if explore objective is complete.
        Args:
            battle: The current battle instance.
        """
        # Reveal specified percentage of the map
        percent = self.params.get('percent', 80)
        total = battle.width * battle.height
        visible = sum(1 for row in battle.tiles for tile in row if tile.fog_of_war and any(fw > 0 for fw in tile.fog_of_war))
        self.progress = int(visible / total * 100)
        if self.progress >= percent:
            self.status = 'complete'
        else:
            self.status = 'incomplete'

    # --- UNIT-BASED OBJECTIVES ---
    def _check_rescue(self, battle):
        """
        Check if rescue objective is complete.
        Args:
            battle: The current battle instance.
        """
        # Locate friendly units and escort to extraction
        rescue_ids = self.params.get('unit_ids', [])
        extraction_tiles = battle.find_tiles(objective_marker='extraction')
        rescued = 0
        for unit in battle.find_units(unit_ids=rescue_ids, alive=True):
            if any((unit.x, unit.y) == (x, y) for (x, y, _) in extraction_tiles):
                rescued += 1
        self.progress = rescued
        if rescued == len(rescue_ids):
            self.status = 'complete'
        else:
            self.status = 'incomplete'

    def _check_capture(self, battle):
        """
        Check if capture objective is complete.
        Args:
            battle: The current battle instance.
        """
        # Capture alive specific units
        capture_ids = self.params.get('unit_ids', [])
        captured = 0
        for unit in battle.find_units(unit_ids=capture_ids, alive=True):
            if getattr(unit, 'is_captured', False):
                captured += 1
        self.progress = captured
        if captured == len(capture_ids):
            self.status = 'complete'
        else:
            self.status = 'incomplete'

    def _check_hunt(self, battle):
        """
        Check if hunt objective is complete.
        Args:
            battle: The current battle instance.
        """
        # Eliminate specific units
        hunt_ids = self.params.get('unit_ids', [])
        alive = [unit for unit in battle.find_units(unit_ids=hunt_ids, alive=True)]
        self.progress = len(hunt_ids) - len(alive)
        if not alive:
            self.status = 'complete'
        else:
            self.status = 'incomplete'

    def _check_recon(self, battle):
        """
        Check if recon objective is complete.
        Args:
            battle: The current battle instance.
        """
        # Identify/mark specific enemy units without engaging
        recon_ids = self.params.get('unit_ids', [])
        seen = 0
        for unit in battle.find_units(unit_ids=recon_ids, alive=True):
            if getattr(unit, 'is_spotted', False):
                seen += 1
        self.progress = seen
        if seen == len(recon_ids):
            self.status = 'complete'
        else:
            self.status = 'incomplete'

    def _check_protect(self, battle):
        """
        Check if protect objective is complete.
        Args:
            battle: The current battle instance.
        """
        # Ensure specific units survive the mission
        protect_ids = self.params.get('unit_ids', [])
        alive = [unit for unit in battle.find_units(unit_ids=protect_ids, alive=True)]
        self.progress = len(alive)
        if len(alive) == len(protect_ids):
            self.status = 'complete'
        else:
            self.status = 'incomplete'

    # --- OBJECT-BASED OBJECTIVES ---
    def _check_sabotage(self, battle):
        """
        Check if sabotage objective is complete.
        Args:
            battle: The current battle instance.
        """
        # Destroy designated objects
        obj_ids = self.params.get('object_ids', [])
        destroyed = 0
        for obj in battle.find_objects(object_ids=obj_ids):
            if getattr(obj, 'is_destroyed', False):
                destroyed += 1
        self.progress = destroyed
        if destroyed == len(obj_ids):
            self.status = 'complete'
        else:
            self.status = 'incomplete'

    def _check_retrieve(self, battle):
        """
        Check if retrieve objective is complete.
        Args:
            battle: The current battle instance.
        """
        # Collect designated objects
        obj_ids = self.params.get('object_ids', [])
        collected = 0
        for obj in battle.find_objects(object_ids=obj_ids):
            if getattr(obj, 'is_collected', False):
                collected += 1
        self.progress = collected
        if collected == len(obj_ids):
            self.status = 'complete'
        else:
            self.status = 'incomplete'

    # --- OTHER OBJECTIVES ---
    def _check_escort(self, battle):
        """
        Check if escort objective is complete.
        Args:
            battle: The current battle instance.
        """
        # Protect moving target as it travels across the map
        escort_ids = self.params.get('unit_ids', [])
        alive = [unit for unit in battle.find_units(unit_ids=escort_ids, alive=True)]
        self.progress = len(alive)
        if len(alive) == len(escort_ids):
            self.status = 'complete'
        else:
            self.status = 'incomplete'

    def _check_ambush(self, battle):
        """
        Check if ambush objective is complete.
        Args:
            battle: The current battle instance.
        """
        # Set up position and eliminate enemy patrol/convoy
        ambush_ids = self.params.get('unit_ids', [])
        eliminated = 0
        for unit in battle.find_units(unit_ids=ambush_ids, alive=False):
            eliminated += 1
        self.progress = eliminated
        if eliminated == len(ambush_ids):
            self.status = 'complete'
        else:
            self.status = 'incomplete'

