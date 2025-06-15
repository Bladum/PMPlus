"""
engine/gui/other/widget/craft_list_widget.py

Widget for managing and displaying a list of crafts with filtering capabilities in the XCOM GUI.

Classes:
    TCraftListWidget: Widget for displaying and managing a list of crafts.

Last standardized: 2025-06-15
"""

from typing import Dict, List, Any, Optional, Callable
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QIcon, QPixmap, QFont
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QListWidget, QListWidgetItem,
    QLabel, QPushButton, QLineEdit, QAbstractItemView, QGroupBox, QScrollArea
)
from gui.theme_manager import XcomStyle, px
from craft.craft import TCraft


class TCraftListWidget(QWidget):
    """
    Widget for displaying and managing a list of crafts.

    Attributes:
        craftSelected (Signal): Emitted when a craft is selected.
        craftChanged (Signal): Emitted when craft data changes (e.g., equipment changed).
    """

    # Signal emitted when a craft is selected
    craftSelected = Signal(TCraft)

    # Signal emitted when craft data changes (e.g., equipment changed)
    craftChanged = Signal(TCraft)

    def __init__(self, parent=None, title="Crafts"):
        """
        Initialize the craft list widget with filter and search capabilities.

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
        self.search_box.setPlaceholderText("Search crafts...")
        self.search_box.setStyleSheet(XcomStyle.lineedit())
        self.search_box.textChanged.connect(self._filter_crafts)
        self.box_layout.addWidget(self.search_box)

        # Filter combo box for craft types
        self.filter_combo = QComboBox()
        self.filter_combo.setStyleSheet(XcomStyle.combobox())
        self.filter_combo.currentTextChanged.connect(self._filter_crafts)
        self.box_layout.addWidget(self.filter_combo)

        # Craft list
        self.craft_list = QListWidget()
        self.craft_list.setStyleSheet(XcomStyle.listwidget())
        self.craft_list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.craft_list.itemSelectionChanged.connect(self._on_selection_changed)
        self.craft_list.setIconSize(QSize(32, 32))
        self.box_layout.addWidget(self.craft_list)

        # Data storage
        self.all_crafts: List[Dict[str, Any]] = []  # Store all crafts for filtering
        self.current_filter = "All"
        self.current_search = ""

        # Add group box to main layout
        self.layout.addWidget(self.group_box)

        # Initialize filters
        self._setup_default_filters()

    def _setup_default_filters(self):
        """Setup default category filters."""
        self.filter_combo.clear()
        self.filter_combo.addItem("All")
        self.filter_combo.addItem("Interceptor")
        self.filter_combo.addItem("Transport")
        self.filter_combo.addItem("Battleship")

    def set_categories(self, categories: List[Dict[str, Any]]):
        """
        Set custom category filters with icons.

        Args:
            categories: List of category dictionaries with 'name' and 'icon' keys
        """
        self.filter_combo.clear()

        for category in categories:
            icon = QIcon(QPixmap(category["icon"]).scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.filter_combo.addItem(icon, category["name"])

    def add_craft(self, craft: TCraft, icon_path: Optional[str] = None) -> bool:
        """
        Add a craft to the list.

        Args:
            craft: Craft to add
            icon_path: Path to craft icon (uses craft.icon_path if None)

        Returns:
            True if craft was added successfully
        """
        if not craft:
            return False

        # Create icon
        icon_path = icon_path if icon_path else getattr(craft, 'icon_path', None)
        icon = None
        if icon_path:
            icon = QIcon(QPixmap(icon_path).scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # Create list item
        craft_name = craft.name if hasattr(craft, 'name') else "Unnamed Craft"
        craft_type = craft.craft_type if hasattr(craft, 'craft_type') else "Unknown"
        craft_status = craft.status if hasattr(craft, 'status') else "Ready"

        item = QListWidgetItem(icon, f"{craft_name} ({craft_status})")

        # Store craft in item data
        item.setData(Qt.UserRole, craft)

        # Store for filtering
        self.all_crafts.append({
            'craft': craft,
            'name': craft_name,
            'icon': icon,
            'type': craft_type,
            'status': craft_status,
            'item': item
        })

        # Add to visible list if it passes current filter
        if self._passes_filter(craft_type, craft_name):
            self.craft_list.addItem(item)

        return True

    def add_crafts(self, crafts: List[TCraft]):
        """
        Add multiple crafts to the list.

        Args:
            crafts: List of crafts to add
        """
        for craft in crafts:
            self.add_craft(craft)

    def remove_craft(self, craft_name: str) -> bool:
        """
        Remove a craft from the list.

        Args:
            craft_name: Name of the craft to remove

        Returns:
            True if craft was found and removed
        """
        # Find craft in all_crafts
        for i, craft_data in enumerate(self.all_crafts):
            if craft_data['name'] == craft_name:
                # Remove from all_crafts
                self.all_crafts.pop(i)

                # Remove from visible list if present
                for row in range(self.craft_list.count()):
                    item = self.craft_list.item(row)
                    craft = item.data(Qt.UserRole)
                    if craft.name == craft_name:
                        self.craft_list.takeItem(row)
                        break

                return True

        return False

    def clear(self):
        """Clear all crafts from the list."""
        self.craft_list.clear()
        self.all_crafts = []

    def get_selected_craft(self) -> Optional[TCraft]:
        """Get the currently selected craft."""
        selected_items = self.craft_list.selectedItems()
        if selected_items:
            return selected_items[0].data(Qt.UserRole)
        return None

    def select_craft_by_name(self, name: str) -> bool:
        """
        Select a craft by name.

        Args:
            name: Name of the craft to select

        Returns:
            True if craft was found and selected
        """
        for row in range(self.craft_list.count()):
            item = self.craft_list.item(row)
            craft = item.data(Qt.UserRole)
            if craft.name == name:
                self.craft_list.setCurrentItem(item)
                return True

        return False

    def _filter_crafts(self):
        """Filter crafts based on selected category and search text."""
        self.current_filter = self.filter_combo.currentText()
        self.current_search = self.search_box.text().lower()

        # Clear and rebuild visible list
        self.craft_list.clear()

        for craft_data in self.all_crafts:
            craft_type = craft_data['type']
            craft_name = craft_data['name']

            if self._passes_filter(craft_type, craft_name):
                self.craft_list.addItem(craft_data['item'])

    def _passes_filter(self, craft_type: str, craft_name: str) -> bool:
        """Check if a craft passes the current filter and search criteria."""
        # Check type filter
        type_match = (self.current_filter == "All" or
                     craft_type.lower() == self.current_filter.lower())

        # Check search text
        search_match = (not self.current_search or
                       self.current_search in craft_name.lower())

        return type_match and search_match

    def _on_selection_changed(self):
        """Handle selection changes and emit craftSelected signal."""
        selected_craft = self.get_selected_craft()
        if selected_craft:
            self.craftSelected.emit(selected_craft)

    def update_craft(self, updated_craft: TCraft):
        """
        Update a craft's data and display.

        Args:
            updated_craft: Craft with updated data
        """
        # Find and update in all_crafts
        for craft_data in self.all_crafts:
            if craft_data['craft'].name == updated_craft.name:
                craft_data['craft'] = updated_craft

                # Update display text
                craft_status = updated_craft.status if hasattr(updated_craft, 'status') else "Ready"
                craft_data['item'].setText(f"{updated_craft.name} ({craft_status})")

                # Emit signal that craft has been updated
                self.craftChanged.emit(updated_craft)
                break

    def update_craft_status(self, craft_name: str, new_status: str):
        """
        Update a craft's status display.

        Args:
            craft_name: Name of the craft to update
            new_status: New status text to display
        """
        # Find and update in all_crafts
        for craft_data in self.all_crafts:
            if craft_data['craft'].name == craft_name:
                # Update status field
                craft_data['status'] = new_status
                if hasattr(craft_data['craft'], 'status'):
                    craft_data['craft'].status = new_status

                # Update display text
                craft_data['item'].setText(f"{craft_name} ({new_status})")
                break
