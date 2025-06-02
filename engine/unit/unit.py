"""
TUnit Class
==========

Purpose:
    Represents an individual unit in the game with all its attributes and capabilities.

Interactions:
    - Uses TUnitType for type information
    - Belongs to a faction (TSide)
    - Uses TUnitStats for attributes
    - Has racial template (TRace)
    - Can have traits (TTrait)
    - Equipped with armor and weapons
"""

from item.item_armour import TItemArmour
from item.item_weapon import TItemWeapon
from traits.trait import TTrait
from unit.race import TRace
from unit.side import TSide
from unit.unit_stat import TUnitStats
from unit.unit_type import TUnitType


class TUnit:

    def __init__(self, unit_type : TUnitType, side_id ):
        """
        Unit represent a single entity of unit in game.
        It has type only for reference, and all parameters

        """

        from engine.engine.game import TGame
        self.game = TGame()

        self.unit_type = unit_type
        self.side_id = side_id

        # for player units

        self.name = ''
        self.nationality = ''
        self.face = ''
        self.female = False

        # core units

        self.stats : TUnitStats = None
        self.race : TRace = None
        self.traits : list[TTrait] = None

        # equipment

        self.armour : TItemArmour = None
        self.weapon : TItemWeapon = None
        self.equipment : list[TItemWeapon] = None

        # position and direction

        self.position = None  # (x, y) coordinates on the map
        self.direction = None

        # status flags

        self.alive = True                # is the unit alive?
        self.dead = False                # unit is dead
        self.mind_controlled = False     # is the unit mind controlled?
        self.panicked = False            # is the unit panicked?
        self.crazy = False               # is the unit crazy?
        self.stunned = False             # is the unit stunned?
        self.kneeling = False            # is the unit kneeling?
        self.running = False             # is the unit running?

    def calculate_stats(self):
        # 1. Start with base stats from race
        stats = self.race.stats.copy()

        # 2. Apply traits modifiers
        for trait in self.traits:
            stats = stats + trait.stats

        # 3. Apply armor modifiers
        if self.armour:
            stats = stats + self.armour.get_stat_modifiers()

        # 4. Apply primary weapon modifiers
        if self.weapon:
            stats = stats + self.weapon.get_stat_modifiers()

        # 5. Apply secondary weapon modifiers
        for weapon in self.equipment:
            stats = stats + weapon.get_stat_modifiers()

        return stats





