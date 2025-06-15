"""
engine/gui/other/slots/craft_inventory_slot.py

Specialized inventory slot for craft equipment items in the XCOM GUI.

Classes:
    TCraftInventorySlot: Inventory slot for craft components with craft-specific functionality.

Last standardized: 2025-06-15
"""

from typing import Optional, Dict, Any
from PySide6.QtCore import Signal
from gui.other.slots.inventory_slot import TInventorySlot
from item.item import TItem
from item.item_type import TItemType
from craft.craft import TCraft


class TCraftInventorySlot(TInventorySlot):
    """
    Inventory slot for craft components with craft-specific functionality.

    Attributes:
        statsChanged (Signal): Emitted when craft stats change.
        systemsChanged (Signal): Emitted when a craft system changes.

    Methods:
        __init__(...): Initialize the slot with custom properties.
        set_craft(...): Associate this slot with a specific craft.
        set_hardpoint_type(...): Set the type of hardpoint this slot represents.
        update_craft_compatibility(): Update slot restrictions based on current craft specifications.
        can_accept_item(...): Check if an item can be accepted in this slot.
        add_item(...): Add an component to this slot with craft-specific effects.
        remove_item(...): Remove and return the current component, reverting craft stat changes.
        set_compatibility(...): Set compatibility requirements for this component slot.
    """

    # Signal emitted when craft's stats change due to component changes
    statsChanged = Signal(object)  # Emits craft object when stats change
    systemsChanged = Signal(str)   # Emits system name that changed

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
        """
        Initialize craft inventory slot with custom properties.

        Args:
            parent: Parent widget.
            slot_type: Type of slot (e.g., weapon, engine).
            slot_name: Name of the slot.
            size: Size of the slot in pixels.
            border_width: Border width in pixels.
            accept_types: List of accepted item types.
            bg_color: Background color.
            border_color: Border color.
            hover_color: Hover color.
            locked: If True, slot is locked.
        """
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

        # Craft-specific properties
        self.craft: Optional[TCraft] = None
        self.stat_modifiers: Dict[str, int] = {}
        self.compatibility: Dict[str, Any] = {}  # Compatibility requirements
        self.hardpoint_type: str = ""  # Type of hardpoint (weapon bay, engine mount, etc.)

    def set_craft(self, craft: TCraft):
        """Associate this slot with a specific craft."""
        self.craft = craft

        # Update slot validation based on craft specifications
        self.update_craft_compatibility()

    def set_hardpoint_type(self, hardpoint_type: str):
        """
        Set the type of hardpoint this slot represents.

        Args:
            hardpoint_type: Type of hardpoint (e.g., "weapon_bay", "engine_mount")
        """
        self.hardpoint_type = hardpoint_type

        # Update tooltip to show hardpoint type
        current_tooltip = self.toolTip()
        if current_tooltip:
            self.setToolTip(f"{current_tooltip} ({hardpoint_type})")
        else:
            self.setToolTip(f"{hardpoint_type}")

    def update_craft_compatibility(self):
        """Update slot restrictions based on current craft specifications."""
        if not self.craft:
            return

        # Example: Disable slot if craft doesn't support this component type
        if self.hardpoint_type and not self.craft.has_hardpoint(self.hardpoint_type):
            self.setEnabled(False)
            self.setToolTip(f"Craft does not support {self.hardpoint_type}")
        else:
            self.setEnabled(True)
            self.setToolTip(f"{self.slot_name}")

    def can_accept_item(self, item) -> bool:
        """
        Override to check craft-specific compatibility.

        Args:
            item: Item to validate for this slot

        Returns:
            True if the craft can mount this component in this slot
        """
        # First do base validation
        if not super().can_accept_item(item):
            return False

        # Check craft-specific compatibility
        if self.craft and hasattr(item, 'compatibility'):
            # Check craft type compatibility
            if (hasattr(self.craft, 'craft_type') and
                'craft_type' in item.compatibility and
                self.craft.craft_type not in item.compatibility['craft_type']):
                return False

            # Check size compatibility
            if (hasattr(self.craft, 'size') and
                'min_size' in item.compatibility and
                self.craft.size < item.compatibility['min_size']):
                return False

            # Check hardpoint compatibility
            if (self.hardpoint_type and
                'hardpoint' in item.compatibility and
                self.hardpoint_type not in item.compatibility['hardpoint']):
                return False

        return True

    def add_item(self, item: TItem, quantity: int = 1, emit_signal: bool = True) -> bool:
        """
        Add an component to this slot with craft-specific effects.

        Args:
            item: Component to add to the slot
            quantity: Quantity to add (typically 1 for craft components)
            emit_signal: Whether to emit signals

        Returns:
            True if the component was successfully added
        """
        # Call the parent method first
        if not super().add_item(item, quantity, False):  # Don't emit yet
            return False

        # Apply component effects to craft
        if self.craft and hasattr(item, 'stat_modifiers'):
            for stat, value in item.stat_modifiers.items():
                if hasattr(self.craft, stat):
                    old_value = getattr(self.craft, stat)
                    setattr(self.craft, stat, old_value + value)

            # Store modifiers for later unapplying
            self.stat_modifiers = getattr(item, 'stat_modifiers', {})

            # Add component to craft's internal systems if applicable
            if hasattr(self.craft, 'add_component') and callable(self.craft.add_component):
                self.craft.add_component(item, self.hardpoint_type)

            # Emit craft stats changed signal
            self.statsChanged.emit(self.craft)

        # Emit system changed signal if applicable
        if self.hardpoint_type:
            self.systemsChanged.emit(self.hardpoint_type)

        # Now emit the regular item changed signal if requested
        if emit_signal:
            self.itemChanged.emit(self.item)

        return True

    def remove_item(self, quantity: Optional[int] = None, emit_signal: bool = True) -> Optional[TItem]:
        """
        Remove and return the current component, reverting craft stat changes.

        Args:
            quantity: Quantity to remove (None = all)
            emit_signal: Whether to emit signals

        Returns:
            The removed component or None if slot was empty
        """
        # Get the item before removing it
        item_to_remove = self.item

        # Call parent remove method
        removed_item = super().remove_item(quantity, False)  # Don't emit yet

        if removed_item and self.craft:
            # Unapply stat modifiers
            for stat, value in self.stat_modifiers.items():
                if hasattr(self.craft, stat):
                    old_value = getattr(self.craft, stat)
                    setattr(self.craft, stat, old_value - value)

            # Remove component from craft's internal systems if applicable
            if hasattr(self.craft, 'remove_component') and callable(self.craft.remove_component):
                self.craft.remove_component(removed_item, self.hardpoint_type)

            # Clear stored modifiers
            self.stat_modifiers = {}

            # Emit craft stats changed signal
            self.statsChanged.emit(self.craft)

        # Emit system changed signal if applicable
        if self.hardpoint_type and removed_item:
            self.systemsChanged.emit(self.hardpoint_type)

        # Now emit the regular item changed signal if requested
        if emit_signal and removed_item:
            self.itemChanged.emit(None)

        return removed_item

    def set_compatibility(self, compatibility: Dict[str, Any]):
        """
        Set compatibility requirements for this component slot.

        Args:
            compatibility: Dictionary of compatibility requirements
        """
        self.compatibility = compatibility

        # Update restrictions immediately if a craft is set
        if self.craft:
            self.update_craft_compatibility()
