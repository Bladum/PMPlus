"""
TItemArmour: Represents an armour item assigned to a unit.

Manages shield points, regeneration, and resistance to damage types. Provides stat modifiers and interacts with unit systems for damage reduction.

Classes:
    TItemArmour: Main class for unit armour items.

Last standardized: 2025-06-14
"""

from typing import Dict, Any, Optional
from .item import TItem
from .item_type import TItemType


class TItemArmour(TItem):
    """
    Represents an armour item assigned to a unit (soldier, alien, etc).

    Manages shield points, regeneration, and resistance to damage types.
    Provides stat modifiers and interacts with unit systems for damage reduction.

    Attributes:
        shield (int): Current shield points.
        max_shield (int): Maximum shield points.
        shield_regen (int): Shield regeneration per turn.
    """

    def __init__(self, item_type_id: str, item_id: Optional[str] = None):
        """
        Initialize a new armour item.

        Args:
            item_type_id (str): ID of the armour type to use.
            item_id (Optional[str]): Unique identifier (generated if not provided).
        """
        super().__init__(item_type_id, item_id)
        self.shield = 0
        self.max_shield = self.item_type.armour_shield
        self.shield_regen = self.item_type.armour_shield_regen

    def shield_regeneration(self):
        """
        Regenerate shield by shield_regen per turn, up to max_shield.

        Returns:
            int: New shield value after regeneration.
        """
        if self.shield < self.max_shield:
            self.shield = min(self.max_shield, self.shield + self.shield_regen)
        return self.shield

    def is_shield_empty(self):
        """
        Check if the shield is depleted.

        Returns:
            bool: True if shield is empty or below zero, False otherwise.
        """
        return self.shield <= 0

    def reset_shield(self):
        """
        Reset shield to maximum value.
        """
        self.shield = self.max_shield

    def apply_damage(self, damage: int, damage_type: str) -> float:
        """
        Applies incoming damage to the shield first (no resistance), then applies resistance to remaining damage.

        Args:
            damage (int): Incoming damage value.
            damage_type (str): Type of damage (for resistance lookup).

        Returns:
            float: Final damage to be applied to the unit (after shield and resistance).
        """
        # Apply damage to shield first
        shield_damage = min(self.shield, damage)
        self.shield -= shield_damage
        remaining_damage = damage - shield_damage

        # If there is no shield left, apply resistance to remaining damage
        if remaining_damage > 0:
            resistances = self.item_type.armour_resistance
            if not resistances:
                return remaining_damage
            modifier = resistances.get(damage_type, 1.0)
            final_damage = remaining_damage * float(modifier)
            return final_damage

        return 0.0

    def get_stat_modifiers(self):
        """
        Returns a dictionary of stat modifiers provided by this armour.
        Override in subclasses or extend item_type to provide modifiers.

        Returns:
            dict: Stat modifiers affecting the unit.
        """
        return self.item_type.unit_stats
