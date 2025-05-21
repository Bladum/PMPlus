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
    type: e.g. 'eliminate', 'escape', 'hold', 'defend', 'rescue', etc.
    params: dict with details (unit ids, tile coords, turns, etc.)
    status: 'incomplete', 'complete', 'failed'
    """
    def __init__(self, obj_type: str, params: dict[str, Any]):
        self.type = obj_type
        self.params = params
        self.status = 'incomplete'
        self.progress = 0  # For objectives with progress (e.g. explore %)

    def check_status(self, battle):
        # Dispatch to specific check method based on type
        method = getattr(self, f'_check_{self.type}', None)
        if method:
            method(battle)
        else:
            self.status = 'incomplete'  # Unknown type

    # --- CORE OBJECTIVES ---
    def _check_eliminate(self, battle):
        # Defeat all enemy units
        enemies = battle.find_units(side=battle.SIDE_ENEMY, alive=True)
        if not enemies:
            self.status = 'complete'
        else:
            self.status = 'incomplete'

    def _check_escape(self, battle):
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
        # Survive for specified number of turns
        turns = self.params.get('turns', 10)
        if battle.turn >= turns:
            self.status = 'complete'
        else:
            self.status = 'incomplete'

    def _check_blitz(self, battle):
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
        # Prevent enemies from capturing marked POC
        poc_tiles = battle.find_tiles(objective_marker='poc')
        for (x, y, tile) in poc_tiles:
            if tile.unit and tile.unit.side == battle.SIDE_ENEMY:
                self.status = 'failed'
                return
        self.status = 'complete'

    def _check_conquer(self, battle):
        # Conquer marked POC from enemy forces
        poc_tiles = battle.find_tiles(objective_marker='poc')
        for (x, y, tile) in poc_tiles:
            if not tile.unit or tile.unit.side != battle.SIDE_PLAYER:
                self.status = 'incomplete'
                return
        self.status = 'complete'

    def _check_explore(self, battle):
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
        # Eliminate specific units
        hunt_ids = self.params.get('unit_ids', [])
        alive = [unit for unit in battle.find_units(unit_ids=hunt_ids, alive=True)]
        self.progress = len(hunt_ids) - len(alive)
        if not alive:
            self.status = 'complete'
        else:
            self.status = 'incomplete'

    def _check_recon(self, battle):
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
        # Protect moving target as it travels across the map
        escort_ids = self.params.get('unit_ids', [])
        alive = [unit for unit in battle.find_units(unit_ids=escort_ids, alive=True)]
        self.progress = len(alive)
        if len(alive) == len(escort_ids):
            self.status = 'complete'
        else:
            self.status = 'incomplete'

    def _check_ambush(self, battle):
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

