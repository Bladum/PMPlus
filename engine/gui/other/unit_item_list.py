"""
Unit Inventory Widget for XCOM Inventory System

This module provides the UnitInventoryWidget component which is specialized for
displaying and managing unit equipment and inventory items (armor, weapons, equipment, etc).
It extends the base InventoryWidget with unit-specific item categories and filtering.
"""

from typing import Dict, Any, Optional, Callable
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt

from engine.gui.other.base_item_list import TInventoryWidget
from inventory_system import InventoryItem


class TUnitInventoryWidget(TInventoryWidget):
    """
    A specialized inventory widget for displaying and managing unit equipment.

    Features:
    - Specific categories for unit items (armor, weapons, equipment, others)
    - Sorted item list with counts
    - Drag and drop support for equipping/unequipping
    - Item filtering by type
    """

    def __init__(self, parent=None):
        """Initialize a unit inventory widget with appropriate categories."""
        # Define unit-specific categories
        unit_categories = [
            {"name": "All", "icon": "other/item2.png"},
            {"name": "Armour", "icon": "items/combatVest.png"},
            {"name": "Weapon", "icon": "items/assaultRifle.png"},
            {"name": "Equipment", "icon": "items/medikit.png"},
            {"name": "Other", "icon": "other/item.png"},
        ]

        super().__init__(parent, categories=unit_categories)

        # Additional unit-specific initialization
        self.source_widget_id = 'unit_inventory'

    def add_weapon(self, name: str, icon_path: Optional[str], info_dict: Dict[str, Any], count: int = 1) -> bool:
        """
        Add a weapon to the inventory with correct type.

        Args:
            name: Display name of the weapon
            icon_path: Path to weapon icon
            info_dict: Dictionary with weapon metadata
            count: Number of weapons to add

        Returns:
            True if weapon was added successfully, False otherwise
        """
        # Ensure item_type is set to weapon
        info_dict['item_type'] = 'weapon'
        return self.add_item(name, icon_path, info_dict, count)

    def add_armor(self, name: str, icon_path: Optional[str], info_dict: Dict[str, Any]) -> bool:
        """
        Add armor to the inventory with correct type.

        Args:
            name: Display name of the armor
            icon_path: Path to armor icon
            info_dict: Dictionary with armor metadata

        Returns:
            True if armor was added successfully, False otherwise
        """
        # Ensure item_type is set to armor
        info_dict['item_type'] = 'armour'
        return self.add_item(name, icon_path, info_dict, 1)

    def add_equipment(self, name: str, icon_path: Optional[str], info_dict: Dict[str, Any], count: int = 1) -> bool:
        """
        Add equipment to the inventory with correct type.

        Args:
            name: Display name of the equipment
            icon_path: Path to equipment icon
            info_dict: Dictionary with equipment metadata
            count: Number of equipment pieces to add

        Returns:
            True if equipment was added successfully, False otherwise
        """
        # Ensure item_type is set to equipment
        info_dict['item_type'] = 'equipment'
        return self.add_item(name, icon_path, info_dict, count)

    def set_unit(self, unit):
        """
        Set the unit for this inventory and populate with its items.

        Args:
            unit: Unit object with inventory items
        """
        self.clear_inventory()

        # If unit has inventory items, populate the widget
        if hasattr(unit, 'inventory') and unit.inventory:
            for item in unit.inventory:
                self.add_item(
                    item.name,
                    item.icon_path,
                    item.properties,
                    1  # Units typically have one of each equipment
                )
