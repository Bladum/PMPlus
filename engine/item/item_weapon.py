"""
Represents a weapon item assigned to a unit (soldier, alien, etc).

This class manages the operational state and capabilities of a weapon
equipped by a unit. It maintains the current state of the weapon (ammo,
active mode) and provides methods to calculate effective parameters
based on the selected firing mode.

Interactions:
- References TItemType for static weapon parameters
- Uses TWeaponMode to calculate effective parameters for each mode
- Used by combat systems for hit chance and damage calculations
- Provides stat modifiers that may affect unit stats
- Interacts with UI systems for mode selection and ammo display

Key Features:
- Current state tracking (ammo, selected mode)
- Multiple firing modes with parameter adjustments
- Action point cost calculations
- Range, accuracy and damage parameter access
- Fire capability and ammo consumption
"""

from typing import Dict, Any, Optional
from .item import TItem
from .item_type import TItemType

class TItemWeapon(TItem):

    def __init__(self, item_type_id: str, item_id: Optional[str] = None):
        """
        Initialize a new weapon item.

        Args:
            item_type_id: ID of the weapon type to use
            item_id: Unique identifier (generated if not provided)
        """
        # Initialize base item
        super().__init__(item_type_id, item_id)

        # Weapon-specific attributes
        self.active = True
        self.ammo = self.item_type.unit_ammo if hasattr(self.item_type, 'unit_ammo') else 0

        # Weapon mode support
        self.current_mode = 'snap'  # default mode

        # Pre-calculate all mode parameters
        self.mode_params = {}
        base_params = {
            'ap_cost': self.item_type.unit_action_point,
            'range': self.item_type.unit_range,
            'accuracy': self.item_type.unit_accuracy,
            'shots': self.item_type.unit_shots,
            'damage': self.item_type.unit_damage
        }
        for mode_name, mode in self.item_type.unit_modes.items():
            self.mode_params[mode_name] = mode.apply(base_params)

    def get_mode_params(self, mode_name=None):
        if mode_name is None:
            mode_name = self.current_mode
        return self.mode_params.get(mode_name, {})

    def set_mode(self, mode_name):
        if mode_name in self.item_type.unit_modes:
            self.current_mode = mode_name
            return True
        return False

    def ammo_needed(self):
        return max(0, self.item_type.unit_ammo - self.ammo)

    def get_rearm_cost(self):
        return self.ammo_needed() * self.item_type.unit_rearm_cost

    def can_in_range(self, target_range):
        params = self.get_mode_params()
        ranged = params.get('range', self.item_type.unit_range)
        return target_range <= ranged

    def can_fire(self, current_ap=4):
        params = self.get_mode_params()
        ap_cost = params.get('ap_cost', self.item_type.unit_action_point )
        shots = params.get('shots', 1)
        return self.ammo >= shots and current_ap >= ap_cost

    def fire(self):
        params = self.get_mode_params()
        shots = params.get('shots', 1)
        if self.ammo >= shots:
            self.ammo -= shots
            return True
        return False

    def get_shots(self):
        params = self.get_mode_params()
        return params.get('shots', self.item_type.unit_shots)

    def get_range(self):
        params = self.get_mode_params()
        return params.get('range', self.item_type.unit_range)

    def get_accuracy(self):
        params = self.get_mode_params()
        return params.get('accuracy', self.item_type.unit_accuracy)

    def get_damage(self):
        params = self.get_mode_params()
        return params.get('damage', self.item_type.unit_damage)

    def get_ap_cost(self):
        params = self.get_mode_params()
        return params.get('ap_cost', self.item_type.unit_action_point )

    def get_stat_modifiers(self):
        return self.item_type.unit_stats
