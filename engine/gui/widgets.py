"""
Custom Widget Classes for XCOM Inventory System

This module contains specialized Qt widgets for the inventory interface:
- EquipmentSlotWidget: Drag-and-drop equipment slots with type validation
- ItemListWidget: Filterable inventory list with stacking support  
- UnitListWidget: Unit selection list with category filtering

All widgets follow the XCOM theme and support the global state management system.
"""

import json
import sys
from typing import Optional, Dict, Any, List
from PySide6.QtCore import Qt, QPoint, QRect, QMimeData
from PySide6.QtGui import (QFont, QPixmap, QColor, QPainter, QDrag, QCursor, 
                          QDragEnterEvent, QDropEvent, QMouseEvent, QPen, 
                          QBrush, QIcon)
from PySide6.QtWidgets import (QListWidget, QListWidgetItem, QAbstractItemView, 
                              QLabel, QWidget, QApplication)

from theme_styles import XcomTheme, XcomStyle, GRID, px, WIDGET_MARGIN, WIDGET_PADDING
from game_data import ItemType, UnitCategory
from inventory_system import InventoryItem, ItemRarity

# Global references for cross-widget communication
# These are set by main_interface.py and used for coordinating state changes
item_list_widget_global: Optional['ItemListWidget'] = None
equipment_slots_global: List['EquipmentSlotWidget'] = []
weight_label_global: Optional[QLabel] = None
unit_inventory_manager_global = None
current_unit_global: Optional[str] = None
unit_info_label_global: Optional[QLabel] = None

def update_weight_display() -> None:
    """
    Calculate and update the total weight display from equipped items.
    
    Iterates through all equipment slots, sums item weights, and updates
    the weight label. Called whenever items are equipped/unequipped.
    """
    global equipment_slots_global, weight_label_global

    if not weight_label_global or not equipment_slots_global:
        return

    total_weight = sum(slot.item.weight for slot in equipment_slots_global if slot.item)
    weight_label_global.setText(f"Weight: {total_weight}")

def update_equipment_slot_states(enabled_count: int) -> None:
    """
    Enable or disable equipment slots based on equipped armor.
    
    Args:
        enabled_count: Number of equipment slots to enable (from armor properties)
        
    Equipment slots beyond the enabled count are disabled and their items
    are automatically returned to inventory.
    """
    global equipment_slots_global, item_list_widget_global

    print(f"🔧 UPDATE_EQUIPMENT_SLOT_STATES: Starting with enabled_count={enabled_count}")

    if not equipment_slots_global:
        print("❌ UPDATE_EQUIPMENT_SLOT_STATES: No equipment slots available")
        return

    # Filter to only equipment slots (not armor/weapon slots)
    equipment_slots = [slot for slot in equipment_slots_global 
                      if slot.slot_type == ItemType.EQUIPMENT]

    print(f"🔍 UPDATE_EQUIPMENT_SLOT_STATES: Found {len(equipment_slots)} equipment slots")
    for i, slot in enumerate(equipment_slots):
        print(f"🔍 UPDATE_EQUIPMENT_SLOT_STATES: Equipment slot {i}: '{slot.slot_name}' - enabled: {slot.enabled}, has_item: {slot.item is not None}")

    for i, slot in enumerate(equipment_slots):
        print(f"🔧 UPDATE_EQUIPMENT_SLOT_STATES: Processing slot {i}: '{slot.slot_name}'")
        
        if i < enabled_count:
            # Enable slot - accept drops and restore normal appearance
            print(f"✅ UPDATE_EQUIPMENT_SLOT_STATES: Enabling slot {i}: '{slot.slot_name}'")
            slot.enabled = True
            slot.setAcceptDrops(True)
            slot.set_border_color(XcomTheme.BORDER_COLOR)
            slot._original_border_color = XcomTheme.BORDER_COLOR
        else:
            # Disable slot - return item to inventory and gray out
            print(f"❌ UPDATE_EQUIPMENT_SLOT_STATES: Disabling slot {i}: '{slot.slot_name}'")
            slot.enabled = False
            slot.setAcceptDrops(False)
            
            # Move item to inventory if slot has item
            if slot.item:
                print(f"🔧 UPDATE_EQUIPMENT_SLOT_STATES: Moving item '{slot.item.name}' from disabled slot to inventory")
                # Import globals from main_interface module to ensure proper access
                import main_interface
                item_list_widget_global = main_interface.item_list_widget_global if hasattr(main_interface, 'item_list_widget_global') else None
                
                if item_list_widget_global:
                    item = slot.remove_item()
                    item_list_widget_global.add_item_to_inventory(item, 1)
                    print(f"✅ UPDATE_EQUIPMENT_SLOT_STATES: Successfully moved '{item.name}' to inventory")
                else:
                    print("❌ UPDATE_EQUIPMENT_SLOT_STATES: Could not access item_list_widget_global")

            # Set gray appearance for disabled state
            slot.set_border_color(XcomTheme.TEXT_DIM)
            slot._original_border_color = XcomTheme.TEXT_DIM

        slot.update()
        print(f"🔧 UPDATE_EQUIPMENT_SLOT_STATES: Updated slot {i}: '{slot.slot_name}' - enabled: {slot.enabled}")

    print("✅ UPDATE_EQUIPMENT_SLOT_STATES: Completed updating all equipment slots")

def validate_and_update_equipment_slots() -> None:
    """
    Validate and update equipment slots based on currently equipped armor.
    
    This function ensures equipment slots are correctly enabled/disabled based on 
    the current armor's equipment_slots property. It handles all scenarios where
    armor might change and automatically returns displaced items to inventory.
    
    Called whenever:
    - Armor is equipped or unequipped
    - Units are switched 
    - Inventory is loaded
    - Equipment is validated
    """
    global equipment_slots_global, item_list_widget_global
    
    print("🔍 VALIDATE_AND_UPDATE_EQUIPMENT_SLOTS: Starting validation...")
    
    if not equipment_slots_global:
        print("❌ VALIDATE_AND_UPDATE_EQUIPMENT_SLOTS: No equipment slots available for validation")
        return
    
    print(f"🔍 VALIDATE_AND_UPDATE_EQUIPMENT_SLOTS: Found {len(equipment_slots_global)} total equipment slots")
    
    # Find currently equipped armor
    current_armor = None
    armor_slot = None
    for slot in equipment_slots_global:
        print(f"🔍 VALIDATE_AND_UPDATE_EQUIPMENT_SLOTS: Checking slot '{slot.slot_name}' (type: {slot.slot_type}) - has item: {slot.item is not None}")
        if slot.slot_type == ItemType.ARMOUR:
            armor_slot = slot
            if slot.item:
                current_armor = slot.item
                print(f"🔍 VALIDATE_AND_UPDATE_EQUIPMENT_SLOTS: Found armor slot with item: {current_armor.name}")
            else:
                print("🔍 VALIDATE_AND_UPDATE_EQUIPMENT_SLOTS: Found armor slot but it's empty")
            break
    
    if not armor_slot:
        print("❌ VALIDATE_AND_UPDATE_EQUIPMENT_SLOTS: No armor slot found!")
        return
    
    # Determine available equipment slots
    if current_armor:
        available_slots = current_armor.properties.get('equipment_slots', 2)
        print(f"✅ VALIDATE_AND_UPDATE_EQUIPMENT_SLOTS: Armor '{current_armor.name}' provides {available_slots} equipment slots")
        print(f"🔍 VALIDATE_AND_UPDATE_EQUIPMENT_SLOTS: Armor properties: {current_armor.properties}")
    else:
        available_slots = 2  # Default when no armor equipped
        print(f"✅ VALIDATE_AND_UPDATE_EQUIPMENT_SLOTS: No armor equipped - using default {available_slots} equipment slots")
    
    # Update equipment slot states
    print(f"🔧 VALIDATE_AND_UPDATE_EQUIPMENT_SLOTS: Calling update_equipment_slot_states({available_slots})")
    update_equipment_slot_states(available_slots)
    print("✅ VALIDATE_AND_UPDATE_EQUIPMENT_SLOTS: Validation complete")

def test_equipment_slot_validation() -> None:
    """
    Test function to manually trigger equipment slot validation.
    This can be called from the console to debug equipment slot issues.
    """
    print("🧪 TEST_EQUIPMENT_SLOT_VALIDATION: Manual test triggered")
    print(f"🔍 TEST: equipment_slots_global has {len(equipment_slots_global) if equipment_slots_global else 0} slots")
    print(f"🔍 TEST: item_list_widget_global is {'available' if item_list_widget_global else 'None'}")
    
    if equipment_slots_global:
        for i, slot in enumerate(equipment_slots_global):
            print(f"🔍 TEST: Slot {i}: {slot.slot_name} (type: {slot.slot_type}) - has_item: {slot.item is not None} - enabled: {slot.enabled}")
    
    validate_and_update_equipment_slots()
    print("🧪 TEST_EQUIPMENT_SLOT_VALIDATION: Test completed")

class EquipmentSlotWidget(QWidget):
    """
    A custom widget representing an equipment slot that can hold one item.
    
    Features:
    - Drag and drop support with visual feedback
    - Type validation (only accepts compatible item types)
    - Custom painting with rounded borders and item icons
    - Right-click to return items to inventory
    - Enable/disable state for armor-dependent equipment slots
    
    Attributes:
        slot_name: Identifier for this slot
        slot_type: ItemType enum restricting what items can be equipped
        item: Currently equipped InventoryItem or None
        enabled: Whether this slot accepts drops (for equipment slots)
    """
    
    def __init__(self, slot_name: str, parent: Optional[QWidget] = None, 
                 label_text: Optional[str] = None, slot_type: Optional[ItemType] = None):
        """
        Initialize an equipment slot widget.
        
        Args:
            slot_name: Unique identifier for this slot
            parent: Parent widget
            label_text: Text to display above the slot
            slot_type: ItemType that this slot accepts (None = accepts all)
        """
        super().__init__(parent)
        self.slot_name = slot_name
        self.slot_type = slot_type  # ItemType enum value
        self.item: Optional[InventoryItem] = None  # InventoryItem or None
        self.enabled = True  # For equipment slots that can be disabled
        self.setAcceptDrops(True)

        # Make the widget perfectly square and grid-aligned
        self.setFixedSize(px(4 * GRID), px(4 * GRID))

        # Widget style settings
        self._border_radius = 4
        self._border_width = 3
        self._border_color = XcomTheme.BORDER_COLOR
        self._original_border_color = XcomTheme.BORDER_COLOR
        self._bg_color = XcomTheme.BG_LIGHT
        self._icon_size = px(3 * GRID)

        # Create label above the slot
        self.label = QLabel(label_text or slot_name, parent)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_SMALL))
        self.label.setStyleSheet(f"color: {XcomTheme.TEXT_MID}; background: transparent;")
        self.label.setFixedSize(px(4 * GRID), px(GRID // 2))

        # Make widget transparent so our custom painting works properly
        self.setAttribute(Qt.WA_StyledBackground, False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

    def move(self, x: int, y: int) -> None:
        """Move widget and position label above it."""
        super().move(x, y)
        # Position label above the slot
        if hasattr(self, 'label'):
            self.label.move(x, y - px(GRID // 2) - 2)

    def set_background_color(self, color: str) -> None:
        """Set background color and trigger repaint."""
        self._bg_color = color
        self.update()

    def set_border_color(self, color: str) -> None:
        """Set border color and trigger repaint."""
        self._border_color = color
        self._original_border_color = color
        self.update()

    def can_accept_item(self, item: InventoryItem) -> bool:
        """
        Check if this slot can accept the given item.
        
        Args:
            item: InventoryItem to validate
            
        Returns:
            True if item can be equipped in this slot
        """
        if not self.enabled:
            return False

        if self.slot_type and item.item_type != self.slot_type:
            return False

        # Only allow one item per slot - no stacking
        return self.item is None

    def add_item(self, item: InventoryItem) -> bool:
        """
        Add an item to this slot if validation passes.
        
        Args:
            item: InventoryItem to equip
            
        Returns:
            True if item was successfully equipped
        """
        print(f"🔧 ADD_ITEM: Attempting to add '{item.name}' (type: {item.item_type.value}) to slot '{self.slot_name}' (type: {self.slot_type})")
        
        if not self.can_accept_item(item):
            print(f"❌ ADD_ITEM: Item '{item.name}' cannot be accepted by slot '{self.slot_name}'")
            return False

        self.item = item
        self.update()
        print(f"✅ ADD_ITEM: Successfully added '{item.name}' to slot '{self.slot_name}'")

        # Update equipment slots if this is armor - use comprehensive validation
        if self.slot_type == ItemType.ARMOUR:
            print(f"🔧 ADD_ITEM: Armor '{item.name}' was equipped - triggering equipment slot validation")
            validate_and_update_equipment_slots()
        else:
            print(f"🔍 ADD_ITEM: Non-armor item '{item.name}' equipped - no slot validation needed")

        # Update weight display
        update_weight_display()
        return True

    def remove_item(self) -> Optional[InventoryItem]:
        """
        Remove and return the currently equipped item.
        
        Returns:
            The removed InventoryItem or None if slot was empty
        """
        if self.item is None:
            print(f"🔍 REMOVE_ITEM: Slot '{self.slot_name}' is already empty")
            return None

        item = self.item
        was_armor = (self.slot_type == ItemType.ARMOUR)
        print(f"🔧 REMOVE_ITEM: Removing '{item.name}' (type: {item.item_type.value}) from slot '{self.slot_name}' (was_armor: {was_armor})")
        
        self.item = None
        self.update()

        # Reset equipment slots if armor was removed - use comprehensive validation
        if was_armor:
            print(f"🔧 REMOVE_ITEM: Armor '{item.name}' was removed - triggering equipment slot validation")
            validate_and_update_equipment_slots()
        else:
            print(f"🔍 REMOVE_ITEM: Non-armor item '{item.name}' removed - no slot validation needed")

        # Update weight display
        update_weight_display()
        return item

    def set_item(self, item):
        """Legacy method for compatibility"""
        if item:
            self.add_item(item)
        else:
            self.clear_item()

    def clear_item(self):
        """Clear the item from this slot"""
        self.remove_item()

    def paintEvent(self, event) -> None:
        """Custom paint method for slot appearance and item icon."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()

        # Draw widget background and border
        painter.setPen(QPen(QColor(self._border_color), self._border_width))
        painter.setBrush(QBrush(QColor(self._bg_color)))
        painter.drawRoundedRect(self._border_width / 2, self._border_width / 2,
                                w - self._border_width, h - self._border_width,
                                self._border_radius, self._border_radius)

        # Calculate inner area for icon
        slot_rect = QRect(self._border_width * 2, self._border_width * 2,
                          w - 4 * self._border_width,
                          h - 4 * self._border_width)

        if self.item:
            # Draw item icon centered in slot
            pixmap = self.item.get_pixmap(min(slot_rect.width(), slot_rect.height()) - px(8))
            icon_x = slot_rect.x() + (slot_rect.width() - pixmap.width()) // 2
            icon_y = slot_rect.y() + (slot_rect.height() - pixmap.height()) // 2
            painter.drawPixmap(icon_x, icon_y, pixmap)
        else:
            # Draw placeholder for empty slot
            pen = QPen(QColor(self._border_color))
            pen.setStyle(Qt.DashLine)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(slot_rect.adjusted(px(4), px(4), -px(4), -px(4)))

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        """Handle drag enter with validation and visual feedback."""
        if not self.enabled:
            event.ignore()
            return

        if event.mimeData().hasText():
            try:
                data = json.loads(event.mimeData().text())
                item = InventoryItem.from_dict(data['item'])
                source_slot_id = data.get('source_slot')

                # Don't accept drops from the same slot
                if source_slot_id == id(self):
                    event.ignore()
                    return

                if self.can_accept_item(item):
                    event.acceptProposedAction()
                    # Visual feedback - valid drop (green border)
                    self._border_color = XcomTheme.ACCENT_GREEN
                    self.update()
                else:
                    event.ignore()
                    # Visual feedback - invalid drop (red border)
                    self._border_color = XcomTheme.ACCENT_RED
                    self.update()
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Drag enter error: {e}")
                event.ignore()
        else:
            event.ignore()

    def dragLeaveEvent(self, event) -> None:
        """Restore normal appearance when drag leaves."""
        # Restore original border color
        self._border_color = self._original_border_color
        self.update()

    def dropEvent(self, event: QDropEvent) -> None:
        """Handle item drop with replacement logic."""
        if not self.enabled:
            event.ignore()
            return

        try:
            data = json.loads(event.mimeData().text())
            item = InventoryItem.from_dict(data['item'])

            if self.can_accept_item(item):
                # Check for item replacement (same category, different item)
                if self.item and self.item.item_type == item.item_type:
                    # Replace items - move current item to inventory
                    old_item = self.remove_item()
                    if old_item:
                        # Import globals from main_interface module to ensure proper access
                        import main_interface
                        item_list_widget_global = main_interface.item_list_widget_global if hasattr(main_interface, 'item_list_widget_global') else None
                        if item_list_widget_global:
                            item_list_widget_global.add_item_to_inventory(old_item, 1)

                self.add_item(item)
                event.acceptProposedAction()
            else:
                event.ignore()
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Drop error: {e}")
            event.ignore()

        # Restore original border color
        self._border_color = self._original_border_color
        self.update()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Handle left mouse press for dragging."""
        if self.item and self.enabled and event.button() == Qt.MouseButton.LeftButton:
            self.start_drag()
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """Handle right mouse release for item removal."""
        if event.button() == Qt.MouseButton.RightButton and self.item and self.enabled:
            print(f"Right-click detected on slot {self.slot_name} with item {self.item.name}")
            self.move_to_inventory()
        super().mouseReleaseEvent(event)

    def move_to_inventory(self) -> None:
        """Move item from slot to inventory (right-click functionality)."""
        # Import globals from main_interface module to ensure proper access
        import main_interface
        item_list_widget_global = main_interface.item_list_widget_global if hasattr(main_interface, 'item_list_widget_global') else None
        
        if self.item and item_list_widget_global:
            item = self.remove_item()
            item_list_widget_global.add_item_to_inventory(item, 1)
            print(f"Moved {item.name} back to inventory via right-click")
        else:
            print(f"Cannot move item: item={self.item is not None}, item_list_widget={item_list_widget_global is not None}")

    def start_drag(self) -> None:
        """Start dragging this slot's item."""
        if not self.item or not self.enabled:
            return

        # Create drag object
        drag = QDrag(self)
        mime_data = QMimeData()

        # Store item data as JSON
        item_data = {
            'item': self.item.to_dict(),
            'stack_size': 1,
            'source_slot': id(self)
        }
        mime_data.setText(json.dumps(item_data))
        drag.setMimeData(mime_data)

        # Create drag pixmap using the item's icon - scale by 2x
        pixmap = self.item.get_pixmap(128)  # 2x larger (64 -> 128)

        # Add semi-transparent effect to show it's being dragged
        painter = QPainter(pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceAtop)
        painter.fillRect(pixmap.rect(), QColor(255, 255, 255, 150))  # Semi-transparent overlay
        painter.end()

        drag.setPixmap(pixmap)
        drag.setHotSpot(QPoint(64, 64))  # Adjusted for 2x size

        # Hide system cursor during drag
        QApplication.setOverrideCursor(Qt.BlankCursor)

        # Execute drag
        result = drag.exec(Qt.MoveAction)

        # Restore cursor
        QApplication.restoreOverrideCursor()

        if result == Qt.MoveAction:
            # Item was moved, remove from this slot
            self.remove_item()

class ItemListWidget(QListWidget):
    """
    Inventory list widget with filtering, sorting, and drag-and-drop support.
    
    Features:
    - Category-based filtering (All, Armour, Weapon, Equipment, Other)
    - Automatic sorting by category then name
    - Item count tracking and display
    - Drag to equipment slots
    - Right-click auto-equip functionality
    """
    
    def __init__(self, *args, **kwargs):
        """Initialize inventory list with empty state."""
        super().__init__(*args, **kwargs)
        self.item_info: Dict[str, Dict[str, Any]] = {}
        self.item_counts: Dict[str, int] = {}  # Track item quantities
        self.all_items: List[Dict[str, Any]] = []  # Store all items for filtering
        self.current_filter = "All"
        
        # Configure list behavior
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setMouseTracking(True)
        self.setDragDropMode(QAbstractItemView.DragDrop)  # Allow both drag and drop
        
        # Disable scrollbars
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def addItemWithInfo(self, item: QListWidgetItem, info_dict: Dict[str, Any], 
                       count: int = 1) -> None:
        """
        Add an item to the inventory with metadata and count.
        
        Args:
            item: QListWidgetItem with icon and name
            info_dict: Dictionary containing item properties
            count: Initial quantity
        """
        # Import canonical path function
        from item_path_lookup import get_canonical_path
        
        # Extract base name (remove count if present)
        base_name = item.text().split(' (')[0] if ' (' in item.text() else item.text()
        
        # Get the canonical path for this item
        canonical_path = get_canonical_path(base_name)
        
        # Always use the canonical path
        info_dict['icon_path'] = canonical_path
        
        # Set icon using canonical path
        icon = QIcon(QPixmap(canonical_path).scaled(32, 32, Qt.KeepAspectRatio, Qt.FastTransformation))
        item.setIcon(icon)

        # Ensure weight is set
        if 'weight' not in info_dict:
            info_dict['weight'] = 1

        # Store in all_items for filtering
        self.all_items.append({
            'name': base_name,
            'icon': icon,
            'info': info_dict,
            'count': count
        })

        self.addItem(item)
        self.item_info[base_name] = info_dict
        self.item_counts[base_name] = count

        # Sort items after adding
        self.sort_items()

    def clear_all_items(self):
        """Clear all items and reset data"""
        self.clear()
        self.item_info.clear()
        self.item_counts.clear()
        self.all_items.clear()

    def sort_items(self):
        """Sort items by category then by name"""
        # Implementation moved from custom_widgets.py
        pass

    def filter_items(self, category):
        """Filter items based on selected category"""
        # Implementation moved from custom_widgets.py
        pass

    def add_item_to_inventory(self, item: InventoryItem, count: int = 1):
        """Add an item back to the inventory list"""
        base_name = item.name
        
        # Make sure we're using the canonical icon path
        # The item.icon_path should already be canonical from InventoryItem.__init__
        icon_path = item.icon_path
        
        # Update all_items list
        found_in_all = False
        for item_data in self.all_items:
            if item_data['name'] == base_name:
                item_data['count'] += count
                # Update the icon to ensure it's correct
                item_data['icon'] = QIcon(QPixmap(icon_path).scaled(32, 32, Qt.KeepAspectRatio, Qt.FastTransformation))
                found_in_all = True
                break

        if not found_in_all:
            # Add to all_items with canonical path
            self.all_items.append({
                'name': base_name,
                'icon': QIcon(QPixmap(icon_path).scaled(32, 32, Qt.KeepAspectRatio, Qt.FastTransformation)),
                'info': item.properties,
                'count': count
            })

        # Check if item already exists in current filtered view
        if base_name in self.item_counts:
            # Update existing item count
            self.item_counts[base_name] += count
            self.update_item_display(base_name)
            
            # Also update its icon to ensure consistency
            for i in range(self.count()):
                list_item = self.item(i)
                if list_item and list_item.text().startswith(f"{base_name} "):
                    list_item.setIcon(QIcon(QPixmap(icon_path).scaled(32, 32, Qt.KeepAspectRatio, Qt.FastTransformation)))
        else:
            # Check if item should be visible with current filter
            should_show = False
            if self.current_filter == "All":
                should_show = True
            else:
                item_type = item.item_type.value
                if self.current_filter.lower() == item_type:
                    should_show = True

            if should_show:
                # Create new inventory entry
                self.item_counts[base_name] = count
                self.item_info[base_name] = item.properties

                # Create new list item with proper icon scaling using canonical path
                new_item = QListWidgetItem(
                    QIcon(QPixmap(icon_path).scaled(32, 32, Qt.KeepAspectRatio, Qt.FastTransformation)),
                    f"{base_name} ({count})"
                )
                self.addItem(new_item)

        # Sort items after adding
        self.sort_items()

    def update_item_display(self, base_name):
        """Update the display text for an item with its current count"""
        count = self.item_counts[base_name]
        for i in range(self.count()):
            item = self.item(i)
            if item.text().split(' (')[0] == base_name:
                item.setText(f"{base_name} ({count})")
                break

    def remove_item_from_inventory(self, base_name, count=1):
        """Remove count from inventory, remove item if count reaches 0"""
        # Update all_items list
        for item_data in self.all_items:
            if item_data['name'] == base_name:
                item_data['count'] -= count
                if item_data['count'] <= 0:
                    self.all_items.remove(item_data)
                break

        if base_name in self.item_counts:
            self.item_counts[base_name] -= count

            if self.item_counts[base_name] <= 0:
                # Remove item completely
                del self.item_counts[base_name]
                del self.item_info[base_name]

                # Remove from list widget
                for i in range(self.count()):
                    item = self.item(i)
                    if item.text().split(' (')[0] == base_name:
                        self.takeItem(i)
                        break
            else:
                # Update display
                self.update_item_display(base_name)

    def getItemData(self, item):
        """Get the complete data for an item as an InventoryItem object"""
        if not item:
            return None

        base_name = item.text().split(' (')[0]  # Remove count from name
        info = self.item_info.get(base_name, {})

        # Convert string values to enums
        item_type = ItemType.OTHER
        if 'item_type' in info:
            try:
                item_type = ItemType(info['item_type'])
            except ValueError:
                pass

        rarity = ItemRarity.COMMON
        if 'rarity' in info:
            try:
                rarity = ItemRarity(info['rarity'])
            except ValueError:
                pass

        # Don't need to provide icon_path as InventoryItem will use canonical path from name
        return InventoryItem(
            name=base_name,  # Use base name without count
            icon_path=None,  # Let InventoryItem use canonical path
            properties=info,
            item_type=item_type,
            rarity=rarity,
            stackable=info.get('stackable', False),
            max_stack=info.get('max_stack', 1),
            weight=info.get('weight', 1)
        )

    def auto_equip_item(self, item: InventoryItem):
        """Automatically equip item to appropriate slot (RMB functionality)"""
        print(f"🔧 AUTO_EQUIP: Starting auto-equip for '{item.name}' (type: {item.item_type.value})")
        
        # Import globals from main_interface module to ensure proper access
        import main_interface
        
        equipment_slots_global = main_interface.equipment_slots_global if hasattr(main_interface, 'equipment_slots_global') else globals().get('equipment_slots_global')
        current_unit = main_interface.current_unit_global if hasattr(main_interface, 'current_unit_global') else None

        if not equipment_slots_global:
            print("❌ AUTO_EQUIP: No equipment slots available")
            return False

        if not current_unit:
            print("❌ AUTO_EQUIP: No unit selected - cannot equip item")
            return False

        print(f"🔍 AUTO_EQUIP: Attempting to auto-equip {item.name} (type: {item.item_type.value}) for unit {current_unit}")
        
        # Find appropriate slot
        target_slot = None

        if item.item_type == ItemType.ARMOUR:
            print(f"🔍 AUTO_EQUIP: Looking for armor slot...")
            # Find armour slot
            for slot in equipment_slots_global:
                if slot.slot_type == ItemType.ARMOUR:
                    print(f"🔍 AUTO_EQUIP: Found armour slot: {slot.slot_name}, has item: {slot.item is not None}, enabled: {slot.enabled}")
                    if slot.item is None and slot.enabled:
                        target_slot = slot
                        print(f"✅ AUTO_EQUIP: Empty armor slot found: {slot.slot_name}")
                        break
                    elif slot.item is not None and slot.enabled:
                        # Replace existing armor
                        print(f"🔧 AUTO_EQUIP: Replacing existing armor '{slot.item.name}' with '{item.name}'")
                        old_item = slot.remove_item()
                        if old_item:
                            item_list_widget_global = main_interface.item_list_widget_global if hasattr(main_interface, 'item_list_widget_global') else None
                            if item_list_widget_global:
                                item_list_widget_global.add_item_to_inventory(old_item, 1)
                                print(f"✅ AUTO_EQUIP: Returned old armor '{old_item.name}' to inventory")
                        target_slot = slot
                        print(f"✅ AUTO_EQUIP: Will replace armor in slot: {slot.slot_name}")
                        break
                        
        elif item.item_type == ItemType.WEAPON:
            print(f"🔍 AUTO_EQUIP: Looking for weapon slot...")
            # Find weapon slot
            for slot in equipment_slots_global:
                if slot.slot_type == ItemType.WEAPON:
                    print(f"🔍 AUTO_EQUIP: Found weapon slot: {slot.slot_name}, has item: {slot.item is not None}, enabled: {slot.enabled}")
                    if slot.item is None and slot.enabled:
                        target_slot = slot
                        break
                    elif slot.item is not None and slot.enabled:
                        # Replace existing weapon
                        old_item = slot.remove_item()
                        if old_item:
                            item_list_widget_global = main_interface.item_list_widget_global if hasattr(main_interface, 'item_list_widget_global') else None
                            if item_list_widget_global:
                                item_list_widget_global.add_item_to_inventory(old_item, 1)
                        target_slot = slot
                        break
                        
        elif item.item_type == ItemType.EQUIPMENT:
            print(f"🔍 AUTO_EQUIP: Looking for equipment slot...")
            # Find first available equipment slot
            for slot in equipment_slots_global:
                if slot.slot_type == ItemType.EQUIPMENT:
                    print(f"🔍 AUTO_EQUIP: Found equipment slot: {slot.slot_name}, has item: {slot.item is not None}, enabled: {slot.enabled}")
                    if slot.item is None and slot.enabled:
                        target_slot = slot
                        print(f"✅ AUTO_EQUIP: Empty equipment slot found: {slot.slot_name}")
                        break

        if target_slot:
            print(f"🔧 AUTO_EQUIP: Equipping {item.name} to slot {target_slot.slot_name}")
            success = target_slot.add_item(item)
            
            if success:
                print(f"✅ AUTO_EQUIP: Successfully equipped {item.name}")
                # Update weight display
                update_weight_display()
                return True
            else:
                print(f"❌ AUTO_EQUIP: Failed to equip {item.name}")
                return False
        else:
            print(f"❌ AUTO_EQUIP: No suitable slot found for {item.name}")
            return False

    def dragEnterEvent(self, event: QDragEnterEvent):
        """Accept drops from equipment slots"""
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        """Handle items dropped back to inventory"""
        try:
            data = json.loads(event.mimeData().text())
            item = InventoryItem.from_dict(data['item'])

            self.add_item_to_inventory(item, 1)
            event.acceptProposedAction()
        except Exception as e:
            print(f"Drop to inventory error: {e}")
            event.ignore()

    def startDrag(self, supportedActions):
        """Override to implement custom drag behavior"""
        current_item = self.currentItem()
        if not current_item:
            return

        item_data = self.getItemData(current_item)
        if not item_data:
            return

        base_name = item_data.name

        # Check if we have items in stock
        if self.item_counts.get(base_name, 0) <= 0:
            return

        # Create drag object
        drag = QDrag(self)
        mime_data = QMimeData()

        # Store item data as JSON
        drag_data = {
            'item': item_data.to_dict(),
            'stack_size': 1,  # Default stack size from list
            'source_slot': id(self)
        }
        mime_data.setText(json.dumps(drag_data))
        drag.setMimeData(mime_data)

        # Set drag pixmap without system cursor using the same icon as the list
        if current_item.icon() and not current_item.icon().isNull():
            pixmap = current_item.icon().pixmap(64, 64)
            drag.setPixmap(pixmap)

        # Hide system cursor during drag
        QApplication.setOverrideCursor(Qt.BlankCursor)

        # Execute drag (using Copy action since we're not removing from list)
        result = drag.exec(Qt.CopyAction)

        # Restore cursor
        QApplication.restoreOverrideCursor()

        if result == Qt.CopyAction:
            # Item was successfully dropped, reduce count
            self.remove_item_from_inventory(base_name, 1)

    def mousePressEvent(self, event):
        """Handle left mouse press for dragging"""
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.position().toPoint()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """Handle right mouse release for auto-equip functionality"""
        if event.button() == Qt.RightButton:
            # Get the item that was right-clicked on
            clicked_item = self.itemAt(event.position().toPoint())
            if clicked_item:
                # Select the item that was right-clicked
                self.setCurrentItem(clicked_item)
                
                item_data = self.getItemData(clicked_item)
                if item_data and self.item_counts.get(item_data.name, 0) > 0:
                    print(f"Right-click detected on item {item_data.name}")
                    
                    # Check if there's a current unit selected
                    import main_interface
                    current_unit = main_interface.current_unit_global
                    if not current_unit:
                        print("No unit selected - cannot equip item")
                        super().mouseReleaseEvent(event)
                        return
                    
                    if self.auto_equip_item(item_data):
                        # Successfully equipped, remove from inventory
                        self.remove_item_from_inventory(item_data.name, 1)
                        
                        # Save the current unit's inventory after equipping
                        unit_inventory_manager = main_interface.unit_inventory_manager
                        equipment_slots = main_interface.equipment_slots_global
                        if unit_inventory_manager and equipment_slots:
                            unit_inventory_manager.save_unit_inventory(current_unit, equipment_slots)
                            print(f"Saved inventory for unit {current_unit} after equipping {item_data.name}")
                        
                        print(f"Auto-equipped {item_data.name} via right-click")
                    else:
                        print(f"Could not auto-equip {item_data.name} - no available slot")
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):  # Only LMB for drag
            return

        if not hasattr(self, 'drag_start_position'):
            return

        if ((event.position().toPoint() - self.drag_start_position).manhattanLength() <
                QApplication.startDragDistance()):
            return

        self.startDrag(Qt.CopyAction)

class UnitListWidget(QListWidget):
    """
    Unit selection list widget with filtering and category support.
    
    Features:
    - Category-based filtering (All categories plus specific unit types)
    - Unit information storage and display
    - Unit selection handling with inventory switching
    - Automatic sorting by category then name
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.unit_info = {}
        self.all_units = []  # Store all units for filtering
        self.current_filter = "All"
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        
        # Disable scrollbars
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def addUnitWithInfo(self, item, info_dict):
        """Add a unit with associated information to the list"""
        unit_name = item.text()
        
        # Store in all_units for filtering
        self.all_units.append({
            'name': unit_name,
            'icon': item.icon(),
            'info': info_dict
        })

        self.addItem(item)
        self.unit_info[unit_name] = info_dict

        # Sort units after adding
        self.sort_units()

    def clear_all_units(self):
        """Clear all units and reset data"""
        self.clear()
        self.unit_info.clear()
        self.all_units.clear()

    def sort_units(self):
        """Sort units by category then by name"""
        # Get all items with their info
        items_with_info = []
        for i in range(self.count()):
            item = self.item(i)
            unit_name = item.text()
            info = self.unit_info.get(unit_name, {})
            items_with_info.append((item, info))

        # Clear the list
        self.clear()

        # Sort by category first, then by name
        def sort_key(item_info_pair):
            item, info = item_info_pair
            category = info.get('category', 'unknown')
            name = item.text()
            return (category, name)

        items_with_info.sort(key=sort_key)

        # Re-add sorted items
        for item, info in items_with_info:
            self.addItem(item)

    def filter_units(self, category):
        """Filter units based on selected category"""
        self.current_filter = category
        self.clear()

        for unit_data in self.all_units:
            unit_info = unit_data['info']
            unit_category = unit_info.get('category', 'unknown').lower()

            # Show unit if it matches filter or filter is "All"
            if category == "All" or category.lower() == unit_category:
                item = QListWidgetItem(unit_data['icon'], unit_data['name'])
                self.addItem(item)

        # Sort filtered results
        self.sort_units()

    def mousePressEvent(self, event):
        """Handle mouse press for unit selection"""
        if event.button() == Qt.LeftButton:
            item = self.itemAt(event.position().toPoint())
            if item:
                self.setCurrentItem(item)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """Handle mouse release for unit selection"""
        if event.button() == Qt.LeftButton:
            item = self.itemAt(event.position().toPoint())
            if item:
                unit_name = item.text()
                self.unit_selected(unit_name)
        super().mouseReleaseEvent(event)

    def unit_selected(self, unit_name):
        """Handle unit selection with proper global variable access"""
        # Import globals from main_interface module to ensure proper access
        import main_interface
        
        # Access the global variables through the module
        unit_inventory_manager_global = main_interface.unit_inventory_manager
        equipment_slots_global = main_interface.equipment_slots_global if hasattr(main_interface, 'equipment_slots_global') else globals().get('equipment_slots_global')
        item_list_widget_global = main_interface.item_list_widget_global if hasattr(main_interface, 'item_list_widget_global') else globals().get('item_list_widget_global')
        unit_info_label_global = main_interface.unit_info_label_global if hasattr(main_interface, 'unit_info_label_global') else globals().get('unit_info_label_global')
        
        print(f"Processing unit selection: {unit_name}")
        print(f"Global references - manager: {unit_inventory_manager_global is not None}, slots: {equipment_slots_global is not None}, item_list: {item_list_widget_global is not None}")

        if not unit_inventory_manager_global:
            print("Missing unit inventory manager")
            return
            
        if not equipment_slots_global:
            print("Missing equipment slots")
            return

        # Save current unit's inventory if there was a previous unit
        if hasattr(main_interface, 'current_unit_global') and main_interface.current_unit_global:
            print(f"Saving inventory for previous unit: {main_interface.current_unit_global}")
            unit_inventory_manager_global.save_unit_inventory(main_interface.current_unit_global, equipment_slots_global)

        # Set new current unit
        main_interface.current_unit_global = unit_name
        print(f"Set current unit to: {unit_name}")

        # Load new unit's inventory
        unit_inventory_manager_global.load_unit_inventory(unit_name, equipment_slots_global, item_list_widget_global)

        # Update unit info display
        if unit_info_label_global and unit_name in self.unit_info:
            unit_info = self.unit_info[unit_name]
            category = unit_info.get('category', 'unknown').capitalize()
            unit_info_label_global.setText(f"Selected: {unit_name}\nCategory: {category}")

        self.update_basic_info_display(unit_name)

    def update_basic_info_display(self, unit_name):
        """Update the basic info group box with unit information"""
        import main_interface
        
        basic_info_label_global = main_interface.basic_info_label_global if hasattr(main_interface, 'basic_info_label_global') else None
        
        if basic_info_label_global and unit_name in self.unit_info:
            unit_info = self.unit_info[unit_name]
            category = unit_info.get('category', 'Unknown')
            
            # Create info text
            info_text = f"Unit: {unit_name}\nType: {category.capitalize()}"
            basic_info_label_global.setText(info_text)
