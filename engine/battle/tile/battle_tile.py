from engine.battle.tile.battle_floor import TBattleFloor
from engine.battle.tile.battle_object import TBattleObject
from engine.battle.tile.battle_wall import TBattleWall
from engine.unit.unit import TUnit


class TBattleTile:
    """
    Represents a tile on battle map, it is 2D array of tiles
    It contains FLOOR, WALL, ITEM, UNIT
    """
    def __init__(self):
        self.floor : TBattleFloor = TBattleFloor()
        self.wall : TBattleWall = None
        self.objects : list[TBattleObject] = []
        self.unit : TUnit = None
        self.smoke = False
        self.fire = False
        self.gas = False
        self.light_level = 0
        self.fog_of_war = []
        self.objective_marker: str = None  # Marker for objectives (e.g. 'extraction', 'poc', 'sabotage')
        self.floor_id = None
        self.wall_id = None
        self.roof_id = None

    def set_layer_ids(self, floor_id, wall_id, roof_id):
        self.floor_id = floor_id
        self.wall_id = wall_id
        self.roof_id = roof_id

    @classmethod
    def from_layer_ids(cls, floor_id, wall_id, roof_id):
        """
        Create a TBattleTile from layer IDs and optional gid_map for properties.
        """
        tile = cls()

        tile.floor = TBattleFloor() if floor_id else None
        tile.wall = TBattleWall() if wall_id else None
        tile.roof_id = roof_id if roof_id else None
        tile.set_layer_ids(floor_id, wall_id, roof_id)
        return tile

    def is_walkable(self):
        """Returns True if tile can be walked on (no wall)."""
        return self.wall is None

    def get_move_cost(self):
        """Returns movement cost for this tile (floor only if walkable)."""
        if not self.is_walkable():
            return float('inf')
        return self.floor.move_cost if self.floor else 1

    def get_sight_cost(self):
        """Returns sight cost for this tile (floor + wall modifiers)."""
        cost = self.floor.sight_cost if self.floor else 0
        if self.wall:
            cost += self.wall.sight_mod
        return cost

    def get_accuracy_mod(self):
        """Returns accuracy modifier for this tile (floor + wall)."""
        mod = self.floor.accuracy_cost if self.floor else 0
        if self.wall:
            mod += self.wall.sight_mod
        return mod

    def get_armor(self):
        """Returns total armor for this tile (floor + wall)."""
        armor = self.floor.armor if self.floor else 0
        if self.wall:
            armor += self.wall.armor
        return armor

    def is_light_source(self):
        """Returns True if any component is a light source."""
        if (self.floor and self.floor.is_light_source) or (self.wall and self.wall.is_light_source):
            return True
        for obj in self.objects:
            if obj.is_light_source:
                return True
        return False

    def destroy_floor(self):
        """Destroys the floor and replaces it if needed."""
        if self.floor:
            new_id = self.floor.on_destroy()
            # Replace with new floor logic here if needed
            self.floor = None
            return new_id
        return None

    def destroy_wall(self):
        """Destroys the wall and replaces it if needed."""
        if self.wall:
            new_id = self.wall.on_destroy()
            # Replace with new wall logic here if needed
            self.wall = None
            return new_id
        return None

    def destroy_object(self, obj):
        """Destroys an object and replaces it if needed."""
        if obj in self.objects:
            new_id = obj.on_destroy()
            self.objects.remove(obj)
            # Replace with new object logic here if needed
            return new_id
        return None

    def apply_damage(self, damage, method, damage_type, damage_model, source=None, area_params=None, battle=None, x=None, y=None):
        """
        Apply damage to this tile.
        :param damage: base damage value
        :param method: 'POINT' or 'AREA'
        :param damage_type: e.g. 'kinetic', 'laser', etc.
        :param damage_model: model for splitting HURT/STUN
        :param source: source unit or weapon
        :param area_params: dict with area settings (radius, dropoff, etc.)
        :param battle: reference to TBattle (for AREA propagation)
        :param x, y: tile coordinates (for AREA)
        """
        if method == 'POINT':
            self.apply_point_damage(damage, damage_type, damage_model, source)
        elif method == 'AREA' and battle is not None and x is not None and y is not None:
            self.apply_area_damage(damage, damage_type, damage_model, source, area_params, battle, x, y)

    def apply_point_damage(self, damage, damage_type, damage_model, source=None):
        """
        Apply direct damage to this tile and its contents (unit, wall, floor, objects).
        Follows OpenXcom order: unit -> wall -> object -> floor.
        """
        # 1. Unit
        if self.unit:
            self.unit.apply_damage(damage, damage_type, damage_model, source)
        # 2. Wall
        if self.wall:
            resisted = self.calculate_resistance(self.wall, damage_type)
            dmg = max(0, damage * resisted - self.wall.armor)
            if dmg > 0:
                destroyed = self.wall.on_destroy() if dmg >= self.wall.armor else None
                if destroyed:
                    self.destroy_wall()
        # 3. Objects
        for obj in list(self.objects):
            resisted = self.calculate_resistance(obj, damage_type)
            dmg = max(0, damage * resisted - obj.armor)
            if dmg > 0:
                destroyed = obj.on_destroy() if dmg >= obj.armor else None
                if destroyed:
                    self.destroy_object(obj)
        # 4. Floor
        if self.floor:
            resisted = self.calculate_resistance(self.floor, damage_type)
            dmg = max(0, damage * resisted - self.floor.armor)
            if dmg > 0:
                destroyed = self.floor.on_destroy() if dmg >= self.floor.armor else None
                if destroyed:
                    self.destroy_floor()

    def apply_area_damage(self, damage, damage_type, damage_model, source, area_params, battle, x, y):
        """
        Apply area damage starting from this tile, propagating outward with drop-off.
        :param area_params: dict with keys 'radius', 'dropoff'
        """
        radius = area_params.get('radius', 1)
        dropoff = area_params.get('dropoff', 0)
        for dx in range(-radius, radius+1):
            for dy in range(-radius, radius+1):
                tx, ty = x+dx, y+dy
                if 0 <= tx < battle.width and 0 <= ty < battle.height:
                    dist = max(abs(dx), abs(dy))
                    dmg = max(0, damage - dropoff * dist)
                    if dmg > 0:
                        battle.tiles[ty][tx].apply_point_damage(dmg, damage_type, damage_model, source)

    def calculate_resistance(self, obj, damage_type):
        """
        Calculate resistance modifier for an object/armor vs. damage type.
        Returns a multiplier (e.g. 1.0 = no resistance, 0.5 = 50% resist, 1.5 = 50% more damage).
        """
        if hasattr(obj, 'resistances') and damage_type in obj.resistances:
            return obj.resistances[damage_type]
        return 1.0

    def distribute_damage(self, damage, damage_model):
        """
        Split damage into HURT/STUN based on damage model (e.g. {'hurt': 0.8, 'stun': 0.2}).
        Returns (hurt, stun).
        """
        hurt = damage * damage_model.get('hurt', 1.0)
        stun = damage * damage_model.get('stun', 0.0)
        return hurt, stun

