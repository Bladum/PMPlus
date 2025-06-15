"""
engine/gui/other/widget/unit_list_widget.py

Widget for managing and displaying a list of units with filtering capabilities in the XCOM GUI.
Standardized: All docstrings and comments follow the unified documentation style (2025-06-14).
"""

from typing import Dict, List, Any, Optional, Callable
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QIcon, QPixmap, QFont
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QListWidget, QListWidgetItem,
    QLabel, QPushButton, QLineEdit, QAbstractItemView, QGroupBox, QScrollArea
)

from gui.theme_manager import XcomStyle, px
from unit.unit import TUnit


class TUnitListWidget(QWidget):
    """
    Widget for displaying and managing a list of units.
    Inherits from QWidget.
    """

    # Signal emitted when a unit is selected
    unitSelected = Signal(TUnit)

    # Signal emitted when unit data changes (e.g., equipment changed)
    unitChanged = Signal(TUnit)

    def __init__(self, parent=None, title="Units"):
        """
        Initialize the unit list widget with filter and search capabilities.

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
        self.search_box.setPlaceholderText("Search units...")
        self.search_box.setStyleSheet(XcomStyle.lineedit())
        self.search_box.textChanged.connect(self._filter_units)
        self.box_layout.addWidget(self.search_box)

        # Filter combo box for unit types
        self.filter_combo = QComboBox()
        self.filter_combo.setStyleSheet(XcomStyle.combobox())
        self.filter_combo.currentTextChanged.connect(self._filter_units)
        self.box_layout.addWidget(self.filter_combo)

        # Unit list
        self.unit_list = QListWidget()
        self.unit_list.setStyleSheet(XcomStyle.listwidget())
        self.unit_list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.unit_list.itemSelectionChanged.connect(self._on_selection_changed)
        self.unit_list.setIconSize(QSize(32, 32))
        self.box_layout.addWidget(self.unit_list)

        # Data storage
        self.all_units: List[Dict[str, Any]] = []  # Store all units for filtering
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
        self.filter_combo.addItem("Soldiers")
        self.filter_combo.addItem("Tanks")
        self.filter_combo.addItem("Aliens")

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

    def add_unit(self, unit: TUnit, icon_path: Optional[str] = None) -> bool:
        """
        Add a unit to the list.

        Args:
            unit: Unit to add
            icon_path: Path to unit icon (uses unit.icon_path if None)

        Returns:
            True if unit was added successfully
        """
        if not unit:
            return False

        # Create icon
        icon_path = icon_path if icon_path else getattr(unit, 'icon_path', None)
        icon = None
        if icon_path:
            icon = QIcon(QPixmap(icon_path).scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # Create list item
        unit_name = unit.name if hasattr(unit, 'name') else "Unnamed Unit"
        unit_type = unit.unit_type if hasattr(unit, 'unit_type') else "Unknown"
        unit_rank = unit.rank if hasattr(unit, 'rank') else ""

        item = QListWidgetItem(icon, f"{unit_name} ({unit_rank})")

        # Store unit in item data
        item.setData(Qt.UserRole, unit)

        # Store for filtering
        self.all_units.append({
            'unit': unit,
            'name': unit_name,
            'icon': icon,
            'type': unit_type,
            'rank': unit_rank,
            'item': item
        })

        # Add to visible list if it passes current filter
        if self._passes_filter(unit_type, unit_name):
            self.unit_list.addItem(item)

        return True

    def add_units(self, units: List[TUnit]):
        """
        Add multiple units to the list.

        Args:
            units: List of units to add
        """
        for unit in units:
            self.add_unit(unit)

    def remove_unit(self, unit_name: str) -> bool:
        """
        Remove a unit from the list.

        Args:
            unit_name: Name of the unit to remove

        Returns:
            True if unit was found and removed
        """
        # Find unit in all_units
        for i, unit_data in enumerate(self.all_units):
            if unit_data['name'] == unit_name:
                # Remove from all_units
                self.all_units.pop(i)

                # Remove from visible list if present
                for row in range(self.unit_list.count()):
                    item = self.unit_list.item(row)
                    unit = item.data(Qt.UserRole)
                    if unit.name == unit_name:
                        self.unit_list.takeItem(row)
                        break

                return True

        return False

    def clear(self):
        """Clear all units from the list."""
        self.unit_list.clear()
        self.all_units = []

    def get_selected_unit(self) -> Optional[TUnit]:
        """Get the currently selected unit."""
        selected_items = self.unit_list.selectedItems()
        if selected_items:
            return selected_items[0].data(Qt.UserRole)
        return None

    def select_unit_by_name(self, name: str) -> bool:
        """
        Select a unit by name.

        Args:
            name: Name of the unit to select

        Returns:
            True if unit was found and selected
        """
        for row in range(self.unit_list.count()):
            item = self.unit_list.item(row)
            unit = item.data(Qt.UserRole)
            if unit.name == name:
                self.unit_list.setCurrentItem(item)
                return True

        return False

    def _filter_units(self):
        """Filter units based on selected category and search text."""
        self.current_filter = self.filter_combo.currentText()
        self.current_search = self.search_box.text().lower()

        # Clear and rebuild visible list
        self.unit_list.clear()

        for unit_data in self.all_units:
            unit_type = unit_data['type']
            unit_name = unit_data['name']

            if self._passes_filter(unit_type, unit_name):
                self.unit_list.addItem(unit_data['item'])

    def _passes_filter(self, unit_type: str, unit_name: str) -> bool:
        """Check if a unit passes the current filter and search criteria."""
        # Check type filter
        type_match = (self.current_filter == "All" or
                     unit_type.lower() == self.current_filter.lower())

        # Check search text
        search_match = (not self.current_search or
                       self.current_search in unit_name.lower())

        return type_match and search_match

    def _on_selection_changed(self):
        """Handle selection changes and emit unitSelected signal."""
        selected_unit = self.get_selected_unit()
        if selected_unit:
            self.unitSelected.emit(selected_unit)

    def update_unit(self, updated_unit: TUnit):
        """
        Update a unit's data and display.

        Args:
            updated_unit: Unit with updated data
        """
        # Find and update in all_units
        for unit_data in self.all_units:
            if unit_data['unit'].name == updated_unit.name:
                unit_data['unit'] = updated_unit

                # Update display text
                unit_rank = updated_unit.rank if hasattr(updated_unit, 'rank') else ""
                unit_data['item'].setText(f"{updated_unit.name} ({unit_rank})")

                # Emit signal that unit has been updated
                self.unitChanged.emit(updated_unit)
                break
