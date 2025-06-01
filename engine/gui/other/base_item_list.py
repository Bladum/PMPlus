"""
A generic widget that displays an inventory with filtering capabilities.

This class provides a reusable inventory widget with category filtering and
drag-and-drop support. It serves as the base component for various inventory
displays throughout the game (base storage, unit equipment, craft loadouts).

Interactions:
- Used by specialized inventory classes (TUnitInventoryWidget, TCraftInventoryWidget)
- Interfaces with TItemTransferManager for drag and drop operations
- Displays items from game's inventory systems
- Communicates with equipment slots for item transfers
- Responds to inventory changes from game systems

Key Features:
- Category filtering via dropdown
- Sorted item display with quantities
- Item icon rendering with counts
- Drag and drop support for moving items
- Consistent styling across the application
"""

import json
from typing import Dict, Any, List, Optional, Callable
from PySide6.QtCore import Qt, QPoint, QMimeData
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QDrag
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QComboBox, QListWidget, QListWidgetItem,
    QAbstractItemView, QApplication
)

from gui.other.theme_manager import px, XcomStyle
from item.item import TItem, TItemRarity  # Import TItem and TItemRarity
from item.item_type import TItemType
from syf.item_path_lookup import get_canonical_path  # Still need this function


class TInventoryWidget(QWidget):

    def __init__(self, parent=None, categories=None):
        """Initialize the inventory widget with combo box and list."""
        super().__init__(parent)

        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(px(0.5), px(0.5), px(0.5), px(0.5))
        self.layout.setSpacing(px(0.5))

        # Initialize the filter combo box
        self.filter_combo = QComboBox()
        self.setup_filter_combo(categories)
        self.layout.addWidget(self.filter_combo)

        # Initialize the item list
        self.item_list = ItemList()
        self.layout.addWidget(self.item_list)

        # Connect signals
        self.filter_combo.currentTextChanged.connect(self.filter_items)

    def setup_filter_combo(self, categories=None):
        """Setup the category filter combo box with icons."""
        self.filter_combo.clear()

        # Use default categories if none provided
        if categories is None:
            categories = [
                {"name": "All", "icon": "other/item2.png"},
                {"name": "Craft Item", "icon": "other/item2.png"},
                {"name": "Armour", "icon": "other/item2.png"},
                {"name": "Weapon", "icon": "other/item2.png"},
                {"name": "Equipment", "icon": "other/item.png"},
                {"name": "Other", "icon": "other/item.png"},
            ]

        # Add items to combo box
        for category in categories:
            icon = QIcon(QPixmap(category["icon"]).scaled(32, 32, Qt.KeepAspectRatio, Qt.FastTransformation))
            self.filter_combo.addItem(icon, category["name"])

        # Apply styling
        self.filter_combo.setStyleSheet(XcomStyle.combobox())

    def filter_items(self, category: str):
        """Filter items based on selected category."""
        self.item_list.filter_items(category)

    def add_item(self, name: str, icon_path: Optional[str], info_dict: Dict[str, Any], count: int = 1) -> bool:
        """
        Add an item to the inventory.

        Args:
            name: Display name of the item
            icon_path: Path to item icon (optional, canonical path will be used if available)
            info_dict: Dictionary with item metadata (must contain 'item_type')
            count: Number of items to add

        Returns:
            True if item was added successfully, False otherwise
        """
        # Ensure item_type is provided
        if 'item_type' not in info_dict:
            print(f"Error: Cannot add item {name}, missing item_type in info_dict")
            return False

        return self.item_list.add_item(name, icon_path, info_dict, count)

    def remove_item(self, name: str, count: int = 1) -> bool:
        """
        Remove an item from the inventory.

        Args:
            name: Name of the item to remove
            count: Number of items to remove

        Returns:
            True if item was removed successfully, False otherwise
        """
        return self.item_list.remove_item(name, count)

    def clear_inventory(self):
        """Clear all items from the inventory."""
        self.item_list.clear_all_items()

    def get_item_count(self, name: str) -> int:
        """Get the count of a specific item in inventory."""
        return self.item_list.get_item_count(name)

    def get_all_items(self) -> Dict[str, Dict[str, Any]]:
        """Get dictionary of all items and their information."""
        return self.item_list.get_all_items_info()

    def set_drag_callback(self, callback: Callable[[TItem], None]):
        """Set a callback function called when an item is dragged out."""
        self.item_list.set_drag_callback(callback)

    def set_drop_callback(self, callback: Callable[[TItem], None]):
        """Set a callback function called when an item is dropped to the list."""
        self.item_list.set_drop_callback(callback)


# Legacy class name for backward compatibility
class BaseInventoryListWidget(TInventoryWidget):
    """Legacy class name, use InventoryWidget instead."""
    pass


class ItemList(QListWidget):
    """
    List widget that displays inventory items with counts.

    Handles all the sorting, filtering, and drag-and-drop functionality.
    Items are stored with complete metadata to ensure proper filtering and display.
    """

    def __init__(self, *args, **kwargs):
        """Initialize inventory list widget."""
        super().__init__(*args, **kwargs)

        # Data storage
        self.item_info: Dict[str, Dict[str, Any]] = {}  # Store item properties
        self.item_counts: Dict[str, int] = {}  # Track item quantities
        self.all_items: List[Dict[str, Any]] = []  # Store all items for filtering
        self.current_filter = "All"

        # Callbacks
        self.drag_callback = None
        self.drop_callback = None

        # Configure list behavior
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setMouseTracking(True)
        self.setDragDropMode(QAbstractItemView.DragDrop)  # Allow both drag and drop

        # Apply styling
        self.setStyleSheet(XcomStyle.listwidget())

        # Disable scrollbars - uncomment if needed
        # self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def add_item(self, name: str, icon_path: Optional[str], info_dict: Dict[str, Any], count: int = 1) -> bool:
        """
        Add an item to the inventory or increase its count if already exists.

        Args:
            name: Display name of the item
            icon_path: Path to item icon (optional)
            info_dict: Dictionary containing item properties
            count: Quantity to add

        Returns:
            True if successful, False otherwise
        """
        if count <= 0:
            return False

        # Get canonical path for item icon
        canonical_path = get_canonical_path(name) if icon_path is None else icon_path

        # Set icon path in info_dict
        info_dict['icon_path'] = canonical_path

        # Create icon
        icon = QIcon(QPixmap(canonical_path).scaled(32, 32, Qt.KeepAspectRatio, Qt.FastTransformation))

        # Check if item already exists
        if name in self.item_counts:
            # Update count
            self.item_counts[name] += count
            # Update display
            self._update_item_display(name)
        else:
            # Create new item entry
            self.item_counts[name] = count
            self.item_info[name] = info_dict

            # Add to all_items list for filtering
            self.all_items.append({
                'name': name,
                'icon': icon,
                'info': info_dict,
                'count': count
            })

            # Create new QListWidgetItem if it should be visible with current filter
            if self._should_show_item(name, self.current_filter):
                list_item = QListWidgetItem(icon, f"{name} ({count})")
                self.addItem(list_item)

        # Sort items after adding
        self.sort_items()
        return True

    def remove_item(self, name: str, count: int = 1) -> bool:
        """
        Remove an item from inventory or decrease its count.

        Args:
            name: Name of the item to remove
            count: Quantity to remove

        Returns:
            True if successful, False otherwise
        """
        if name not in self.item_counts or count <= 0:
            return False

        # Update count
        self.item_counts[name] -= count

        # Remove from inventory if count reached zero
        if self.item_counts[name] <= 0:
            # Remove from data structures
            del self.item_counts[name]
            del self.item_info[name]

            # Remove from all_items
            for i, item_data in enumerate(self.all_items):
                if item_data['name'] == name:
                    self.all_items.pop(i)
                    break

            # Remove from list widget if visible
            for i in range(self.count()):
                item = self.item(i)
                if item.text().split(' (')[0] == name:
                    self.takeItem(i)
                    break
        else:
            # Just update display text
            self._update_item_display(name)

        return True

    def filter_items(self, category: str):
        """Filter items based on selected category."""
        self.current_filter = category
        self.clear()  # Clear visible items only

        # Re-add items that match the filter
        for item_data in self.all_items:
            name = item_data['name']
            count = item_data['count']
            info = item_data['info']
            icon = item_data['icon']

            if self._should_show_item(name, category):
                list_item = QListWidgetItem(icon, f"{name} ({count})")
                self.addItem(list_item)

        # Sort the filtered list
        self.sort_items()

    def sort_items(self):
        """Sort items by category then alphabetically by name."""
        # Define category sort order for consistent display
        category_order = {
            "craft item": 0,
            "armour": 1,
            "weapon": 2,
            "equipment": 3,
            "other": 4
        }

        # Get all visible items with their info
        items_with_info = []
        for i in range(self.count()):
            item = self.item(i)
            name = item.text().split(' (')[0]
            info = self.item_info.get(name, {})
            items_with_info.append((item, info))

        # Clear the visible list
        self.clear()

        # Define sort key function
        def sort_key(item_info):
            item, info = item_info
            name = item.text().split(' (')[0]
            item_type = info.get('item_type', 'other').lower()
            category_index = category_order.get(item_type, 999)
            return (category_index, name)

        # Sort items using our key function
        items_with_info.sort(key=sort_key)

        # Re-add the sorted items
        for item, _ in items_with_info:
            self.addItem(item.clone())

    def clear_all_items(self):
        """Clear all items from inventory."""
        self.clear()
        self.item_info = {}
        self.item_counts = {}
        self.all_items = []

    def get_item_count(self, name: str) -> int:
        """Get the count of a specific item in inventory."""
        return self.item_counts.get(name, 0)

    def get_all_items_info(self) -> Dict[str, Dict[str, Any]]:
        """Get dictionary of all items and their information."""
        result = {}
        for name, info in self.item_info.items():
            result[name] = {
                **info,
                'count': self.item_counts.get(name, 0)
            }
        return result

    def set_drag_callback(self, callback: Callable[[TItem], None]):
        """Set a callback function called when an item is dragged out."""
        self.drag_callback = callback

    def set_drop_callback(self, callback: Callable[[TItem], None]):
        """Set a callback function called when an item is dropped to the list."""
        self.drop_callback = callback

    def _update_item_display(self, name: str):
        """Update the display text for an item with its current count."""
        count = self.item_counts.get(name, 0)
        for i in range(self.count()):
            item = self.item(i)
            item_name = item.text().split(' (')[0]
            if item_name == name:
                item.setText(f"{name} ({count})")
                break

    def _should_show_item(self, name: str, filter_category: str) -> bool:
        """Check if item should be visible with the current filter."""
        if filter_category == "All":
            return True

        info = self.item_info.get(name, {})
        item_type = info.get('item_type', 'other').lower()

        # Handle "Craft Item" category specifically
        if filter_category.lower() == "craft item":
            return item_type == "craft item"

        return item_type == filter_category.lower()

    def _create_inventory_item(self, list_item: QListWidgetItem) -> Optional[TItem]:
        """Create a TItem object from a QListWidgetItem."""
        if not list_item:
            return None

        name = list_item.text().split(' (')[0]
        info = self.item_info.get(name, {})

        # Extract item properties from info dictionary
        item_type_str = info.get('item_type', 'other')

        # Convert string to TItemType enum
        try:
            item_type = TItemType(item_type_str)
        except ValueError:
            item_type = TItemType.ITEM_GENERAL

        # Convert string to TItemRarity enum if present
        rarity_str = info.get('rarity', 'common')
        try:
            rarity = TItemRarity(rarity_str)
        except ValueError:
            rarity = TItemRarity.COMMON

        # Create TItem instance
        return TItem(
            name=name,
            icon_path=info.get('icon_path'),
            item_type=item_type,
            properties=info,
            rarity=rarity,
            weight=info.get('weight', 1)
        )

    def mousePressEvent(self, event):
        """Handle mouse press for initiating drag operations."""
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.position().toPoint()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Handle mouse movement to start drag if threshold is exceeded."""
        if not (event.buttons() & Qt.LeftButton):
            return

        if not hasattr(self, 'drag_start_position'):
            return

        # Check if minimum drag distance is reached
        if ((event.position().toPoint() - self.drag_start_position).manhattanLength() <
                QApplication.startDragDistance()):
            return

        # Get the current item
        current_item = self.currentItem()
        if not current_item:
            return

        # Create drag object
        drag = QDrag(self)
        mime_data = QMimeData()

        # Create a TItem from the QListWidgetItem
        item = self._create_inventory_item(current_item)
        if not item:
            return

        # Serialize item data for drag and drop
        item_data = {
            'name': item.name,
            'type': item.item_type.name,
            'rarity': item.rarity.name,
            'properties': item.properties
        }
        mime_data.setText(json.dumps(item_data))
        drag.setMimeData(mime_data)

        # Create a pixmap for the drag icon
        icon_size = 32
        pixmap = QPixmap(icon_size, icon_size)
        pixmap.fill(Qt.transparent)

        # Draw item icon and count badge
        painter = QPainter(pixmap)
        name = current_item.text().split(' (')[0]
        count = self.item_counts.get(name, 1)

        # Draw the icon
        icon = current_item.icon()
        icon.paint(painter, 0, 0, icon_size, icon_size)

        # Draw count badge if more than 1
        if count > 1:
            badge_size = 16
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(0, 120, 215))
            painter.drawEllipse(icon_size - badge_size, icon_size - badge_size, badge_size, badge_size)
            painter.setPen(Qt.white)
            painter.drawText(icon_size - badge_size, icon_size - badge_size,
                            badge_size, badge_size, Qt.AlignCenter, str(count))
        painter.end()

        # Set the pixmap and hotspot
        drag.setPixmap(pixmap)
        drag.setHotSpot(QPoint(pixmap.width() // 2, pixmap.height() // 2))

        # Execute the drag operation
        if drag.exec(Qt.CopyAction) == Qt.CopyAction:
            # Call drag callback if set
            if self.drag_callback and item:
                self.drag_callback(item)

    def dragEnterEvent(self, event):
        """Handle when a drag enters the widget area."""
        if event.mimeData().hasText():
            try:
                item_data = json.loads(event.mimeData().text())
                if isinstance(item_data, dict) and 'name' in item_data:
                    event.accept()
                    return
            except json.JSONDecodeError:
                pass
        event.ignore()

    def dragMoveEvent(self, event):
        """Handle when a drag moves over the widget area."""
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """Handle when an item is dropped on the widget."""
        if event.mimeData().hasText():
            try:
                # Parse the dropped item data
                item_data = json.loads(event.mimeData().text())

                if isinstance(item_data, dict) and 'name' in item_data:
                    name = item_data['name']
                    item_type_str = item_data.get('type', 'ITEM_GENERAL')

                    # Convert string to TItemType enum
                    try:
                        item_type = TItemType(item_type_str)
                    except ValueError:
                        item_type = TItemType.ITEM_GENERAL

                    # Convert string to TItemRarity enum if present
                    rarity_str = item_data.get('rarity', 'COMMON')
                    try:
                        rarity = TItemRarity(rarity_str)
                    except ValueError:
                        rarity = TItemRarity.COMMON

                    # Create a TItem instance
                    item = TItem(
                        name=name,
                        icon_path=item_data.get('properties', {}).get('icon_path'),
                        item_type=item_type,
                        properties=item_data.get('properties', {}),
                        rarity=rarity,
                        weight=item_data.get('properties', {}).get('weight', 1)
                    )

                    # Call drop callback if set
                    if self.drop_callback and item:
                        self.drop_callback(item)

                    event.accept()
                    return
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Error processing dropped item: {e}")

        event.ignore()
