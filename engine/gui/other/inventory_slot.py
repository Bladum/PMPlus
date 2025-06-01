"""
A customizable slot component that can hold and display game items.

This class provides an interactive slot for equipment items with support for
drag and drop operations, item type restrictions, and visual customization.
It forms the foundation of equipment screens, loadout interfaces, and inventory
grids throughout the game UI.

Interactions:
- Communicates with TItemTransferManager for drag and drop operations
- Validates item type compatibility with defined slot restrictions
- Connects with inventory systems for item movement
- Emits signals when items are added, removed, or interacted with
- Responds to armor changes by updating slot availability

Key Features:
- Type-restricted slots (armor, weapon, equipment, etc.)
- Visual customization through colors and borders
- Drag and drop with validation
- Stack management for stackable items
- Detailed tooltip display with item information
- Lock functionality to prevent item removal
- Right-click return to inventory functionality
"""

import json
from typing import Optional, Dict, Any, List, Callable, Union
from enum import Enum

from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel,
    QSizePolicy, QToolTip, QApplication
)
from PySide6.QtCore import Qt, QSize, QPoint, QMimeData, Signal
from PySide6.QtGui import (
    QDrag, QPainter, QPixmap, QPen, QColor, QBrush,
    QFont, QFontMetrics, QCursor, QDragEnterEvent, QDropEvent, QMouseEvent
)

# Import the item types from the game's inventory system
from engine.gui.widgets import ItemType

# Import global inventory slot registry
from engine.gui.widgets import equipment_slots_global

# Import functions for armor-dependent slots
from engine.gui.widgets import validate_and_update_equipment_slots, update_weight_display


class TInventorySlot(QFrame):


    # Signals for slot events
    itemChanged = Signal(object)  # Emits item or None when changed
    itemDropped = Signal(object, int)  # Emits (item, quantity) when dropped
    rightClicked = Signal(object)  # Emits item or None when right-clicked

    def __init__(
        self,
        parent=None,
        slot_type: Optional[ItemType] = None,
        slot_name: str = "",
        size: int = 64,
        border_width: int = 2,
        accept_types: List[ItemType] = None,
        bg_color: str = "#1E2836",
        border_color: str = "#30465d",
        hover_color: str = "#3399ff",
        locked: bool = False
    ):
        """
        Initialize an inventory slot with custom properties.

        Args:
            parent: Parent widget
            slot_type: Type restriction for this slot (None allows any type)
            slot_name: Display name for the slot
            size: Size of the slot in pixels
            border_width: Width of the slot border in pixels
            accept_types: List of item types this slot accepts (None = accept all)
            bg_color: Background color for empty slot
            border_color: Border color for empty slot
            hover_color: Color to show when hovering
            locked: Whether items can be removed from this slot
        """
        super().__init__(parent)

        # Slot properties
        self.slot_name = slot_name or (slot_type.value if slot_type else "Any")
        self.slot_type = slot_type  # ItemType enum (or None for any type)
        self.accept_types = accept_types or []  # Additional acceptable types
        self.locked = locked  # If True, items can't be removed

        # Item storage
        self.item: Optional[Item] = None
        self.stack_size: int = 0
        self.custom_data: Dict[str, Any] = {}  # For any extra data

        # Visual properties
        self._size = size
        self._border_width = border_width
        self._bg_color = bg_color
        self._border_color = border_color
        self._original_border_color = border_color
        self._hover_color = hover_color
        self._enabled = True  # Whether the slot is interactive

        # Setup widget properties
        self.setFixedSize(size, size)
        self.setFrameShape(QFrame.Box)
        self.setLineWidth(border_width)
        self.setAcceptDrops(True)
        self.setMouseTracking(True)

        # Layout for icon and label
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(2, 2, 2, 2)
        self.layout.setSpacing(0)

        # Item icon/name label
        self.item_label = QLabel(self)
        self.item_label.setAlignment(Qt.AlignCenter)
        self.item_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.item_label.setStyleSheet("background-color: transparent;")
        self.layout.addWidget(self.item_label)

        # Quantity label (for stackable items)
        self.quantity_label = QLabel(self)
        self.quantity_label.setAlignment(Qt.AlignBottom | Qt.AlignRight)
        self.quantity_label.setStyleSheet(
            "color: white; font-weight: bold; font-size: 10px; background-color: rgba(0,0,0,80%);"
        )
        self.quantity_label.setMargin(1)
        self.layout.addWidget(self.quantity_label)

        # Apply initial styling
        self.update_appearance()

        # Register with global registry for armor-dependent validation
        if self not in equipment_slots_global and self.slot_type:
            equipment_slots_global.append(self)

        # Create label above the slot for better identification (based on EquipmentSlotWidget)
        label_text = slot_name or (slot_type.value if slot_type else "Any")
        self.top_label = QLabel(label_text, parent)
        self.top_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.top_label.setStyleSheet("color: #607080; font-size: 8px; background: transparent;")
        self.top_label.setFixedSize(size, 12)

    def move(self, x: int, y: int) -> None:
        """Move widget and position label above it."""
        super().move(x, y)
        # Position label above the slot (like EquipmentSlotWidget)
        if hasattr(self, 'top_label'):
            self.top_label.move(x, y - self.top_label.height() - 2)

    def add_item(self, item: Item, quantity: int = 1, emit_signal: bool = True) -> bool:
        """
        Add an item to this slot if validation passes.

        Args:
            item: Item to add to the slot
            quantity: Quantity to add (for stackable items)
            emit_signal: Whether to emit the itemChanged signal

        Returns:
            True if the item was successfully added
        """
        if not self.can_accept_item(item):
            return False

        # If slot is empty, add the item
        if self.item is None:
            self.item = item
            self.stack_size = max(1, quantity)  # Ensure at least 1
        # Otherwise if it's the same item and stackable, increase quantity
        elif self.item.id == item.id and self.is_stackable(item):
            max_stack = self.get_max_stack_size(item)
            self.stack_size = min(self.stack_size + quantity, max_stack)
        else:
            return False

        # Update visuals and emit signal if requested
        self.update_appearance()
        if emit_signal:
            self.itemChanged.emit(self.item)

        # Special handling for armor items - update equipment slots availability
        if self.slot_type == ItemType.ARMOUR:
            validate_and_update_equipment_slots()

        # Update weight display
        update_weight_display()

        return True

    def remove_item(self, quantity: Optional[int] = None, emit_signal: bool = True) -> Optional[Item]:
        """
        Remove and return the current item.

        Args:
            quantity: Quantity to remove (None = all)
            emit_signal: Whether to emit the itemChanged signal

        Returns:
            The removed item or None if slot was empty
        """
        # Can't remove from locked slots
        if self.locked:
            return None

        # Can't remove if empty
        if self.item is None:
            return None

        removed_item = self.item
        was_armor = self.slot_type == ItemType.ARMOUR

        # If removing partial stack
        if quantity is not None and quantity < self.stack_size:
            self.stack_size -= quantity
            self.update_appearance()
            return removed_item

        # Otherwise remove entire stack/item
        self.item = None
        self.stack_size = 0
        self.update_appearance()

        if emit_signal:
            self.itemChanged.emit(None)

        # Special handling for removed armor - update equipment slots availability
        if was_armor:
            validate_and_update_equipment_slots()

        # Update weight display
        update_weight_display()

        return removed_item

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Handle mouse press events."""
        if event.button() == Qt.LeftButton:
            if self._enabled and self.item and not self.locked:
                # Start drag operation
                self.start_drag()
        elif event.button() == Qt.RightButton:
            # Add right-click to move to inventory (from EquipmentSlotWidget)
            if self._enabled and self.item and not self.locked:
                self.move_to_inventory()

            # Still emit right-click signal for external handlers
            self.rightClicked.emit(self.item)

        super().mousePressEvent(event)

    def move_to_inventory(self) -> None:
        """Move item from slot to inventory (right-click functionality)."""
        # Import globals from main_interface module to ensure proper access
        try:
            import main_interface
            item_list_widget_global = main_interface.item_list_widget_global if hasattr(main_interface, 'item_list_widget_global') else None

            if self.item and item_list_widget_global and hasattr(item_list_widget_global, 'add_item_to_inventory'):
                item = self.remove_item()
                item_list_widget_global.add_item_to_inventory(item, self.stack_size)
                print(f"Moved {item.name} back to inventory via right-click")
            else:
                print(f"Cannot move item: item={self.item is not None}, item_list_widget={item_list_widget_global is not None}")
        except (ImportError, AttributeError) as e:
            print(f"Could not move item to inventory: {e}")

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        """Handle drag enter with visual feedback."""
        if not self._enabled:
            event.ignore()
            return

        if event.mimeData().hasText():
            try:
                # Parse the drag data
                data = json.loads(event.mimeData().text())

                # Get the item data
                item_data = data.get('item', {})
                if not item_data:
                    event.ignore()
                    return

                # Create Item instance from data
                if hasattr(Item, 'from_dict'):
                    item = Item.from_dict(item_data)
                else:
                    item = Item(
                        id=item_data.get('id', ''),
                        name=item_data.get('name', ''),
                        item_type=item_data.get('item_type', 'other')
                    )

                # Get source slot to prevent dragging to itself
                source_slot_id = data.get('source_slot')
                if source_slot_id == id(self):
                    event.ignore()
                    return

                # Check if this slot can accept the item
                if self.can_accept_item(item):
                    event.acceptProposedAction()
                    # Visual feedback - valid drop (green border like EquipmentSlotWidget)
                    self.setStyleSheet(self.styleSheet().replace(
                        self._border_color, "#44CC44"  # Green for valid drop
                    ))
                else:
                    event.ignore()
                    # Visual feedback - invalid drop (red border like EquipmentSlotWidget)
                    self.setStyleSheet(self.styleSheet().replace(
                        self._border_color, "#CC4444"  # Red for rejection
                    ))
            except (json.JSONDecodeError, KeyError, TypeError):
                event.ignore()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent) -> None:
        """Handle item drop into this slot."""
        if not self._enabled:
            event.ignore()
            return

        try:
            # Parse the dropped data
            data = json.loads(event.mimeData().text())

            # Get the item data and quantity
            item_data = data.get('item', {})
            quantity = int(data.get('quantity', 1))

            if not item_data:
                event.ignore()
                return

            # Create Item instance from data
            if hasattr(Item, 'from_dict'):
                item = Item.from_dict(item_data)
            else:
                item = Item(
                    id=item_data.get('id', ''),
                    name=item_data.get('name', ''),
                    item_type=item_data.get('item_type', 'other')
                )

            # Check if we can accept this item
            if self.can_accept_item(item):
                # Check for item replacement (same category, different item) - from EquipmentSlotWidget
                if self.item and self.item.item_type == item.item_type:
                    # Replace items - move current item to inventory
                    old_item = self.remove_item()
                    if old_item:
                        # Import globals from main_interface module to ensure proper access
                        try:
                            import main_interface
                            item_list_widget_global = main_interface.item_list_widget_global if hasattr(main_interface, 'item_list_widget_global') else None
                            if item_list_widget_global and hasattr(item_list_widget_global, 'add_item_to_inventory'):
                                item_list_widget_global.add_item_to_inventory(old_item, self.stack_size)
                        except (ImportError, AttributeError):
                            pass

                # Handle the drop
                self.add_item(item, quantity)
                event.acceptProposedAction()

                # Emit itemDropped signal
                self.itemDropped.emit(item, quantity)
            else:
                event.ignore()
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            print(f"Error in dropEvent: {e}")
            event.ignore()

        # Restore appearance
        self.update_appearance()

    def update_appearance(self) -> None:
        """Update the slot's appearance based on its current state."""
        # Reset style based on whether the slot is enabled
        if not self._enabled:
            border_color = "#555555"  # Gray border for disabled slots
            bg_color = "#333333"      # Dark background for disabled slots
        else:
            border_color = self._original_border_color
            bg_color = self._bg_color

        # Create style sheet for the frame
        self.setStyleSheet(f"""
            QFrame {{
                border: {self._border_width}px solid {border_color};
                border-radius: 4px;
                background-color: {bg_color};
            }}
        """)

        # Update item display
        if self.item:
            # Get or create item icon
            if hasattr(self.item, 'get_pixmap'):
                pixmap = self.item.get_pixmap(self._size - 10)
            elif hasattr(self.item, 'icon_path') and self.item.icon_path:
                pixmap = QPixmap(self.item.icon_path).scaled(self._size - 10, self._size - 10,
                                                            Qt.KeepAspectRatio,
                                                            Qt.SmoothTransformation)
            else:
                # Create a colored rectangle as placeholder
                pixmap = QPixmap(self._size - 10, self._size - 10)
                pixmap.fill(Qt.transparent)
                painter = QPainter(pixmap)
                painter.setPen(QPen(QColor("#CCCCCC")))
                painter.setBrush(QBrush(QColor(self.item.color if hasattr(self.item, 'color') else "#7788AA")))
                painter.drawRoundedRect(0, 0, self._size - 10, self._size - 10, 5, 5)
                painter.end()

            self.item_label.setPixmap(pixmap)

            # Update quantity label for stackable items
            if self.stack_size > 1:
                self.quantity_label.setText(str(self.stack_size))
                self.quantity_label.show()
            else:
                self.quantity_label.hide()
        else:
            # Clear displays when no item
            self.item_label.clear()
            self.quantity_label.hide()

        # Additional visual cue for locked slots
        if self.locked and self.item:
            # Add a small lock indicator in the corner
            lock_overlay = QPixmap(16, 16)
            lock_overlay.fill(Qt.transparent)
            painter = QPainter(lock_overlay)
            painter.setPen(QPen(QColor("#FFCC00")))
            painter.setBrush(QBrush(QColor("#886600")))
            painter.drawEllipse(2, 2, 12, 12)
            painter.setPen(QPen(QColor("#FFCC00"), 2))
            painter.drawLine(8, 6, 8, 10)
            painter.drawPoint(8, 12)
            painter.end()

            # Get current pixmap and overlay the lock
            current_pixmap = self.item_label.pixmap()
            if current_pixmap:
                painter = QPainter(current_pixmap)
                painter.drawPixmap(current_pixmap.width() - 16, 0, lock_overlay)
                painter.end()
                self.item_label.setPixmap(current_pixmap)

    def can_accept_item(self, item) -> bool:
        """
        Check if this slot can accept the given item.

        Args:
            item: Item to validate for this slot

        Returns:
            True if the slot can accept this item
        """
        # Can't accept items when disabled
        if not self._enabled:
            return False

        # Can't accept if slot is locked and already has an item
        if self.locked and self.item:
            return False

        # Check type compatibility
        if self.slot_type is not None:
            # If item type matches slot type directly
            if hasattr(item, 'item_type') and item.item_type == self.slot_type:
                pass  # Type match
            # If item type is in accept_types list
            elif hasattr(item, 'item_type') and self.accept_types and item.item_type in self.accept_types:
                pass  # Type in accepted list
            # Otherwise reject
            else:
                return False

        # If slot already has an item, we must check stack compatibility
        if self.item:
            # Must be same item type and stackable
            return self.item.id == item.id and self.is_stackable(item) and self.stack_size < self.get_max_stack_size(item)

        # Otherwise accept
        return True

    def is_stackable(self, item) -> bool:
        """
        Check if the item can be stacked in this slot.

        Args:
            item: Item to check for stacking

        Returns:
            True if the item can be stacked
        """
        # Honor slot-specific stacking rules first
        if hasattr(self, 'stackable') and not self.stackable:
            return False

        # Check item-specific stacking rules
        if hasattr(item, 'stackable'):
            return item.stackable

        # Default to standard type-based rules
        if hasattr(item, 'item_type'):
            # Weapons and armor typically can't stack
            if item.item_type in [ItemType.WEAPON, ItemType.ARMOUR]:
                return False

        # Default to not stackable for safety
        return False

    def get_max_stack_size(self, item) -> int:
        """
        Get the maximum stack size for this item in this slot.

        Args:
            item: Item to get max stack size for

        Returns:
            Maximum number of items that can be stacked
        """
        # Check item's specific stack limit first
        if hasattr(item, 'max_stack'):
            return item.max_stack

        # Default limits based on type
        if hasattr(item, 'item_type'):
            if item.item_type == ItemType.EQUIPMENT:
                return 5

        # Global default
        return 99
