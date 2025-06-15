"""
TItemWeapon: Represents a weapon item assigned to a unit (soldier, alien, etc).

Manages weapon state, firing modes, and provides methods for combat calculations.

Classes:
    TItemWeapon: Main class for unit weapon items.

Last standardized: 2025-06-14
"""

from typing import Dict, Any, Optional
from .item import TItem
from .item_type import TItemType

class TItemWeapon(TItem):
    """
    Represents a weapon item assigned to a unit (soldier, alien, etc).

    Manages weapon state, firing modes, and provides methods for combat calculations.

    Attributes:
        active (bool): Whether the weapon is active.
        ammo (int): Current ammo count.
        current_mode (str): Currently selected firing mode.
        mode_params (dict): Pre-calculated parameters for each mode.
    """

    def __init__(self, item_type_id: str, item_id: Optional[str] = None):
        """
        Initialize a new weapon item.

        Args:
            item_type_id (str): ID of the weapon type to use.
            item_id (Optional[str]): Unique identifier (generated if not provided).
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
        """
        Get the parameters for a specific firing mode.

        Args:
            mode_name (Optional[str]): Name of the mode. If None, uses current_mode.
        Returns:
            dict: Mode parameters (ap_cost, range, accuracy, shots, damage).
        """
        if mode_name is None:
            mode_name = self.current_mode
        return self.mode_params.get(mode_name, {})

    def set_mode(self, mode_name):
        """
        Set the current firing mode.

        Args:
            mode_name (str): Name of the mode to set.
        Returns:
            bool: True if mode was set, False if not found.
        """
        if mode_name in self.item_type.unit_modes:
            self.current_mode = mode_name
            return True
        return False

    def ammo_needed(self):
        """
        Calculate how much ammo is needed to fully reload.

        Returns:
            int: Number of ammo units needed.
        """
        return max(0, self.item_type.unit_ammo - self.ammo)

    def get_rearm_cost(self):
        """
        Calculate the cost to fully rearm the weapon.

        Returns:
            int: Rearm cost.
        """
        return self.ammo_needed() * self.item_type.unit_rearm_cost

    def can_in_range(self, target_range):
        """
        Check if the target is within range for the current mode.

        Args:
            target_range (int): Distance to target.
        Returns:
            bool: True if in range, False otherwise.
        """
        params = self.get_mode_params()
        ranged = params.get('range', self.item_type.unit_range)
        return target_range <= ranged

    def can_fire(self, current_ap=4):
        """
        Check if the weapon can fire (enough ammo and action points).

        Args:
            current_ap (int): Current action points available.
        Returns:
            bool: True if weapon can fire, False otherwise.
        """
        params = self.get_mode_params()
        ap_cost = params.get('ap_cost', self.item_type.unit_action_point )
        shots = params.get('shots', 1)
        return self.ammo >= shots and current_ap >= ap_cost

    def fire(self):
        """
        Consume ammo for a firing action.

        Returns:
            bool: True if fired successfully, False if not enough ammo.
        """
        params = self.get_mode_params()
        shots = params.get('shots', 1)
        if self.ammo >= shots:
            self.ammo -= shots
            return True
        return False

    def get_shots(self):
        """
        Get the number of shots for the current mode.

        Returns:
            int: Number of shots.
        """
        params = self.get_mode_params()
        return params.get('shots', self.item_type.unit_shots)

    def get_range(self):
        """
        Get the range for the current mode.

        Returns:
            int: Range value.
        """
        params = self.get_mode_params()
        return params.get('range', self.item_type.unit_range)

    def get_accuracy(self):
        """
        Get the accuracy for the current mode.

        Returns:
            int: Accuracy value.
        """
        params = self.get_mode_params()
        return params.get('accuracy', self.item_type.unit_accuracy)

    def get_damage(self):
        """
        Get the damage for the current mode.

        Returns:
            int: Damage value.
        """
        params = self.get_mode_params()
        return params.get('damage', self.item_type.unit_damage)

    def get_ap_cost(self):
        """
        Get the action point cost for the current mode.

        Returns:
            int: Action point cost.
        """
        params = self.get_mode_params()
        return params.get('ap_cost', self.item_type.unit_action_point )

    def get_stat_modifiers(self):
        """
        Get stat modifiers provided by this weapon.

        Returns:
            dict: Stat modifiers affecting the unit.
        """
        return self.item_type.unit_stats
