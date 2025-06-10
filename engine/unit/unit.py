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
    - Uses TUnitInventoryManager for equipment management
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

        # equipment - managed through inventory manager
        from unit.unit_inv_manager import TUnitInventoryManager
        self.inventory_manager = TUnitInventoryManager(self)
        self.inventory = []  # For compatibility with inventory_manager's load/save methods

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

    @property
    def armour(self):
        """Get the unit's equipped armor"""
        return self.inventory_manager.equipment_slots.get("Armor")

    @property
    def weapon(self):
        """Get the unit's primary weapon"""
        return self.inventory_manager.equipment_slots.get("Primary")

    @property
    def equipment(self):
        """Get all equipped items as a list"""
        return [item for item in self.inventory_manager.equipment_slots.values() if item]

    def calculate_stats(self):
        # Use stats calculated from inventory manager
        base_stats = self.race.stats.copy()

        # Apply traits modifiers
        for trait in self.traits:
            base_stats = base_stats + trait.stats

        # Get all stat modifiers from equipment through inventory manager
        for slot_name, modifiers in self.inventory_manager.stat_modifiers.items():
            for stat_name, modifier in modifiers.items():
                if hasattr(base_stats, stat_name):
                    current_value = getattr(base_stats, stat_name)
                    setattr(base_stats, stat_name, current_value + modifier)

        return base_stats
