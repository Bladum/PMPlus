"""
engine/gui/other/widget/base_inventory_widget.py

Comprehensive widget for managing base storage inventory in the XCOM GUI.
Standardized: All docstrings and comments follow the unified documentation style (2025-06-14).
"""

from typing import Dict, List, Any, Optional, Callable, Union, Tuple
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QIcon, QPixmap, QFont, QDragEnterEvent, QDropEvent, QMouseEvent
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QListWidget, QListWidgetItem,
    QLabel, QPushButton, QLineEdit, QAbstractItemView, QGroupBox, QScrollArea,
    QCheckBox, QSpinBox
)
from gui.theme_manager import XcomStyle, px
from item.item import TItem
from item.item_type import TItemType


class TBaseInventoryWidget(QWidget):
    """
    Widget for displaying and managing a base's complete inventory.
    Advanced version of TInventoryWidget with specialized filtering for both unit equipment and craft components.
    Inherits from QWidget.
    """

    # Signal emitted when an item is dragged out
    itemDragged = Signal(TItem, int)  # (item, quantity)

    # Signal emitted when an item is dropped in
    itemDropped = Signal(TItem, int)  # (item, quantity)

    # Signal emitted when item count changes
    inventoryChanged = Signal()

    def __init__(self, parent=None, title="Base Storage"):
        """
        Initialize the base inventory widget with advanced filtering capabilities.

        Args:
            parent: Parent widget.
            title: Title for the group box.
        """
        super().__init__(parent)

        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(px(0.5), px(0.5), px(0.5), px(0.5))
        self.layout.setSpacing(px(0.5))

        # Create group box for styling
        self.group_box = QGroupBox(title)
        self.group_box.setStyleSheet(XcomStyle.groupbox())

        # Group box layout
        self.box_layout = QVBoxLayout(self.group_box)
        self.box_layout.setContentsMargins(px(0.5), px(0.5), px(0.5), px(0.5))
        self.box_layout.setSpacing(px(0.5))

        # Search box for filtering by name
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search items...")
        self.search_box.setStyleSheet(XcomStyle.lineedit())
        self.search_box.textChanged.connect(self._filter_items)
        self.box_layout.addWidget(self.search_box)

        # Create horizontal layout for filter controls
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(px(0.5))

        # Main category filter (Unit Items, Craft Components, Resources)
        self.main_category_combo = QComboBox()
        self.main_category_combo.setStyleSheet(XcomStyle.combobox())
        self.main_category_combo.currentTextChanged.connect(self._on_main_category_changed)
        filter_layout.addWidget(self.main_category_combo)

        # Subcategory filter (depends on main category)
        self.sub_category_combo = QComboBox()
        self.sub_category_combo.setStyleSheet(XcomStyle.combobox())
        self.sub_category_combo.currentTextChanged.connect(self._filter_items)
        filter_layout.addWidget(self.sub_category_combo)

        self.box_layout.addLayout(filter_layout)

        # Add advanced filter toggle
        self.advanced_filter_checkbox = QCheckBox("Advanced Filters")
        self.advanced_filter_checkbox.setStyleSheet(XcomStyle.checkbox())
        self.advanced_filter_checkbox.toggled.connect(self._toggle_advanced_filters)
        self.box_layout.addWidget(self.advanced_filter_checkbox)

        # Advanced filter options (hidden by default)
        self.advanced_filter_widget = QWidget()
        self.advanced_filter_layout = QVBoxLayout(self.advanced_filter_widget)
        self.advanced_filter_layout.setContentsMargins(0, 0, 0, 0)
        self.advanced_filter_layout.setSpacing(px(0.5))

        # Add weight filter
        weight_filter_layout = QHBoxLayout()
        weight_filter_layout.addWidget(QLabel("Max Weight:"))
        self.weight_filter = QSpinBox()
        self.weight_filter.setRange(0, 100)
        self.weight_filter.setValue(100)
        self.weight_filter.setStyleSheet(XcomStyle.spinbox())
        self.weight_filter.valueChanged.connect(self._filter_items)
        weight_filter_layout.addWidget(self.weight_filter)
        self.advanced_filter_layout.addLayout(weight_filter_layout)

        # Add "show empty" checkbox
        self.show_empty_checkbox = QCheckBox("Show Empty Categories")
        self.show_empty_checkbox.setStyleSheet(XcomStyle.checkbox())
        self.show_empty_checkbox.toggled.connect(self._filter_items)
        self.advanced_filter_layout.addWidget(self.show_empty_checkbox)

        # Add advanced filter widget (hidden initially)
        self.box_layout.addWidget(self.advanced_filter_widget)
        self.advanced_filter_widget.hide()

        # Item list
        self.item_list = QListWidget()
        self.item_list.setStyleSheet(XcomStyle.listwidget())
        self.item_list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.item_list.setDragEnabled(True)
        self.item_list.setAcceptDrops(True)
        self.item_list.setIconSize(QSize(32, 32))

        # Connect drag-drop signals
        self.item_list.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)
        self.item_list.itemDoubleClicked.connect(self._on_item_double_clicked)
        self.box_layout.addWidget(self.item_list)

        # Total weight display
        self.weight_label = QLabel("Total Weight: 0")
        self.weight_label.setStyleSheet(f"color: {XcomStyle.text_color}; background: transparent;")
        self.weight_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.box_layout.addWidget(self.weight_label)

        # Data storage
        self.items: Dict[str, Dict[str, Any]] = {}  # Store items by name
        self.item_counts: Dict[str, int] = {}  # Track quantities
        self.all_items: List[Dict[str, Any]] = []  # Store all items for filtering
        self.current_main_category = "All"
        self.current_sub_category = "All"
        self.current_search = ""

        # Add group box to main layout
        self.layout.addWidget(self.group_box)

        # Initialize filters
        self._setup_default_filters()
        self._update_weight_display()

    def _setup_default_filters(self):
        """Setup default category filters."""
        # Main categories
        self.main_category_combo.clear()
        self.main_category_combo.addItem("All")
        self.main_category_combo.addItem("Unit Equipment")
        self.main_category_combo.addItem("Craft Components")
        self.main_category_combo.addItem("Resources")

        # Default subcategories for "All"
        self._update_subcategories("All")

    def _update_subcategories(self, main_category: str):
        """
        Update subcategory combo box based on main category selection.

        Args:
            main_category: The main category selected
        """
        self.sub_category_combo.clear()
        self.sub_category_combo.addItem("All")

        if main_category == "All" or main_category == "Unit Equipment":
            self.sub_category_combo.addItem("Weapons")
            self.sub_category_combo.addItem("Armor")
            self.sub_category_combo.addItem("Equipment")

        if main_category == "All" or main_category == "Craft Components":
            self.sub_category_combo.addItem("Weapons")
            self.sub_category_combo.addItem("Engines")
            self.sub_category_combo.addItem("Defense")
            self.sub_category_combo.addItem("Systems")

        if main_category == "All" or main_category == "Resources":
            self.sub_category_combo.addItem("Materials")
            self.sub_category_combo.addItem("Alien Artifacts")
            self.sub_category_combo.addItem("Supplies")

    def _on_main_category_changed(self, category: str):
        """Handle main category selection change."""
        self.current_main_category = category
        self._update_subcategories(category)
        self._filter_items()

    def _toggle_advanced_filters(self, checked: bool):
        """Toggle visibility of advanced filter options."""
        self.advanced_filter_widget.setVisible(checked)
        self._filter_items()  # Refilter with new options

    def add_item(self, item: TItem, quantity: int = 1, icon_path: Optional[str] = None) -> bool:
        """
        Add an item to the inventory.

        Args:
            item: Item to add
            quantity: Quantity to add
            icon_path: Path to item icon (uses item.icon_path if None)

        Returns:
            True if item was added successfully
        """
        if not item:
            return False

        item_name = item.name if hasattr(item, 'name') else "Unnamed Item"

        # Create icon
        icon_path = icon_path if icon_path else getattr(item, 'icon_path', None)
        icon = None
        if icon_path:
            try:
                icon = QIcon(QPixmap(icon_path).scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            except Exception:
                # Fallback if icon can't be loaded
                pass

        # Get item type information
        item_type = getattr(item, 'item_type', TItemType.ITEM_GENERAL)
        item_weight = getattr(item, 'weight', 1)

        # Determine main category and subcategory
        main_category, sub_category = self._categorize_item(item)

        # Check if item already exists
        if item_name in self.items:
            # Update quantity
            self.item_counts[item_name] += quantity

            # Update item in the list widget if visible
            self._update_item_display(item_name)
        else:
            # Add new item
            self.items[item_name] = {
                'item': item,
                'icon': icon,
                'type': item_type,
                'weight': item_weight,
                'main_category': main_category,
                'sub_category': sub_category
            }

            self.item_counts[item_name] = quantity

            # Add to all_items for filtering
            list_item = QListWidgetItem()
            if icon:
                list_item.setIcon(icon)
            list_item.setText(f"{item_name} ({quantity})")
            list_item.setData(Qt.UserRole, item)

            self.all_items.append({
                'name': item_name,
                'item': item,
                'list_item': list_item,
                'main_category': main_category,
                'sub_category': sub_category,
                'weight': item_weight
            })

            # Add to visible list if passes current filter
            if self._passes_filter(main_category, sub_category, item_name, item_weight):
                self.item_list.addItem(list_item)

        # Update total weight
        self._update_weight_display()

        # Emit signal that inventory changed
        self.inventoryChanged.emit()

        return True

    def _categorize_item(self, item: TItem) -> Tuple[str, str]:
        """
        Determine the main category and subcategory for an item.

        Args:
            item: Item to categorize

        Returns:
            Tuple of (main_category, sub_category)
        """
        item_type = getattr(item, 'item_type', TItemType.ITEM_GENERAL)
        item_type_str = str(item_type).lower() if hasattr(item_type, '__str__') else "unknown"

        # Determine main category
        if item_type_str in ["weapon", "armor", "equipment", "item_weapon", "item_armor", "item_unit_equipment"]:
            main_category = "Unit Equipment"
            if "weapon" in item_type_str:
                sub_category = "Weapons"
            elif "armor" in item_type_str or "armour" in item_type_str:
                sub_category = "Armor"
            else:
                sub_category = "Equipment"

        elif item_type_str in ["craft_weapon", "engine", "defense", "craft_engine", "craft_defense", "craft_item"]:
            main_category = "Craft Components"
            if "weapon" in item_type_str:
                sub_category = "Weapons"
            elif "engine" in item_type_str:
                sub_category = "Engines"
            elif "defense" in item_type_str:
                sub_category = "Defense"
            else:
                sub_category = "Systems"

        elif item_type_str in ["resource", "material", "alien", "supply"]:
            main_category = "Resources"
            if "alien" in item_type_str:
                sub_category = "Alien Artifacts"
            elif "material" in item_type_str:
                sub_category = "Materials"
            else:
                sub_category = "Supplies"

        else:
            main_category = "Resources"
            sub_category = "Supplies"

        return main_category, sub_category

    def remove_item(self, item_name: str, quantity: int = 1) -> Optional[TItem]:
        """
        Remove an item from the inventory.

        Args:
            item_name: Name of the item to remove
            quantity: Quantity to remove (default 1)

        Returns:
            The removed item or None if not found
        """
        if item_name not in self.items or quantity <= 0:
            return None

        # Get item
        item = self.items[item_name]['item']

        # Update count
        current_count = self.item_counts[item_name]
        new_count = max(0, current_count - quantity)

        if new_count <= 0:
            # Remove item completely
            del self.items[item_name]
            del self.item_counts[item_name]

            # Remove from all_items and visible list
            for i, item_data in enumerate(self.all_items):
                if item_data['name'] == item_name:
                    self.all_items.pop(i)
                    break

            # Find and remove from visual list if present
            for i in range(self.item_list.count()):
                list_item = self.item_list.item(i)
                if list_item.data(Qt.UserRole).name == item_name:
                    self.item_list.takeItem(i)
                    break
        else:
            # Just update count
            self.item_counts[item_name] = new_count
            self._update_item_display(item_name)

        # Update total weight
        self._update_weight_display()

        # Emit signal that inventory changed
        self.inventoryChanged.emit()

        return item

    def _update_item_display(self, item_name: str):
        """
        Update the display text for an item with its current count.

        Args:
            item_name: Name of the item to update
        """
        quantity = self.item_counts[item_name]

        # Update in visible list if present
        for i in range(self.item_list.count()):
            list_item = self.item_list.item(i)
            if list_item.data(Qt.UserRole).name == item_name:
                list_item.setText(f"{item_name} ({quantity})")
                break

    def _update_weight_display(self):
        """Update the total weight display label."""
        total_weight = 0

        # Sum weight for all items
        for name, item_data in self.items.items():
            weight = item_data.get('weight', 1)
            count = self.item_counts[name]
            total_weight += weight * count

        self.weight_label.setText(f"Total Weight: {total_weight}")

    def _filter_items(self):
        """Filter items based on all current criteria."""
        self.current_main_category = self.main_category_combo.currentText()
        self.current_sub_category = self.sub_category_combo.currentText()
        self.current_search = self.search_box.text().lower()

        # Get weight filter value
        max_weight = 100
        if self.advanced_filter_checkbox.isChecked():
            max_weight = self.weight_filter.value()

        # Clear and rebuild visible list
        self.item_list.clear()

        # Track categories that have items
        categories_with_items = set()

        for item_data in self.all_items:
            name = item_data['name']
            main_category = item_data['main_category']
            sub_category = item_data['sub_category']
            weight = item_data['weight']

            # Skip items with quantity 0
            if self.item_counts.get(name, 0) <= 0:
                continue

            if self._passes_filter(main_category, sub_category, name, weight):
                # Add to visible list
                list_item = item_data['list_item'].clone()
                self.item_list.addItem(list_item)

                # Update categories that have items
                categories_with_items.add((main_category, sub_category))

        # Hide empty categories if option is unchecked
        if self.advanced_filter_checkbox.isChecked() and not self.show_empty_checkbox.isChecked():
            # TODO: Implement hiding empty categories in subcategory filter
            pass

    def _passes_filter(self, main_category: str, sub_category: str, name: str, weight: float) -> bool:
        """
        Check if an item passes the current filter criteria.

        Args:
            main_category: Main category of the item
            sub_category: Subcategory of the item
            name: Name of the item
            weight: Weight of the item

        Returns:
            True if the item passes all filters
        """
        # Check main category
        if self.current_main_category != "All" and main_category != self.current_main_category:
            return False

        # Check subcategory
        if self.current_sub_category != "All" and sub_category != self.current_sub_category:
            return False

        # Check search text
        if self.current_search and self.current_search not in name.lower():
            return False

        # Check weight if advanced filters are enabled
        if self.advanced_filter_checkbox.isChecked():
            max_weight = self.weight_filter.value()
            if weight > max_weight:
                return False

        return True

    def get_item_count(self, item_name: str) -> int:
        """
        Get the quantity of a specific item.

        Args:
            item_name: Name of the item

        Returns:
            Quantity of the item or 0 if not found
        """
        return self.item_counts.get(item_name, 0)

    def clear(self):
        """Clear all items from the inventory."""
        self.item_list.clear()
        self.items.clear()
        self.item_counts.clear()
        self.all_items.clear()
        self._update_weight_display()

    def get_selected_item(self) -> Optional[Tuple[TItem, int]]:
        """
        Get the currently selected item and its quantity.

        Returns:
            Tuple of (item, quantity) or None if nothing is selected
        """
        selected_items = self.item_list.selectedItems()
        if not selected_items:
            return None

        item = selected_items[0].data(Qt.UserRole)
        quantity = self.item_counts.get(item.name, 0)

        return item, quantity

    def _on_item_double_clicked(self, item):
        """Handle item double-click (e.g., for transferring items)."""
        selected_item = item.data(Qt.UserRole)
        if selected_item:
            quantity = self.item_counts.get(selected_item.name, 0)
            # Emit signal for item being dragged/transferred
            self.itemDragged.emit(selected_item, quantity)

    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter event."""
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        """Handle drop event to receive items."""
        if event.mimeData().hasText():
            try:
                # Parse dropped data
                data = event.mimeData().text()
                import json
                item_data = json.loads(data)

                # Create item from data
                from item.item import TItem
                if 'name' in item_data and 'type' in item_data:
                    item = TItem(
                        name=item_data['name'],
                        item_type=item_data['type'],
                        icon_path=item_data.get('icon_path'),
                        properties=item_data.get('properties', {})
                    )

                    # Add to inventory
                    quantity = item_data.get('quantity', 1)
                    if self.add_item(item, quantity):
                        # Emit signal that item was dropped here
                        self.itemDropped.emit(item, quantity)
                        event.acceptProposedAction()
                    else:
                        event.ignore()
                else:
                    event.ignore()
            except Exception:
                event.ignore()
        else:
            event.ignore()
