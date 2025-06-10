"""
A specialized inventory slot for unit equipment items.

This class extends the base inventory slot with unit-specific functionality.
It handles equipping and unequipping items on soldiers/units, including
validation of item compatibility with unit stats and traits.

Key Features:
- Unit-specific item validation
- Updates unit stats when equipment changes
- Handles specialized equipment types (weapons, armor, etc.)
- Visual feedback for unit compatibility
"""

from typing import Optional, Dict
from PySide6.QtCore import Signal

from item.item import TItem
from unit.unit import TUnit
from gui.other.slots.inventory_slot import TInventorySlot


class TUnitInventorySlot(TInventorySlot):
    """
    Specialized inventory slot for unit equipment with unit-specific functionality.
    """

    # Signal emitted when unit's stats change due to equipment
    statsChanged = Signal(object)  # Emits unit object when stats change

    def __init__(
        self,
        parent=None,
        slot_type=None,
        slot_name="",
        size=64,
        border_width=2,
        accept_types=None,
        bg_color="#1E2836",
        border_color="#30465d",
        hover_color="#3399ff",
        locked=False
    ):
        """Initialize unit inventory slot with custom properties."""
        super().__init__(
            parent=parent,
            slot_type=slot_type,
            slot_name=slot_name,
            size=size,
            border_width=border_width,
            accept_types=accept_types,
            bg_color=bg_color,
            border_color=border_color,
            hover_color=hover_color,
            locked=locked
        )

        # Unit-specific properties
        self.unit: Optional[TUnit] = None
        self.stat_modifiers: Dict[str, int] = {}
        self.requirements: Dict[str, int] = {}  # Item requirements (e.g., strength)

    def set_unit(self, unit: TUnit):
        """Associate this slot with a specific unit."""
        self.unit = unit

        # Update slot validation based on unit capabilities
        self.update_unit_restrictions()

    def update_unit_restrictions(self):
        """Update slot restrictions based on current unit stats and traits."""
        if not self.unit:
            return

        # Example: Disable slot if unit doesn't meet strength requirements
        required_strength = self.requirements.get('strength', 0)
        unit_strength = getattr(self.unit, 'strength', None)
        if (required_strength > 0 and unit_strength is not None and unit_strength < required_strength):
            self.setEnabled(False)
            self.setToolTip(f"Requires {required_strength} strength")
        else:
            self.setEnabled(True)
            self.setToolTip(f"{self.slot_name}")

    def can_accept_item(self, item) -> bool:
        """
        Override to check unit-specific restrictions.

        Args:
            item: Item to validate for this slot

        Returns:
            True if the unit can equip this item in this slot
        """
        # First do base validation
        if not super().can_accept_item(item):
            return False

        # Check unit-specific restrictions
        if self.unit and hasattr(item, 'requirements'):
            # Check strength requirement
            required_strength = item.requirements.get('strength', 0)
            unit_strength = getattr(self.unit, 'strength', None)
            if (required_strength > 0 and unit_strength is not None and unit_strength < required_strength):
                return False

            # Check other stat requirements as needed
            # e.g., psi strength, accuracy requirements, etc.

        return True

    def add_item(self, item: TItem, quantity: int = 1, emit_signal: bool = True) -> bool:
        """
        Add an item to this slot with unit-specific effects.

        Args:
            item: Item to add to the slot
            quantity: Quantity to add (for stackable items)
            emit_signal: Whether to emit the itemChanged signal

        Returns:
            True if the item was successfully added
        """
        # Call the parent method first
        if not super().add_item(item, quantity, False):  # Don't emit yet
            return False

        # Apply item effects to unit
        if self.unit and hasattr(item, 'stat_modifiers'):
            for stat, value in item.stat_modifiers.items():
                if hasattr(self.unit, stat):
                    old_value = getattr(self.unit, stat)
                    setattr(self.unit, stat, old_value + value)

            # Store modifiers for later unapplying
            self.stat_modifiers = getattr(item, 'stat_modifiers', {})

            # Emit unit stats changed signal
            self.statsChanged.emit(self.unit)

        # Now emit the regular item changed signal if requested
        if emit_signal:
            self.itemChanged.emit(self.item)

        return True

    def remove_item(self, quantity: Optional[int] = None, emit_signal: bool = True) -> Optional[TItem]:
        """
        Remove and return the current item, reverting unit stat changes.

        Args:
            quantity: Quantity to remove (None = all)
            emit_signal: Whether to emit the itemChanged signal

        Returns:
            The removed item or None if slot was empty
        """
        # Get the item before removing it
        item_to_remove = self.item

        # Call parent remove method
        removed_item = super().remove_item(quantity, False)  # Don't emit yet

        if removed_item and self.unit:
            # Unapply stat modifiers
            for stat, value in self.stat_modifiers.items():
                if hasattr(self.unit, stat):
                    old_value = getattr(self.unit, stat)
                    setattr(self.unit, stat, old_value - value)

            # Clear stored modifiers
            self.stat_modifiers = {}

            # Emit unit stats changed signal
            self.statsChanged.emit(self.unit)

        # Now emit the regular item changed signal if requested
        if emit_signal and removed_item:
            self.itemChanged.emit(None)

        return removed_item

    def set_requirements(self, requirements: Dict[str, int]):
        """
        Set stat requirements for this equipment slot.

        Args:
            requirements: Dictionary of stat name to minimum value
        """
        self.requirements = requirements

        # Update restrictions immediately if a unit is set
        if self.unit:
            self.update_unit_restrictions()
