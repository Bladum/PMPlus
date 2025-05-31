"""
Craft Inventory Widget for XCOM Inventory System

This module provides the CraftInventoryWidget component which is specialized for
displaying and managing craft items, weapons, and equipment.
It extends the base InventoryWidget with craft-specific item categories and filtering.
"""

from typing import Dict, Any, Optional, Callable
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt

from engine.gui.other.base_item_list import TInventoryWidget
from inventory_system import InventoryItem


class TCraftInventoryWidget(TInventoryWidget):
    """
    A specialized inventory widget for displaying and managing craft equipment.

    Features:
    - Specific categories for craft items (weapons, engines, defenses, etc)
    - Sorted item list with counts
    - Drag and drop support for equipping/unequipping craft components
    - Item filtering by craft component type
    """

    def __init__(self, parent=None):
        """Initialize a craft inventory widget with appropriate categories."""
        # Define craft-specific categories
        craft_categories = [
            {"name": "All", "icon": "other/item2.png"},
            {"name": "Weapon", "icon": "items/fusionLance.png"},
            {"name": "Engine", "icon": "items/energyCell.png"},
            {"name": "Defense", "icon": "items/shieldGenerator.png"},
            {"name": "Special", "icon": "items/alienCore.png"},
            {"name": "Craft Item", "icon": "items/alienAlloy.png"},
        ]

        super().__init__(parent, categories=craft_categories)

        # Additional craft-specific initialization
        self.source_widget_id = 'craft_inventory'

    def add_craft_weapon(self, name: str, icon_path: Optional[str], info_dict: Dict[str, Any]) -> bool:
        """
        Add a craft weapon to the inventory.

        Args:
            name: Display name of the weapon
            icon_path: Path to weapon icon
            info_dict: Dictionary with weapon metadata

        Returns:
            True if weapon was added successfully, False otherwise
        """
        # Ensure item_type is set to weapon
        info_dict['item_type'] = 'weapon'
        return self.add_item(name, icon_path, info_dict, 1)

    def add_engine(self, name: str, icon_path: Optional[str], info_dict: Dict[str, Any]) -> bool:
        """
        Add an engine to the inventory.

        Args:
            name: Display name of the engine
            icon_path: Path to engine icon
            info_dict: Dictionary with engine metadata

        Returns:
            True if engine was added successfully, False otherwise
        """
        # Ensure item_type is set to engine
        info_dict['item_type'] = 'engine'
        return self.add_item(name, icon_path, info_dict, 1)

    def add_defense_system(self, name: str, icon_path: Optional[str], info_dict: Dict[str, Any]) -> bool:
        """
        Add a defense system to the inventory.

        Args:
            name: Display name of the defense system
            icon_path: Path to defense system icon
            info_dict: Dictionary with defense system metadata

        Returns:
            True if defense system was added successfully, False otherwise
        """
        # Ensure item_type is set to defense
        info_dict['item_type'] = 'defense'
        return self.add_item(name, icon_path, info_dict, 1)

    def add_craft_item(self, name: str, icon_path: Optional[str], info_dict: Dict[str, Any], count: int = 1) -> bool:
        """
        Add a craft item (materials, components) to the inventory.

        Args:
            name: Display name of the craft item
            icon_path: Path to craft item icon
            info_dict: Dictionary with craft item metadata
            count: Number of items to add

        Returns:
            True if craft item was added successfully, False otherwise
        """
        # Ensure item_type is set to craft item
        info_dict['item_type'] = 'craft item'
        return self.add_item(name, icon_path, info_dict, count)

    def set_craft(self, craft):
        """
        Set the craft for this inventory and populate with its items.

        Args:
            craft: Craft object with inventory items
        """
        self.clear_inventory()

        # If craft has inventory/components, populate the widget
        if hasattr(craft, 'components') and craft.components:
            for component in craft.components:
                component_info = component.to_dict() if hasattr(component, 'to_dict') else {
                    'item_type': component.component_type
                }
                self.add_item(
                    component.name,
                    component.icon_path if hasattr(component, 'icon_path') else None,
                    component_info,
                    1
                )

        # If craft has cargo/materials, add them too
        if hasattr(craft, 'cargo') and craft.cargo:
            for item_name, item_data in craft.cargo.items():
                count = item_data.get('count', 1)
                info = item_data.get('info', {'item_type': 'craft item'})
                icon_path = item_data.get('icon_path')

                self.add_item(item_name, icon_path, info, count)
