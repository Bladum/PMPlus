"""
Unit Inventory Management System

This module provides inventory management functionality for units in the game,
handling equipment slots for armor, weapons, and up to 4 equipment items.

Key Features:
- Equipment slot management (armor, weapon, equipment)
- Dynamic slot availability based on armor type
- Template saving/loading for quick equipment setups
- Weight calculation for equipped items
- Item validation and compatibility checking
"""

from typing import Optional, Dict, List, Any, Tuple, Union, Set
from dataclasses import dataclass, field

# Import existing item class if available, otherwise define a minimal version
try:
    from engine.item.item import Item
except ImportError:
    @dataclass
    class Item:
        """Simplified Item class to use if the real one isn't available"""
        id: str
        name: str
        item_type: str  # "armor", "weapon", "equipment"
        weight: int = 1
        properties: Dict[str, Any] = field(default_factory=dict)


class TUnitInventory:
    """
    Inventory management for a single unit.

    This class manages equipment slots for a unit, including armor, weapon,
    and up to 4 equipment slots. The availability of equipment slots is
    determined by the equipped armor.

    Purpose:
        Provides a complete inventory management system for unit equipment.

    Interactions:
        - Owned by TUnit to manage its equipment
        - Holds Item objects (armor, weapons, equipment)
        - Affects TUnitStats through equipment bonuses
        - Interacts with combat systems through equipped items' capabilities
        - Provides weight calculations that may affect unit movement

    Attributes:
        armor_slot: Current armor item (or None if empty)
        weapon_slot: Current weapon item (or None if empty)
        equipment_slots: List of up to 4 equipment items (None for empty slots)
        available_equipment_slots: Number of currently available equipment slots
    """

    def __init__(self):
        """Initialize an empty inventory with default slot configuration"""
        self.armor_slot: Optional[Item] = None
        self.weapon_slot: Optional[Item] = None
        self.equipment_slots: List[Optional[Item]] = [None, None, None, None]  # Always 4 slots (enabled/disabled separately)
        self.available_equipment_slots: int = 2  # Default is 2 equipment slots

    @property
    def total_weight(self) -> int:
        """Calculate total weight of all equipped items"""
        weight = 0

        if self.armor_slot:
            weight += self.armor_slot.weight

        if self.weapon_slot:
            weight += self.weapon_slot.weight

        # Only count equipment in available slots
        for i in range(self.available_equipment_slots):
            if self.equipment_slots[i]:
                weight += self.equipment_slots[i].weight

        return weight

    def is_slot_empty(self, slot_type: str, index: int = 0) -> bool:
        """
        Check if a specific slot is empty.

        Args:
            slot_type: Type of slot ('armor', 'weapon', or 'equipment')
            index: Index for equipment slots (0-3), ignored for other types

        Returns:
            True if the slot is empty, False otherwise
        """
        if slot_type.lower() == 'armor':
            return self.armor_slot is None
        elif slot_type.lower() == 'weapon':
            return self.weapon_slot is None
        elif slot_type.lower() == 'equipment':
            if index < 0 or index >= len(self.equipment_slots):
                return True  # Out of range slots are considered empty
            return self.equipment_slots[index] is None
        else:
            raise ValueError(f"Unknown slot type: {slot_type}")

    def can_accept_item(self, item: Item, slot_type: str, index: int = 0) -> bool:
        """
        Check if an item can be placed in the specified slot.

        Args:
            item: Item to check
            slot_type: Type of slot ('armor', 'weapon', or 'equipment')
            index: Index for equipment slots (0-3), ignored for other types

        Returns:
            True if the item can be placed in the slot, False otherwise
        """
        # Check appropriate type for each slot
        if slot_type.lower() == 'armor':
            return item.item_type.lower() == 'armor' or item.item_type.lower() == 'armour'
        elif slot_type.lower() == 'weapon':
            return item.item_type.lower() == 'weapon'
        elif slot_type.lower() == 'equipment':
            # Check if equipment slot is available based on index
            if index < 0 or index >= self.available_equipment_slots:
                return False  # Out of range or disabled slots can't accept items
            return item.item_type.lower() == 'equipment'
        else:
            return False

    def add_item(self, item: Item, slot_type: str, index: int = 0) -> Tuple[bool, Optional[Item]]:
        """
        Add an item to the specified slot.

        Args:
            item: Item to add
            slot_type: Type of slot ('armor', 'weapon', or 'equipment')
            index: Index for equipment slots (0-3), ignored for other types

        Returns:
            Tuple of (success, replaced_item). If the slot was occupied,
            the replaced item is returned; otherwise None is returned.
        """
        if not self.can_accept_item(item, slot_type, index):
            return False, None

        replaced_item = None

        # Handle each slot type
        if slot_type.lower() == 'armor':
            replaced_item = self.armor_slot
            self.armor_slot = item

            # Update available equipment slots based on armor
            self._update_equipment_slots()

        elif slot_type.lower() == 'weapon':
            replaced_item = self.weapon_slot
            self.weapon_slot = item

        elif slot_type.lower() == 'equipment':
            # Skip if index is out of range for available slots
            if index < 0 or index >= self.available_equipment_slots:
                return False, None

            replaced_item = self.equipment_slots[index]
            self.equipment_slots[index] = item

        return True, replaced_item

    def remove_item(self, slot_type: str, index: int = 0) -> Optional[Item]:
        """
        Remove an item from the specified slot.

        Args:
            slot_type: Type of slot ('armor', 'weapon', or 'equipment')
            index: Index for equipment slots (0-3), ignored for other types

        Returns:
            The removed item, or None if the slot was already empty
        """
        removed_item = None

        # Handle each slot type
        if slot_type.lower() == 'armor':
            removed_item = self.armor_slot
            self.armor_slot = None

            # Reset equipment slots to default when armor is removed
            self._update_equipment_slots()

        elif slot_type.lower() == 'weapon':
            removed_item = self.weapon_slot
            self.weapon_slot = None

        elif slot_type.lower() == 'equipment':
            # Skip if index is out of range for available slots
            if index < 0 or index >= len(self.equipment_slots):
                return None

            removed_item = self.equipment_slots[index]
            self.equipment_slots[index] = None

        return removed_item

    def auto_equip(self, item: Item) -> Tuple[bool, str, int]:
        """
        Automatically equip an item in the first available slot of appropriate type.

        Args:
            item: Item to equip

        Returns:
            Tuple of (success, slot_type, index) indicating where the item was placed
        """
        if item.item_type.lower() in ('armor', 'armour'):
            if self.is_slot_empty('armor'):
                success, _ = self.add_item(item, 'armor')
                return success, 'armor', 0

        elif item.item_type.lower() == 'weapon':
            if self.is_slot_empty('weapon'):
                success, _ = self.add_item(item, 'weapon')
                return success, 'weapon', 0

        elif item.item_type.lower() == 'equipment':
            # Try to find first empty equipment slot
            for i in range(self.available_equipment_slots):
                if self.is_slot_empty('equipment', i):
                    success, _ = self.add_item(item, 'equipment', i)
                    return success, 'equipment', i

        # No suitable slot found
        return False, '', -1

    def _update_equipment_slots(self):
        """
        Update the number of available equipment slots based on equipped armor.

        When armor changes, this adjusts the number of available equipment slots
        and removes items from slots that are no longer available.
        """
        old_slots = self.available_equipment_slots

        # Determine new slot count
        if self.armor_slot is None:
            # Default is 2 slots when no armor is equipped
            self.available_equipment_slots = 2
        else:
            # Get equipment_slots from armor properties, default to 2 if not specified
            self.available_equipment_slots = self.armor_slot.properties.get('equipment_slots', 2)

            # Ensure value is within valid range (1-4)
            self.available_equipment_slots = max(1, min(4, self.available_equipment_slots))

        # Handle removal of items from disabled slots
        if self.available_equipment_slots < old_slots:
            # Return items from slots that are no longer available
            for i in range(self.available_equipment_slots, old_slots):
                if self.equipment_slots[i] is not None:
                    # In a real implementation, these items would be returned to inventory
                    # For now, we just clear the slots
                    self.equipment_slots[i] = None

    def get_template(self) -> Dict[str, Any]:
        """
        Create a template of the current equipment configuration.

        Returns:
            Dictionary mapping slot names to item names (or None for empty slots)
        """
        template = {
            'armor': self.armor_slot.name if self.armor_slot else None,
            'weapon': self.weapon_slot.name if self.weapon_slot else None,
            'equipment': []
        }

        # Add all equipment slots (only including available ones)
        for i in range(self.available_equipment_slots):
            item = self.equipment_slots[i]
            template['equipment'].append(item.name if item else None)

        return template

    def apply_template(self, template: Dict[str, Any], item_provider) -> List[Tuple[str, str]]:
        """
        Apply an equipment template, using the provided item_provider to get items by name.

        Args:
            template: Dictionary mapping slot names to item names
            item_provider: Function that returns an Item object given a name

        Returns:
            List of tuples (slot_description, error_message) for any slots that couldn't be filled
        """
        errors = []

        # Start with a clean inventory
        self.clear_all()

        # Apply armor first (this affects available equipment slots)
        armor_name = template.get('armor')
        if armor_name:
            try:
                armor_item = item_provider(armor_name)
                if not self.add_item(armor_item, 'armor')[0]:
                    errors.append(('armor', f"Couldn't equip {armor_name}"))
            except Exception as e:
                errors.append(('armor', f"Error equipping {armor_name}: {str(e)}"))

        # Apply weapon
        weapon_name = template.get('weapon')
        if weapon_name:
            try:
                weapon_item = item_provider(weapon_name)
                if not self.add_item(weapon_item, 'weapon')[0]:
                    errors.append(('weapon', f"Couldn't equip {weapon_name}"))
            except Exception as e:
                errors.append(('weapon', f"Error equipping {weapon_name}: {str(e)}"))

        # Apply equipment
        equipment_names = template.get('equipment', [])
        for i, equip_name in enumerate(equipment_names):
            if equip_name and i < self.available_equipment_slots:
                try:
                    equip_item = item_provider(equip_name)
                    if not self.add_item(equip_item, 'equipment', i)[0]:
                        errors.append((f'equipment_{i}', f"Couldn't equip {equip_name}"))
                except Exception as e:
                    errors.append((f'equipment_{i}', f"Error equipping {equip_name}: {str(e)}"))

        return errors

    def clear_all(self):
        """Remove all items from all slots"""
        self.armor_slot = None
        self.weapon_slot = None
        self.equipment_slots = [None, None, None, None]
        self.available_equipment_slots = 2  # Reset to default

    def get_all_items(self) -> List[Item]:
        """
        Get a list of all equipped items.

        Returns:
            List of all non-None items in all slots
        """
        items = []

        if self.armor_slot:
            items.append(self.armor_slot)

        if self.weapon_slot:
            items.append(self.weapon_slot)

        # Only include equipment from available slots
        for i in range(self.available_equipment_slots):
            if self.equipment_slots[i]:
                items.append(self.equipment_slots[i])

        return items

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert inventory to a dictionary for serialization.

        Returns:
            Dictionary representation of the inventory
        """
        result = {
            'armor': self.armor_slot.to_dict() if self.armor_slot else None,
            'weapon': self.weapon_slot.to_dict() if self.weapon_slot else None,
            'equipment_slots': [],
            'available_equipment_slots': self.available_equipment_slots
        }

        # Include all equipment slots
        for item in self.equipment_slots:
            if item:
                result['equipment_slots'].append(item.to_dict())
            else:
                result['equipment_slots'].append(None)

        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any], item_factory) -> 'TUnitInventory':
        """
        Create a UnitInventory from a dictionary representation.

        Args:
            data: Dictionary containing inventory data
            item_factory: Function that creates an Item from a dictionary

        Returns:
            New UnitInventory instance
        """
        inventory = cls()

        # Load armor
        if data.get('armor'):
            inventory.armor_slot = item_factory(data['armor'])

        # Load weapon
        if data.get('weapon'):
            inventory.weapon_slot = item_factory(data['weapon'])

        # Set available equipment slots (do this before loading equipment)
        inventory.available_equipment_slots = data.get('available_equipment_slots', 2)

        # Load equipment
        equipment_data = data.get('equipment_slots', [])
        for i, item_data in enumerate(equipment_data):
            if i < 4 and item_data:  # Ensure we don't exceed 4 slots
                inventory.equipment_slots[i] = item_factory(item_data)

        return inventory
