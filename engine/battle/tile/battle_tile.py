"""
Battle tile module for representing individual tiles in a battle map.
"""
from typing import Optional, Dict, Any

from battle.tile.battle_floor import TBattleFloor
from battle.tile.battle_object import TBattleObject
from battle.tile.battle_roof import TBattleRoof
from battle.tile.battle_wall import TBattleWall
from unit.unit import TUnit


class TBattleTile:
    """
    Represents a single tile in the battle map.
    Each tile contains information about its floor, wall, roof, objects, and unit.

    Attributes:
        floor (TBattleFloor): The floor component of the tile.
        wall (TBattleWall|None): The wall component of the tile.
        roof (TBattleRoof|None): The roof component of the tile.
        objects (list[TBattleObject]): List of objects on this tile.
        unit (TUnit|None): Unit currently on this tile.
        smoke (bool): Whether the tile contains smoke.
        fire (bool): Whether the tile contains fire.
        gas (bool): Whether the tile contains gas.
        light_level (int): Light level on this tile.
        fog_of_war (list): Fog of war state for this tile.
        floor_id (str): ID of the floor tile.
        wall_id (str|None): ID of the wall tile.
        roof_id (str|None): ID of the roof tile.
        passable (bool): Whether the tile can be walked on.
        blocks_fire (bool): Whether the tile blocks fire.
        blocks_sight (bool): Whether the tile blocks line of sight.
        blocks_light (bool): Whether the tile blocks light.
        metadata (dict): Additional metadata for the tile.
    """
    def __init__(self,
                 floor_id: str = '0',
                 wall_id: Optional[str] = None,
                 roof_id: Optional[str] = None):
        """
        Initialize a battle tile with layer IDs.

        Args:
            floor_id: ID of the floor tile (mandatory)
            wall_id: ID of the wall tile (optional)
            roof_id: ID of the roof tile (optional)
        """

        self.floor : TBattleFloor = TBattleFloor()
        self.wall : TBattleWall = None
        self.roof : TBattleRoof = None

        self.objects : list[TBattleObject] = []
        self.unit : TUnit = None

        self.smoke = False
        self.fire = False
        self.gas = False
        self.light_level = 0
        self.fog_of_war = []

        self.floor_id: str = floor_id
        self.wall_id: Optional[str] = wall_id
        self.roof_id: Optional[str] = roof_id

        # Additional properties
        self.passable: bool = True
        self.blocks_fire: bool = False
        self.blocks_sight: bool = False
        self.blocks_light: bool = False
        self.metadata: Dict[str, Any] = {}

    def copy(self) -> 'TBattleTile':
        """
        Create a deep copy of this tile.

        Returns:
            A new TBattleTile with the same properties
        """
        new_tile = TBattleTile(self.floor_id, self.wall_id, self.roof_id)
        new_tile.passable = self.passable
        new_tile.blocks_fire = self.blocks_fire
        new_tile.blocks_sight = self.blocks_sight
        new_tile.blocks_light = self.blocks_light
        new_tile.metadata = self.metadata.copy()
        return new_tile

    def update_properties(self) -> None:
        """
        Update tile properties based on layer IDs.
        For example, walls might make a tile impassable.
        """
        # Base assumption: floors are passable
        self.passable = True
        self.blocks_fire = False
        self.blocks_sight = False

        # Walls typically block movement and sight/fire
        if self.wall_id is not None:
            self.passable = False
            self.blocks_fire = True
            self.blocks_sight = True

        # Roofs might block light
        if self.roof_id is not None:
            self.blocks_light = True

    def has_floor(self) -> bool:
        """
        Check if this tile has a floor.

        Returns:
            True if the tile has a valid floor ID
        """
        return self.floor_id > '0'

    def has_wall(self) -> bool:
        """
        Check if this tile has a wall.

        Returns:
            True if the tile has a valid wall ID
        """
        return self.wall_id is not None and self.wall_id > 0

    def has_roof(self) -> bool:
        """
        Check if this tile has a roof.

        Returns:
            True if the tile has a valid roof ID
        """
        return self.roof_id is not None and self.roof_id > 0

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

    @staticmethod
    def gid_to_tileset_name(gid, used_tilesets):
        """
        Convert a global tile ID (gid) to a string in the format 'XXX_YYY',
        where XXX is the tileset name and YYY is the relative tile id.
        Args:
            gid: The global tile ID.
            used_tilesets: List of dicts with keys: name, first_gid, last_gid, counttile
        Returns:
            str: 'XXX_YYY' or None if gid is 0 or not found.
        """
        if not gid or gid == 0:
            return None
        for tileset in used_tilesets:
            if tileset[1] <= gid <= tileset[2] :
                rel_id = gid - tileset[1] + 1
                return f"{tileset[0]}_{int(rel_id):03d}"
        return None

    @staticmethod
    def from_gids(floor_gid, wall_gid, roof_gid, used_tilesets):
        """
        Create a TBattleTile from GIDs and used_tilesets info.
        Returns a TBattleTile with floor_id, wall_id, roof_id set to 'XXX_YYY' format.
        """
        floor_id = TBattleTile.gid_to_tileset_name(floor_gid, used_tilesets)
        wall_id = TBattleTile.gid_to_tileset_name(wall_gid, used_tilesets)
        roof_id = TBattleTile.gid_to_tileset_name(roof_gid, used_tilesets)
        return TBattleTile(floor_id, wall_id, roof_id)
