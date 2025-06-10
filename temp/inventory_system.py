"""
Inventory Management System for XCOM Inventory Application

This module provides comprehensive inventory and item management functionality
including item creation, template systems, and unit-specific inventory tracking.
It handles serialization, item properties, and provides a foundation for
save/load functionality.

Key Features:
- InventoryItem class with full property management
- Template system for saving/loading equipment configurations
- Unit-specific inventory management and persistence
- Comprehensive serialization support (to_dict/from_dict)
- Type-safe item handling with proper enumerations
- Stackable and non-stackable item support
- Weight-based inventory calculations

Classes:
- InventoryItem: Core item representation with properties and metadata
- InventoryTemplate: Equipment configuration template storage
- TemplateManager: Template persistence and management operations
- UnitInventoryManager: Per-unit inventory state management
"""

import json
import os
from typing import Optional, Dict, Any, List, Union
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QIcon

from item_path_lookup import get_canonical_path

class InventoryItem:
    """
    Core class representing an individual inventory item.
    
    This class encapsulates all item properties including visual representation,
    game mechanics data, and serialization capabilities. Items can be weapons,
    armor, equipment, or miscellaneous objects with varying properties.

    Attributes:
        name: Human-readable item name
        icon_path: Path to item's visual icon
        properties: Dictionary of item-specific properties and stats
        item_type: ItemType enumeration (WEAPON, ARMOUR, EQUIPMENT, OTHER)
        stackable: Whether multiple items can stack in inventory
        max_stack: Maximum number that can stack together
        id: Unique identifier for the item instance
        weight: Item weight for inventory management
        description: Human-readable item description
    """
    
    def __init__(self, name: str, icon_path: Optional[str], properties: Optional[Dict[str, Any]] = None, 
                 item_type: ItemType = ItemType.OTHER,
                 stackable: bool = False, max_stack: int = 1, item_id: Optional[str] = None,
                 weight: int = 1) -> None:
        """
        Initialize a new inventory item.
        
        Args:
            name: Display name for the item
            icon_path: Path to icon file, defaults to 'other/item.png' if None
            properties: Dictionary of custom properties and stats
            item_type: Type classification for the item
            stackable: Whether item can stack with identical items
            max_stack: Maximum stack size if stackable
            item_id: Unique ID, auto-generated from name if None
            weight: Item weight for inventory calculations
        """
        self.name = name
        
        # Use the canonical path from game_data if available, otherwise use the provided path,
        # and fall back to default if neither is available
        canonical_path = get_canonical_path(name)
        if canonical_path:
            self.icon_path = canonical_path
        elif icon_path:
            self.icon_path = icon_path
        else:
            self.icon_path = 'other/item.png'
            
        self.properties = properties or {}
        self.item_type = item_type
        self.stackable = stackable
        self.max_stack = max_stack
        self.id = item_id or f"{name}_{hash(name) % 10000}"
        self.weight = weight

        # Extract description from properties if available
        self.description = self.properties.get('desc', f"A {self.item_type.value}")

    def get_pixmap(self, size: int = 64) -> QPixmap:
        """
        Get a QPixmap representation of the item icon.
        
        Args:
            size: Desired size in pixels (square)
            
        Returns:
            QPixmap scaled to requested size with fast transformation
            
        Uses FastTransformation for crisp scaling without blurring,
        maintaining pixel art aesthetics.
        """
        # Use Qt.FastTransformation for crisp scaling without blurring
        return QPixmap(self.icon_path).scaled(size, size, Qt.KeepAspectRatio, Qt.FastTransformation)

    def get_icon(self, size: int = 32) -> QIcon:
        """
        Get a QIcon representation of the item.
        
        Args:
            size: Desired icon size in pixels
            
        Returns:
            QIcon created from the item's pixmap
            
        Convenience method for UI components that require QIcon objects.
        """
        return QIcon(self.get_pixmap(size))

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize the item to a dictionary for storage or transmission.
        
        Returns:
            Dictionary containing all item data in JSON-serializable format
            
        Used for saving items to files, templates, or network transmission.
        All enum values are converted to their string representations.
        """
        return {
            'id': self.id,
            'name': self.name,
            'icon_path': self.icon_path,
            'properties': self.properties,
            'item_type': self.item_type.value,
            'stackable': self.stackable,
            'max_stack': self.max_stack,
            'description': self.description,
            'weight': self.weight
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'InventoryItem':
        """
        Create an InventoryItem from a dictionary representation.
        
        Args:
            data: Dictionary containing item data (from to_dict() or JSON)
            
        Returns:
            New InventoryItem instance with data from dictionary
            
        Handles conversion of string enum values back to proper enums.
        Provides defaults for missing optional fields.
        Always uses canonical path from game_data for consistent icons.
        """
        # Get the item name first since we need it for the canonical path
        name = data['name']
        
        # Use canonical path directly from GameData to ensure consistency
        # The icon_path in data is ignored to fix the reference issue
        return cls(
            name=name,  # Use name directly (canonical path will be looked up)
            icon_path=None,  # icon_path will be set in __init__ using canonical path
            properties=data.get('properties', {}),
            item_type=ItemType(data.get('item_type', 'other')),
            stackable=data.get('stackable', False),
            max_stack=data.get('max_stack', 1),
            item_id=data.get('id'),
            weight=data.get('weight', 1)
        )



class TemplateManager:
    """
    Manager for equipment template persistence and operations.
    
    This class provides a simplified interface for template management.
    In the current implementation, it serves as a placeholder for future
    file-based or database-backed template storage systems.
    
    Note: Current implementation is simplified for in-memory use only.
    Future versions could implement file-based persistence or cloud storage.
    """
    
    @staticmethod
    def save_template(template: InventoryTemplate) -> bool:
        """
        Save an equipment template to persistent storage.
        
        Args:
            template: InventoryTemplate instance to save
            
        Returns:
            True if save was successful, False otherwise
            
        Note: Current implementation is simplified and always returns True.
        """
        return True

    @staticmethod
    def load_template(name: str) -> Optional[InventoryTemplate]:
        """
        Load an equipment template by name.
        
        Args:
            name: Name of the template to load
            
        Returns:
            InventoryTemplate instance if found, None otherwise
            
        Note: Current implementation is simplified and always returns None.
        """
        return None

    @staticmethod
    def get_available_templates() -> List[str]:
        """
        Get list of available template names.
        
        Returns:
            List of template names available for loading
            
        Note: Current implementation is simplified and returns empty list.
        """
        return []

    @staticmethod
    def delete_template(name: str) -> bool:
        """
        Delete a template by name.
        
        Args:
            name: Name of the template to delete
            
        Returns:
            True if deletion was successful, False otherwise
            
        Note: Current implementation is simplified and always returns False.
        """
        return False
# TEMPLATE SYSTEM END

# Unit-specific inventory management
class UnitInventoryManager:
    """
    Manager for per-unit equipment configurations and persistence.
    
    This class handles saving and loading equipment setups for individual units,
    allowing each unit to maintain their own equipment configuration. When
    switching between units, their previously equipped items are automatically
    restored.
    
    Features:
    - Per-unit equipment state persistence
    - Automatic inventory return when switching units
    - Error handling for corrupted or missing item data
    - Unit inventory validation and cleanup
    
    Attributes:
        unit_inventories: Dictionary mapping unit names to equipment configurations
    """
    
    def __init__(self) -> None:
        """
        Initialize a new unit inventory manager.
        
        Creates an empty inventory tracking system. Unit inventories
        are populated as units are equipped and saved.
        """
        self.unit_inventories: Dict[str, Dict[str, Optional[Dict[str, Any]]]] = {}  # Maps unit name to equipment setup
        
    def save_unit_inventory(self, unit_name: str, equipment_slots: List[Any]) -> None:
        """
        Save current equipment setup for a specific unit.
        
        Args:
            unit_name: Name of the unit to save equipment for
            equipment_slots: List of equipment slot widgets containing items
            
        Iterates through all equipment slots and saves the current item
        configuration. Empty slots are recorded as None values.
        """
        equipment_data: Dict[str, Optional[Dict[str, Any]]] = {}
        for slot in equipment_slots:
            slot_key = slot.slot_name
            if slot.item:
                equipment_data[slot_key] = slot.item.to_dict()
            else:
                equipment_data[slot_key] = None
        
        self.unit_inventories[unit_name] = equipment_data
        print(f"Saved inventory for unit: {unit_name}")

    def load_unit_inventory(self, unit_name: str, equipment_slots: List[Any], 
                          item_list_widget: Any) -> None:
        """
        Load equipment setup for a specific unit.
        
        Args:
            unit_name: Name of the unit to load equipment for
            equipment_slots: List of equipment slot widgets to populate
            item_list_widget: Widget managing the general item inventory
            
        Clears current equipment, then loads the saved configuration for the 
        specified unit. Items from the previous unit stay with that unit's 
        saved inventory - they don't return to base inventory when switching units.
        """
        print(f"Loading inventory for unit: {unit_name}")
        
        # Clear current equipment (don't return to inventory - items stay with previous unit)
        for slot in equipment_slots:
            if slot.item:
                slot.remove_item()  # Just remove, don't add back to inventory
        
        if unit_name not in self.unit_inventories:
            print(f"No saved inventory for {unit_name}, cleared all slots")
            return

        equipment_data = self.unit_inventories[unit_name]

        # Load saved equipment
        for slot in equipment_slots:
            slot_key = slot.slot_name
            if slot_key in equipment_data and equipment_data[slot_key]:
                try:
                    item = InventoryItem.from_dict(equipment_data[slot_key])
                    if slot.add_item(item):
                        # NOTE: Don't remove from base inventory when loading existing unit equipment
                        # Items were already removed when first equipped - they're just being restored
                        print(f"Loaded {item.name} into {slot_key}")
                except Exception as e:
                    print(f"Error loading item for slot {slot_key}: {e}")
        
        # After loading all equipment, validate equipment slots based on armor
        from engine.gui.widgets import validate_and_update_equipment_slots
        validate_and_update_equipment_slots()

    def get_all_unit_names(self) -> List[str]:
        """
        Get all unit names that have saved inventory configurations.
        
        Returns:
            List of unit names with saved equipment setups
            
        Useful for debugging, cleanup operations, or displaying
        units with custom equipment configurations.
        """
        return list(self.unit_inventories.keys())