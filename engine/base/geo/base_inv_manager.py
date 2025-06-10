"""
Base Inventory Management System

This module provides comprehensive inventory management for XCOM bases,
handling items, units, and crafts with categorized storage and operations.
"""

from typing import Dict, List, Optional, Tuple, Set, Union, Any

from enums import EUnitItemCategory
from unit.unit import TUnit
from craft.craft import TCraft


class TBaseInventory:
    """
    Inventory management system for XCOM bases.

    Provides comprehensive functionality for managing items, units, and crafts
    including categorized storage, addition, removal, and various sorting options.

    Attributes:
        items: Dictionary mapping item IDs to quantities
        units: List of units stationed at the base
        crafts: List of crafts stationed at the base
        item_categories: Dictionary mapping item IDs to their categories
        storage_capacity: Maximum item storage capacity in size units
        craft_capacity: Maximum number of crafts that can be stored at the base
        item_sizes: Dictionary mapping item IDs to their size values
    """

    def __init__(self, storage_capacity: int = 100, craft_capacity: int = 4):
        """
        Initialize empty inventory with necessary data structures

        Args:
            storage_capacity: Maximum storage capacity for items (default: 100)
            craft_capacity: Maximum number of crafts that can be stored (default: 4)
        """
        self.items: Dict[str, float] = {}  # Item ID -> quantity
        self.units: List[TUnit] = []
        self.crafts: List[TCraft] = []
        self.item_categories: Dict[str, EUnitItemCategory] = {}  # Item ID -> category
        self.captures: Dict[str, float] = {}  # Captured units/specimens ID -> quantity
        self.item_sizes: Dict[str, float] = {}  # Item ID -> size value
        self.storage_capacity: int = storage_capacity
        self.craft_capacity: int = craft_capacity

    # Item management methods

    def add_item(self, item_id: str, quantity: float = 1.0, category: Optional[EUnitItemCategory] = None) -> bool:
        """
        Add an item to inventory or increase its quantity if it already exists.
        Validates against storage capacity before adding.

        Args:
            item_id: Unique identifier for the item
            quantity: Amount to add (can be fractional for certain resources)
            category: Item category for classification (only set when adding new items)

        Returns:
            True if successfully added, False if insufficient storage capacity
        """
        # Calculate required storage space for new items
        item_size = self.get_item_size(item_id)
        required_space = quantity * item_size

        # If item already exists, we only need space for the additional quantity
        if item_id in self.items:
            required_space = (self.items[item_id] + quantity) * item_size - self.items[item_id] * item_size

        # Check if there's enough space
        if required_space > self.get_remaining_storage():
            return False

        # Add the item since we have enough space
        if item_id in self.items:
            self.items[item_id] += quantity
        else:
            self.items[item_id] = quantity
            if category:
                self.item_categories[item_id] = category
            else:
                # Default to OTHER if no category provided
                self.item_categories[item_id] = EUnitItemCategory.EQUIPMENT

        return True

    def remove_item(self, item_id: str, quantity: float = 1.0) -> bool:
        """
        Remove an item from inventory or reduce its quantity.

        Args:
            item_id: Unique identifier for the item
            quantity: Amount to remove

        Returns:
            True if successful, False if not enough items available
        """
        if item_id not in self.items or self.items[item_id] < quantity:
            return False

        self.items[item_id] -= quantity

        # Remove item completely if quantity reaches 0
        if self.items[item_id] <= 0:
            del self.items[item_id]
            if item_id in self.item_categories:
                del self.item_categories[item_id]

        return True

    def set_item_quantity(self, item_id: str, quantity: float, category: Optional[EUnitItemCategory] = None) -> bool:
        """
        Set exact quantity of an item, adding it if it doesn't exist.
        Validates against storage capacity.

        Args:
            item_id: Unique identifier for the item
            quantity: Exact quantity to set
            category: Item category if adding new item

        Returns:
            True if successfully set, False if insufficient storage capacity
        """
        if quantity <= 0:
            # Remove the item completely
            if item_id in self.items:
                del self.items[item_id]
                if item_id in self.item_categories:
                    del self.item_categories[item_id]
            return True
        else:
            # Calculate required storage change
            item_size = self.get_item_size(item_id)
            current_quantity = self.items.get(item_id, 0)
            storage_change = (quantity - current_quantity) * item_size

            # Check if there's enough space for the increased quantity
            if storage_change > 0 and storage_change > self.get_remaining_storage():
                return False

            # Set the quantity since we have enough space
            self.items[item_id] = quantity

            # Set category if item is new and category is provided
            if item_id not in self.item_categories and category:
                self.item_categories[item_id] = category
            elif item_id not in self.item_categories:
                self.item_categories[item_id] = EUnitItemCategory.EQUIPMENT

            return True

    def get_item_quantity(self, item_id: str) -> float:
        """
        Get quantity of an item in inventory.

        Args:
            item_id: Unique identifier for the item

        Returns:
            Current quantity of item, 0 if item doesn't exist
        """
        return self.items.get(item_id, 0)

    def get_item_category(self, item_id: str) -> Optional[EUnitItemCategory]:
        """
        Get category of an item.

        Args:
            item_id: Unique identifier for the item

        Returns:
            ItemCategory of the item, None if item doesn't exist
        """
        return self.item_categories.get(item_id)

    def set_item_category(self, item_id: str, category: EUnitItemCategory) -> bool:
        """
        Set or update category of an existing item.

        Args:
            item_id: Unique identifier for the item
            category: New category for the item

        Returns:
            True if successful, False if item doesn't exist
        """
        if item_id not in self.items:
            return False

        self.item_categories[item_id] = category
        return True

    def get_items_by_category(self, category: EUnitItemCategory) -> Dict[str, float]:
        """
        Get all items of a specific category with their quantities.

        Args:
            category: Category to filter by

        Returns:
            Dictionary of item_id -> quantity for matching items
        """
        return {
            item_id: qty for item_id, qty in self.items.items()
            if self.item_categories.get(item_id) == category
        }

    def get_total_items_count(self) -> int:
        """
        Get total count of all items (sum of quantities).

        Returns:
            Sum of all item quantities
        """
        return sum(self.items.values())

    def get_unique_items_count(self) -> int:
        """
        Get count of unique items (regardless of quantity).

        Returns:
            Count of unique item types in inventory
        """
        return len(self.items)

    def has_sufficient_items(self, required_items: Dict[str, float]) -> bool:
        """
        Check if inventory has sufficient quantities of required items.

        Args:
            required_items: Dictionary mapping item IDs to required quantities

        Returns:
            True if all requirements are met, False otherwise
        """
        for item_id, required_qty in required_items.items():
            if self.items.get(item_id, 0) < required_qty:
                return False
        return True

    def consume_items(self, items_to_consume: Dict[str, float]) -> bool:
        """
        Consume multiple items at once if sufficient quantities are available.

        Args:
            items_to_consume: Dictionary mapping item IDs to quantities to consume

        Returns:
            True if successful, False if not enough of any item
        """
        # First check if we have enough of everything
        if not self.has_sufficient_items(items_to_consume):
            return False

        # Remove all items
        for item_id, qty in items_to_consume.items():
            self.remove_item(item_id, qty)

        return True

    def set_item_size(self, item_id: str, size: float) -> None:
        """
        Set the size/storage space requirement for an item.

        Args:
            item_id: Unique identifier for the item
            size: Space taken by one unit of the item
        """
        self.item_sizes[item_id] = size

    def get_item_size(self, item_id: str) -> float:
        """
        Get the size of an item.

        Args:
            item_id: Unique identifier for the item

        Returns:
            Size of the item, defaults to 1.0 if not specified
        """
        return self.item_sizes.get(item_id, 1.0)

    def get_used_storage(self) -> float:
        """
        Calculate the total used storage space.

        Returns:
            Total storage space used by all items
        """
        return sum(self.items.get(item_id, 0) * self.get_item_size(item_id)
                  for item_id in self.items)

    def get_remaining_storage(self) -> float:
        """
        Calculate the remaining storage space.

        Returns:
            Remaining storage capacity
        """
        return max(0, self.storage_capacity - self.get_used_storage())

    # Unit management methods

    def add_unit(self, unit: TUnit) -> None:
        """
        Add a unit to the base.

        Args:
            unit: Unit to add
        """
        self.units.append(unit)

    def remove_unit(self, unit: TUnit) -> bool:
        """
        Remove a unit from the base.

        Args:
            unit: Unit to remove

        Returns:
            True if unit was found and removed, False otherwise
        """
        if unit in self.units:
            self.units.remove(unit)
            return True
        return False

    def get_units_count(self) -> int:
        """
        Get total number of units at base.

        Returns:
            Count of units
        """
        return len(self.units)

    def get_units_by_type(self, unit_type: str) -> List[TUnit]:
        """
        Get units of a specific type.

        Args:
            unit_type: Type identifier to filter by

        Returns:
            List of matching units
        """
        return [unit for unit in self.units if unit.unit_type == unit_type]

    # Craft management methods

    def add_craft(self, craft: TCraft) -> bool:
        """
        Add a craft to the base if there's available capacity.

        Args:
            craft: Craft to add

        Returns:
            True if successfully added, False if no capacity available
        """
        # Check if there's available capacity for the new craft
        if len(self.crafts) >= self.craft_capacity:
            return False

        # Add the craft since we have enough capacity
        self.crafts.append(craft)
        return True

    def remove_craft(self, craft: TCraft) -> bool:
        """
        Remove a craft from the base.

        Args:
            craft: Craft to remove

        Returns:
            True if craft was found and removed, False otherwise
        """
        if craft in self.crafts:
            self.crafts.remove(craft)
            return True
        return False

    def get_crafts_count(self) -> int:
        """
        Get total number of crafts at base.

        Returns:
            Count of crafts
        """
        return len(self.crafts)

    def get_crafts_by_type(self, craft_type: str) -> List[TCraft]:
        """
        Get crafts of a specific type.

        Args:
            craft_type: Type identifier to filter by

        Returns:
            List of matching crafts
        """
        return [craft for craft in self.crafts if craft.craft_type.id == craft_type]

    # Capture management methods

    def add_capture(self, capture_id: str, quantity: float = 1.0) -> None:
        """
        Add captured unit/specimen to inventory.

        Args:
            capture_id: Unique identifier for the capture
            quantity: Amount to add
        """
        if capture_id in self.captures:
            self.captures[capture_id] += quantity
        else:
            self.captures[capture_id] = quantity

    def remove_capture(self, capture_id: str, quantity: float = 1.0) -> bool:
        """
        Remove captured unit/specimen from inventory.

        Args:
            capture_id: Unique identifier for the capture
            quantity: Amount to remove

        Returns:
            True if successful, False if not enough captures available
        """
        if capture_id not in self.captures or self.captures[capture_id] < quantity:
            return False

        self.captures[capture_id] -= quantity

        # Remove capture completely if quantity reaches 0
        if self.captures[capture_id] <= 0:
            del self.captures[capture_id]

        return True

    def get_capture_quantity(self, capture_id: str) -> float:
        """
        Get quantity of a captured unit/specimen.

        Args:
            capture_id: Unique identifier for the capture

        Returns:
            Current quantity, 0 if not found
        """
        return self.captures.get(capture_id, 0)

    # Serialization methods

    def to_dict(self) -> Dict:
        """
        Convert inventory to dictionary for serialization.

        Returns:
            Dictionary representation of inventory
        """
        # Convert categories to strings for serialization
        category_dict = {
            item_id: category.value
            for item_id, category in self.item_categories.items()
        }

        return {
            "items": self.items,
            "item_categories": category_dict,
            "captures": self.captures,
            # We don't serialize units and crafts here as they are complex objects
            # They should be handled separately by their own serialization methods
        }

    def from_dict(self, data: Dict) -> None:
        """
        Load inventory from dictionary.

        Args:
            data: Dictionary containing inventory data
        """
        # Load items
        self.items = data.get("items", {})

        # Load categories with proper conversion
        self.item_categories = {}
        for item_id, category_str in data.get("item_categories", {}).items():
            try:
                self.item_categories[item_id] = EUnitItemCategory(category_str)
            except ValueError:
                # Fallback to ITEM_OTHER if category is invalid
                self.item_categories[item_id] = EUnitItemCategory.EQUIPMENT

        # Load captures
        self.captures = data.get("captures", {})

        # Note: This doesn't restore units or crafts, as they need special handling

    def save_template(self) -> Dict[str, Any]:
        """
        Save current base inventory as a template dict.
        Returns:
            Dictionary representing the current items, units, crafts, and captures.
        """
        return {
            'items': dict(self.items),
            'units': [unit.id for unit in self.units],
            'crafts': [craft.id for craft in self.crafts],
            'captures': dict(self.captures)
        }

    def load_template(self, template: Dict[str, Any], unit_provider=None, craft_provider=None) -> None:
        """
        Load base inventory from a template dict.
        Args:
            template: Dictionary representing items, units, crafts, and captures.
            unit_provider: Optional function to get TUnit by id
            craft_provider: Optional function to get TCraft by id
        """
        self.items = dict(template.get('items', {}))
        self.captures = dict(template.get('captures', {}))
        if unit_provider:
            self.units = [unit_provider(uid) for uid in template.get('units', [])]
        if craft_provider:
            self.crafts = [craft_provider(cid) for cid in template.get('crafts', [])]
