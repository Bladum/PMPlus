"""
TBattle: Main battle state and logic manager.

Represents a battle instance created by a mission. Manages all units, map tiles, items, effects, sides, turns, fog of war, and objectives. Responsible for the core battle state, including map generation, unit management, turn processing, and objective tracking.

Classes:
    TBattle: Main class for battle state and logic.

Last standardized: 2025-06-14
"""

from engine.battle.battle_generator import TBattleGenerator
from engine.battle.battle_tile import TBattleTile
from engine.unit.unit import TUnit
from engine.battle.objective import TBattleObjective


class TBattle:
    """
    Represents a battle, created by a mission.
    Holds all units, map tiles, items, effects, and manages battle sides and turns.

    Attributes:
        SIDE_PLAYER (int): Player side identifier.
        SIDE_ENEMY (int): Enemy side identifier.
        SIDE_ALLY (int): Ally side identifier.
        SIDE_NEUTRAL (int): Neutral side identifier.
        NUM_SIDES (int): Number of sides in the battle.
        DIPLOMACY (list): Diplomacy matrix for side interactions.
        tiles (list[list[TBattleTile]]): 2D array of battle map tiles.
        width (int): Width of the battle map.
        height (int): Height of the battle map.
        sides (list[list[TUnit]]): List of units for each side.
        fog_of_war (list): Fog of war state for each tile and side.
        current_side (int): Currently active side.
        turn (int): Current turn number.
        objectives (list[TBattleObjective]): List of mission objectives.
    """
    SIDE_PLAYER = 0
    SIDE_ENEMY = 1
    SIDE_ALLY = 2
    SIDE_NEUTRAL = 3
    NUM_SIDES = 4
    # Diplomacy matrix: [attacker][target] = action
    # 0 = ignore, 1 = hostile, 2 = opportunistic, -1 = protect
    DIPLOMACY = [
        [0, 1, 0, 0],   # 0: Player
        [1, 0, 1, 2],   # 1: Enemy
        [0, 1, 0, -1],  # 2: Ally
        [0, 2, -1, 0],  # 3: Neutral
    ]

    def __init__(self, generator: TBattleGenerator):
        """
        Initialize a TBattle instance with a battle map generator.

        Args:
            generator (TBattleGenerator): Generator for creating the battle map and initial state.
        """
        # Generate the battle map (2D list of TBattleTile)
        self.tiles: list[list[TBattleTile]] = generator.generate()
        self.width = len(self.tiles[0]) if self.tiles else 0
        self.height = len(self.tiles)

        # Each tile may have fire/smoke/gas, light, fog of war
        # (Already handled in TBattleTile)

        # Sides: each has a list of units
        self.sides: list[list[TUnit]] = [[] for _ in range(self.NUM_SIDES)]

        # Fog of war: 3 states per tile per side (0=hidden, 1=partial, 2=full)
        self.fog_of_war = [[[0 for _ in range(self.width)] for _ in range(self.height)] for _ in range(self.NUM_SIDES)]

        # Turn/side management
        self.current_side = self.SIDE_PLAYER
        self.turn = 1

        # Mission objectives
        self.objectives: list[TBattleObjective] = []

    def add_unit(self, unit: TUnit, side: int, x: int, y: int):
        """
        Add a unit to the battle at the specified side and coordinates.
        Args:
            unit (TUnit): The unit to add.
            side (int): Side identifier.
            x (int): X coordinate.
            y (int): Y coordinate.
        """
        self.sides[side].append(unit)
        self.tiles[y][x].unit = unit
        unit.x = x
        unit.y = y
        unit.side = side

    def process_turn(self):
        """
        Process the current turn, handling all side and unit actions.
        """
        for side in range(self.NUM_SIDES):
            self.process_side(side)
        self.turn += 1

    def process_side(self, side: int):
        """
        Process all actions for a given side during their turn.
        Args:
            side (int): Side identifier.
        """
        for unit in self.sides[side]:
            self.process_unit(unit)

    def process_unit(self, unit: TUnit):
        """
        Process actions for a single unit during its side's turn.
        Args:
            unit (TUnit): The unit to process.
        """
        # Placeholder: implement AI, player input, etc.
        pass

    def update_fog_of_war(self):
        """
        Update the fog of war state for all sides based on current unit positions and visibility.
        """
        # Placeholder: implement vision/fog logic
        pass

    def update_lighting(self):
        """
        Update lighting on the battle map based on light sources and environmental effects.
        """
        # Placeholder: implement lighting logic
        pass

    def get_diplomacy_action(self, attacker_side, target_side):
        """
        Get the diplomacy action between two sides.
        Args:
            attacker_side (int): Attacker's side identifier.
            target_side (int): Target's side identifier.
        Returns:
            int: Diplomacy action code.
        """
        return self.DIPLOMACY[attacker_side][target_side]

    def check_objectives(self):
        """
        Check the status of all battle objectives.
        """
        for obj in self.objectives:
            obj.check_status(self)

    def is_mission_complete(self):
        """
        Determine if the mission is complete based on objectives and battle state.
        Returns:
            bool: True if mission is complete, False otherwise.
        """
        return all(obj.status in ('complete', 'failed') for obj in self.objectives)

    def get_objective_statuses(self):
        """
        Get the current status of all objectives in the battle.
        Returns:
            list: List of objective statuses.
        """
        return [(obj.type, obj.status, obj.progress) for obj in self.objectives]

    def find_units(self, side=None, alive=None, unit_ids=None):
        """
        Find units in the battle matching the given criteria.
        Args:
            side (int, optional): Side identifier to filter units.
            alive (bool, optional): Filter by alive/dead status.
            unit_ids (list, optional): Filter by unit IDs.
        Returns:
            list: List of matching units.
        """
        result = []
        for side_units in self.sides:
            for unit in side_units:
                if side is not None and unit.side != side:
                    continue
                if alive is not None and getattr(unit, 'is_alive', True) != alive:
                    continue
                if unit_ids is not None and getattr(unit, 'id', None) not in unit_ids:
                    continue
                result.append(unit)
        return result

    def find_objects(self, object_ids=None):
        """
        Find objects in the battle matching the given IDs.
        Args:
            object_ids (list, optional): List of object IDs to find.
        Returns:
            list: List of matching objects.
        """
        result = []
        for row in self.tiles:
            for tile in row:
                for obj in getattr(tile, 'objects', []):
                    if object_ids is not None and getattr(obj, 'id', None) not in object_ids:
                        continue
                    result.append(obj)
        return result

    def find_tiles(self, objective_marker=None):
        """
        Find tiles in the battle matching a given objective marker.
        Args:
            objective_marker (any, optional): Marker to filter tiles.
        Returns:
            list: List of matching tiles.
        """
        result = []
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if objective_marker is not None and getattr(tile, 'objective_marker', None) != objective_marker:
                    continue
                result.append((x, y, tile))
        return result

