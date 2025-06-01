"""
Barracks GUI Module

This module contains the BarracksGUI implementation for XCOM inventory system.
It handles unit management, equipment, and inventory interfaces.
"""

import sys
import os

from gui.gui_core import TGuiCoreScreen

# Add parent directory to path for imports to work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from typing import Optional, Dict, Any, List
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
                             QGroupBox, QPushButton, QComboBox, QListWidgetItem)

from syf.theme_styles import XcomTheme, XcomStyle, GRID, px
from syf.game_data import GameData, ItemType
from syf.inventory_system import (InventoryItem, InventoryTemplate, UnitInventoryManager)

class TGuiBarracks(TGuiCoreScreen):
    """
    BarracksGUI implements the barracks screen with unit management,
    equipment loadouts, and inventory functionality.
    """

    def __init__(self, parent=None):
        """Initialize the barracks screen widget."""
        super().__init__(parent)

        # Initialize state variables
        self.unit_inventory_manager = UnitInventoryManager()
        self.current_unit: Optional[str] = None
        self.saved_template: Optional[InventoryTemplate] = None

        # Widget references
        self.equipment_slots = []
        self.item_list_widget = None
        self.weight_label = None
        self.unit_info_label = None
        self.unit_list_widget = None
        self.load_template_button = None
        self.summary_label = None

        # Set up the UI
        self._setup_ui()

    def _setup_ui(self):
        """Set up the UI components."""
        # Import custom widgets
        from engine.gui.widgets import EquipmentSlotWidget, ItemListWidget, UnitListWidget

        # Set the layout
        self.setStyleSheet(f"background: {XcomTheme.BG_MID};")
        self.setContentsMargins(0, 0, 0, 0)

        # Create equipment slots from data structure
        for slot_data in GameData.get_equipment_slots():
            gx, gy = slot_data["position"]
            r_adj, g_adj, b_adj = slot_data["color_adjust"]

            slot_bg = self._adjust_color(XcomTheme.BG_LIGHT,
                                       int(r_adj * 255),
                                       int(g_adj * 255),
                                       int(b_adj * 255))

            slot = EquipmentSlotWidget(slot_data["name"], self,
                                       label_text=slot_data["name"],
                                       slot_type=slot_data["type"])
            slot.set_background_color(slot_bg)
            slot.set_border_color(XcomTheme.BORDER_COLOR)
            slot.setFixedSize(px(GRID * 4), px(GRID * 4))
            slot.move(px(GRID * gx), px(GRID * gy))
            slot.show()
            self.equipment_slots.append(slot)

        # TEMPLATE SYSTEM - Add template buttons
        save_template_button = QPushButton("SAVE", self)
        save_template_button.setFixedSize(px(GRID * 2), px(GRID * 1))
        save_template_button.move(px(GRID * 25), px(GRID * 8))
        save_template_button.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_SMALL))
        save_template_button.setStyleSheet(XcomStyle.pushbutton(rounded=True, border_width=1))
        save_template_button.clicked.connect(self._save_template)
        save_template_button.show()

        self.load_template_button = QPushButton("LOAD", self)
        self.load_template_button.setFixedSize(px(GRID * 2), px(GRID * 1))
        self.load_template_button.move(px(GRID * 25), px(GRID * 9))
        self.load_template_button.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_SMALL))
        self.load_template_button.setStyleSheet(XcomStyle.pushbutton(rounded=True, border_width=1))
        self.load_template_button.clicked.connect(self._load_template)
        self.load_template_button.setEnabled(False)  # Disabled until template is saved
        self.load_template_button.show()

        # Add a test button for equipment slot validation
        test_button = QPushButton("TEST", self)
        test_button.setFixedSize(px(GRID * 2), px(GRID * 1))
        test_button.move(px(GRID * 25), px(GRID * 10))
        test_button.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_SMALL))
        test_button.setStyleSheet(XcomStyle.pushbutton(rounded=True, border_width=1))
        test_button.clicked.connect(self._test_equipment_slots)
        test_button.show()

        # Weight display label between Armour and Weapon slots
        self.weight_label = QLabel("Weight: 0", self)
        self.weight_label.setFixedSize(px(GRID * 4), px(GRID // 2))
        self.weight_label.move(px(GRID * 24), px(GRID * 6))
        self.weight_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.weight_label.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_NORMAL, QFont.Bold))
        self.weight_label.setStyleSheet(f"color: {XcomTheme.ACCENT_YELLOW}; background: transparent;")
        self.weight_label.show()

        # Soldier head image (non-interactive, just for display)
        head_display = QLabel(self)
        head_display.setFixedSize(px(GRID * 4), px(GRID * 4))
        head_display.move(px(GRID * 24), px(GRID * 1))
        head_display.setStyleSheet(f"""
            QLabel {{
                background: {self._adjust_color(XcomTheme.BG_LIGHT, -int(0.05 * 255), -int(0.05 * 255), -int(0.05 * 255))};
                border: 3px solid {XcomTheme.BORDER_COLOR};
                border-radius: 4px;
            }}
        """)
        head_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        head_display.setText("HEAD")
        head_display.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_SMALL))
        head_display.show()

        # Place summary groupbox
        summary_groupbox = QGroupBox("Summary", self)
        summary_groupbox.setStyleSheet(XcomStyle.groupbox())
        summary_groupbox.setFixedSize(px(GRID * 6), px(GRID * 4))
        summary_groupbox.move(px(GRID * 1), px(GRID * 1))
        summary_groupbox.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # Add summary content with left-top alignment and monospace font for table formatting
        summary_layout = QVBoxLayout(summary_groupbox)
        summary_layout.setContentsMargins(px(1), px(3), px(1), px(1))
        summary_layout.setSpacing(0)
        summary_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.summary_label = QLabel("Units:     0\nTanks:     0\nDogs:      0\nAliens:    0\nCapacity: 50", summary_groupbox)
        self.summary_label.setFont(QFont("Courier", XcomTheme.FONT_SIZE_SMALL))  # Monospace font for alignment
        self.summary_label.setStyleSheet(f"color: {XcomTheme.TEXT_BRIGHT}; background: transparent;")
        self.summary_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        summary_layout.addWidget(self.summary_label)

        summary_groupbox.show()

        # Unit list widget
        unit_list_groupbox = QGroupBox("", self)
        unit_list_groupbox.setStyleSheet(XcomStyle.groupbox())
        unit_list_groupbox.setFixedSize(px(GRID * 6), px(GRID * 14))
        unit_list_groupbox.move(px(GRID * 1), px(GRID * 6))
        unit_list_groupbox.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        unit_list_groupbox.setContentsMargins(px(0.5), px(0.5), 0, 0)

        unit_list_layout = QVBoxLayout(unit_list_groupbox)
        unit_list_layout.setContentsMargins(px(0.5), px(0.5), 0, 0)
        unit_list_layout.setSpacing(px(0.5))

        unit_filter_combo = QComboBox(unit_list_groupbox)
        unit_filter_combo.clear()
        for unit_category in GameData.get_unit_categories():
            unit_filter_combo.addItem(QIcon(QPixmap(unit_category["icon"]).scaled(32, 32)), unit_category["name"])
        unit_filter_combo.setStyleSheet(XcomStyle.combobox())
        unit_list_layout.addWidget(unit_filter_combo)

        self.unit_list_widget = UnitListWidget(unit_list_groupbox)

        # Load initial units
        for name, icon_path, info in GameData.get_current_base_units():
            item = QListWidgetItem(QIcon(QPixmap(icon_path).scaled(32, 32)), name)
            self.unit_list_widget.addUnitWithInfo(item, info)
        self.unit_list_widget.setStyleSheet(XcomStyle.listwidget())

        # Connect unit selection signal
        self.unit_list_widget.unitSelected.connect(self._on_unit_selected)

        # Connect filter combo to filtering function
        unit_filter_combo.currentTextChanged.connect(self.unit_list_widget.filter_units)

        unit_list_layout.addWidget(self.unit_list_widget)
        unit_list_groupbox.show()

        # Item list widget
        item_list = QGroupBox("", self)
        item_list.setStyleSheet(XcomStyle.groupbox())
        item_list.setFixedSize(px(GRID * 6), px(GRID * 21))
        item_list.move(px(GRID * 33), px(GRID * 1))
        item_list.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        item_list.setContentsMargins(px(0.5), px(0.5), 0, 0)

        item_list_layout = QVBoxLayout(item_list)
        item_list_layout.setContentsMargins(px(0.5), px(0.5), 0, 0)
        item_list_layout.setSpacing(px(0.5))

        item_filter_combo = QComboBox(item_list)
        item_filter_combo.clear()
        for category in GameData.get_item_categories():
            item_filter_combo.addItem(QIcon(QPixmap(category["icon"]).scaled(32, 32)), category["name"])
        item_filter_combo.setStyleSheet(XcomStyle.combobox())
        item_list_layout.addWidget(item_filter_combo)

        self.item_list_widget = ItemListWidget(item_list)

        # Initialize with current base items
        for name, icon_path, info, count in GameData.get_current_base_items():
            item = QListWidgetItem(QIcon(QPixmap(icon_path).scaled(32, 32, Qt.KeepAspectRatio, Qt.FastTransformation)),
                                f"{name} ({count})")
            self.item_list_widget.addItemWithInfo(item, info, count)
        self.item_list_widget.setStyleSheet(XcomStyle.listwidget())

        # Connect filter combo to filtering function
        item_filter_combo.currentTextChanged.connect(self.item_list_widget.filter_items)

        item_list_layout.addWidget(self.item_list_widget)
        item_list.show()

        # Stats groupbox
        unit_stats_groupbox = QGroupBox("Stats", self)
        unit_stats_groupbox.setStyleSheet(XcomStyle.groupbox())
        unit_stats_groupbox.setFixedSize(px(GRID * 11), px(GRID * 8))
        unit_stats_groupbox.move(px(GRID * 8), px(GRID * 6))
        unit_stats_groupbox.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        unit_stats_groupbox.setContentsMargins(px(0.5), px(0.5), 0, 0)
        unit_stats_groupbox.show()

        # Traits groupbox
        traits_groupbox = QGroupBox("Traits", self)
        traits_groupbox.setStyleSheet(XcomStyle.groupbox())
        traits_groupbox.setFixedSize(px(GRID * 11), px(GRID * 8))
        traits_groupbox.move(px(GRID * 8), px(GRID * 14))
        traits_groupbox.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        traits_groupbox.setContentsMargins(px(0.5), px(0.5), 0, 0)
        traits_groupbox.show()

        # Fire button
        fire_button = QPushButton("Fire", self)
        fire_button.setFixedSize(px(GRID * 2 - 2), px(GRID - 2))
        fire_button.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_NORMAL))
        fire_button.move(px(GRID * 3), px(GRID * 21))
        fire_button.show()

        # Basic info widget
        basic_info_groupbox = QGroupBox("Basic info", self)
        basic_info_groupbox.setStyleSheet(XcomStyle.groupbox())
        basic_info_groupbox.setFixedSize(px(GRID * 11), px(GRID * 4))
        basic_info_groupbox.move(px(GRID * 8), px(GRID * 1))
        basic_info_groupbox.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # Add unit info label with left-top alignment
        basic_info_layout = QVBoxLayout(basic_info_groupbox)
        basic_info_layout.setContentsMargins(px(1), px(3), px(1), px(1))
        basic_info_layout.setSpacing(px(1))
        basic_info_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.unit_info_label = QLabel("No unit selected", basic_info_groupbox)
        self.unit_info_label.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_NORMAL, QFont.Bold))
        self.unit_info_label.setStyleSheet(f"color: {XcomTheme.ACCENT_BLUE}; background: transparent;")
        self.unit_info_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        basic_info_layout.addWidget(self.unit_info_label)

        basic_info_groupbox.show()

        # Initialize equipment slot states (default 2 equipment slots enabled)
        self._update_equipment_slot_states(2)

        # Update initial summary
        self.update_summary_display()

        # Update globals in widgets module to ensure proper cross-module communication
        import engine.gui.widgets
        engine.gui.widgets.equipment_slots_global = self.equipment_slots
        engine.gui.widgets.item_list_widget_global = self.item_list_widget
        engine.gui.widgets.weight_label_global = self.weight_label
        engine.gui.widgets.unit_inventory_manager_global = self.unit_inventory_manager
        engine.gui.widgets.current_unit_global = self.current_unit
        engine.gui.widgets.unit_info_label_global = self.unit_info_label

        # Auto-select first unit if any units exist
        if GameData.get_current_base_units() and len(GameData.get_current_base_units()) > 0:
            self.unit_list_widget.setCurrentRow(0)
            first_unit_name = GameData.get_current_base_units()[0][0]
            self._on_unit_selected(first_unit_name)

    def screen_activated(self):
        """Called when this screen becomes active."""
        # Refresh data when screen becomes active
        self.refresh_base_data()

    def screen_deactivated(self):
        """Called when another screen becomes active."""
        pass

    def refresh_base_data(self):
        """Refresh unit and item lists for the current active base."""
        # Reset current unit
        self.current_unit = None
        self.unit_info_label.setText("No unit selected")

        # Clear equipment slots
        for slot in self.equipment_slots:
            if slot.item:
                slot.remove_item()

        # Load new base data
        units = GameData.get_current_base_units()
        items = GameData.get_current_base_items()

        # Populate unit list
        if self.unit_list_widget:
            self.unit_list_widget.clear()  # Clear before adding new items
            for name, icon_path, info in units:
                item = QListWidgetItem(QIcon(QPixmap(icon_path).scaled(32, 32)), name)
                self.unit_list_widget.addUnitWithInfo(item, info)

            # Auto-select first unit if any units exist
            if units and len(units) > 0:
                self.unit_list_widget.setCurrentRow(0)
                first_unit_name = units[0][0]
                self._on_unit_selected(first_unit_name)

        # Populate item list
        if self.item_list_widget:
            self.item_list_widget.clear()  # Clear before adding new items
            for name, icon_path, info, count in items:
                item = QListWidgetItem(QIcon(QPixmap(icon_path).scaled(32, 32, Qt.KeepAspectRatio, Qt.FastTransformation)),
                                    f"{name} ({count})")
                self.item_list_widget.addItemWithInfo(item, info, count)

        # Update summary
        self.update_summary_display()

    def update_summary_display(self):
        """Update summary statistics with formatted table display."""
        if self.summary_label:
            stats = GameData.get_base_summary()
            # Format as table with aligned columns
            summary_text = f"Units:    {stats['soldiers']:2d}\nTanks:    {stats['tanks']:2d}\nDogs:     {stats['dogs']:2d}\nAliens:   {stats['aliens']:2d}\nCapacity: {stats['capacity']:2d}"
            self.summary_label.setText(summary_text)

    def _update_weight_display(self):
        """Update the weight display label with total equipment weight."""
        if not self.weight_label or not self.equipment_slots:
            return

        total_weight: int = 0
        for slot in self.equipment_slots:
            if slot.item:
                total_weight += slot.item.weight

        self.weight_label.setText(f"Weight: {total_weight}")

    def _update_equipment_slot_states(self, enabled_count: int):
        """Enable or disable equipment slots based on armor configuration."""
        if not self.equipment_slots:
            return

        equipment_slots = [slot for slot in self.equipment_slots if slot.slot_type == ItemType.EQUIPMENT]

        for i, slot in enumerate(equipment_slots):
            if i < enabled_count:
                # Enable slot
                slot.enabled = True
                slot.setAcceptDrops(True)
                slot.set_border_color(XcomTheme.BORDER_COLOR)
                slot._original_border_color = XcomTheme.BORDER_COLOR
            else:
                # Disable slot
                slot.enabled = False
                slot.setAcceptDrops(False)

                # Move item to inventory if slot has item
                if slot.item and self.item_list_widget:
                    item = slot.remove_item()
                    self.item_list_widget.add_item_to_inventory(item, 1)

                # Set gray appearance
                slot.set_border_color(XcomTheme.TEXT_DIM)
                slot._original_border_color = XcomTheme.TEXT_DIM

            slot.update()

    def _on_unit_selected(self, unit_name: str):
        """Handle unit selection from the list."""
        self.current_unit = unit_name
        self.unit_info_label.setText(f"Unit: {unit_name}")

        # Validate equipment slots after unit selection
        from engine.gui.widgets import validate_and_update_equipment_slots
        validate_and_update_equipment_slots()

    def _save_template(self):
        """Save current equipment setup as template in memory."""
        if not self.equipment_slots:
            print("No equipment slots available for saving template")
            return

        # Create equipment data dictionary
        equipment_data = {}
        for slot in self.equipment_slots:
            slot_key = slot.slot_name
            if slot.item:
                equipment_data[slot_key] = slot.item.to_dict()
            else:
                equipment_data[slot_key] = None

        # Save template in memory
        self.saved_template = InventoryTemplate("Memory Template", equipment_data)

        # Enable load button
        if self.load_template_button:
            self.load_template_button.setEnabled(True)

        print("Template saved to memory")

    def _load_template(self):
        """Load template from memory."""
        if not self.saved_template or not self.equipment_slots:
            print("No template available or no equipment slots")
            return

        # Clear current equipment and return to inventory
        for slot in self.equipment_slots:
            if slot.item:
                item = slot.remove_item()
                if item and self.item_list_widget:
                    self.item_list_widget.add_item_to_inventory(item, 1)

        # Load template equipment
        for slot in self.equipment_slots:
            slot_key = slot.slot_name
            if slot_key in self.saved_template.equipment_data and self.saved_template.equipment_data[slot_key]:
                try:
                    item = InventoryItem.from_dict(self.saved_template.equipment_data[slot_key])
                    slot.add_item(item)
                    # Remove from inventory if it exists
                    if self.item_list_widget:
                        self.item_list_widget.remove_item_from_inventory(item.name, 1)
                except Exception as e:
                    print(f"Error loading item for slot {slot_key}: {e}")

        # After loading template, validate equipment slots based on loaded armor
        from engine.gui.widgets import validate_and_update_equipment_slots
        validate_and_update_equipment_slots()

        print("Template loaded from memory")

    def _test_equipment_slots(self):
        """Test function for equipment slot validation."""
        import engine.gui.widgets
        engine.gui.widgets.test_equipment_slot_validation()

    def _adjust_color(self, hex_color: str, r: int = 0, g: int = 0, b: int = 0) -> str:
        """
        Adjust RGB values of a hex color.

        Args:
            hex_color: Base color in hex format (#RRGGBB)
            r: Red adjustment (-255 to 255)
            g: Green adjustment (-255 to 255)
            b: Blue adjustment (-255 to 255)

        Returns:
            Adjusted color in hex format
        """
        from PySide6.QtGui import QColor
        c = QColor(hex_color)
        c = QColor(min(255, max(0, c.red() + r)),
                  min(255, max(0, c.green() + g)),
                  min(255, max(0, c.blue() + b)))
        return c.name()
