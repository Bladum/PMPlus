from engine.battle.map.battle_generator import TBattleGenerator
from engine.battle.tile.battle_tile import TBattleTile
from engine.unit.unit import TUnit
from engine.battle.mission.objective import BattleObjective


class TBattle:
    """
    Represents a battle, created by a mission.
    Holds all units, map tiles, items, effects, and manages battle sides and turns.
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
        self.objectives: list[BattleObjective] = []

    def add_unit(self, unit: TUnit, side: int, x: int, y: int):
        """Adds a unit to the battle on a given side and position."""
        self.sides[side].append(unit)
        self.tiles[y][x].unit = unit
        unit.x = x
        unit.y = y
        unit.side = side

    def process_turn(self):
        """Processes a full turn for all sides."""
        for side in range(self.NUM_SIDES):
            self.process_side(side)
        self.turn += 1

    def process_side(self, side: int):
        """Processes all units for a given side."""
        for unit in self.sides[side]:
            self.process_unit(unit)

    def process_unit(self, unit: TUnit):
        """Processes a single unit's actions (AI or player)."""
        # Placeholder: implement AI, player input, etc.
        pass

    def update_fog_of_war(self):
        """Updates fog of war for all sides based on unit vision."""
        # Placeholder: implement vision/fog logic
        pass

    def update_lighting(self):
        """Updates lighting for all tiles based on light sources."""
        # Placeholder: implement lighting logic
        pass

    def get_diplomacy_action(self, attacker_side, target_side):
        """
        Returns the diplomacy action between two sides.
        0 = ignore, 1 = hostile, 2 = opportunistic, -1 = protect
        """
        return self.DIPLOMACY[attacker_side][target_side]

    def check_objectives(self):
        """Update all objectives' status."""
        for obj in self.objectives:
            obj.check_status(self)

    def is_mission_complete(self):
        """Returns True if all objectives are complete or failed (mission over)."""
        return all(obj.status in ('complete', 'failed') for obj in self.objectives)

    def get_objective_statuses(self):
        """Returns a list of (type, status, progress) for all objectives."""
        return [(obj.type, obj.status, obj.progress) for obj in self.objectives]

    def find_units(self, side=None, alive=None, unit_ids=None):
        """
        Returns a list of units matching the criteria.
        :param side: filter by side (int)
        :param alive: filter by alive status (True/False)
        :param unit_ids: filter by unit ids (list)
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
        Returns a list of objects on the map matching the criteria.
        :param object_ids: filter by object ids (list)
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
        Returns a list of (x, y, tile) for tiles matching the criteria.
        :param objective_marker: filter by marker (str)
        """
        result = []
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if objective_marker is not None and getattr(tile, 'objective_marker', None) != objective_marker:
                    continue
                result.append((x, y, tile))
        return result

