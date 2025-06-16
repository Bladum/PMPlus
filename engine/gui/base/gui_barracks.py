"""
engine/gui/base/gui_barracks.py

Barracks GUI Module for XCOM/AlienFall

Implements the barracks management screen, providing unit roster, equipment assignment, loadout templates, and inventory management for the base barracks interface.

Classes:
    TGuiBarracks: Main barracks GUI screen for unit and inventory management.
    UnitListWidget: Custom widget for displaying the list of units in the barracks.
    ItemListWidget: Custom widget for displaying the list of items available for equipment.

Last standardized: 2025-06-15
"""

import os
from typing import Optional, Dict, List, Tuple, Any

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QIcon, QPixmap, QColor, QCursor
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel,
                             QGroupBox, QPushButton, QComboBox, QListWidgetItem, QListWidget,
                             QToolTip, QProgressBar, QScrollArea, QWidget, QAbstractItemView,
                             QInputDialog, QMessageBox)

from gui.gui_core import TGuiCoreScreen
from gui.other.slots.unit_inventory_slot import TUnitInventorySlot
from gui.theme_manager import XcomTheme, GRID, px, XcomStyle
from unit.unit import TUnit

from item.item_type import TItemType
from item.item import TItem
from unit.unit_inv_manager import TUnitInventoryManager, InventoryTemplate

# Constants for UI layout and configuration
MAX_EQUIPMENT_SLOTS = 8
STATS_ATTRIBUTES = ["health", "stamina", "strength", "reactions", "accuracy", "throwing"]


class TGuiBarracks(TGuiCoreScreen):
    """
    Main barracks GUI screen for unit and inventory management.

    Responsibilities:
    - Display and manage the unit roster for the current base.
    - Allow equipping and unequipping items on units.
    - Support saving and loading equipment loadout templates.
    - Show unit stats, traits, and summary information.
    - Integrate with unit inventory and item management systems.

    Attributes:
        game: Reference to the main game instance.
        unit_inventory_manager: Manager for unit inventory operations.
        current_unit: Currently selected unit name.
        equipment_slots: List of equipment slot widgets.
        item_list_widget: Widget displaying available items.
        unit_list_widget: Widget displaying available units.
        weight_label: Label showing equipment weight.
        unit_info_label: Label showing unit information.
        load_template_button: Button for loading equipment templates.
        summary_label: Label showing barracks summary information.

    Signals:
        equipment_changed (str, str): Emitted when equipment changes (slot_name, item_name).
        unit_equipped (str): Emitted when a unit is equipped (unit_name).

    Methods:
        __init__(parent=None): Initialize the barracks GUI screen.
        _setup_ui(): Set up the main UI layout and widgets.
        _setup_equipment_slots(): Set up equipment slot widgets.
        _setup_template_controls(): Set up loadout template controls.
        _setup_weight_label(): Set up the equipment weight label.
        _setup_unit_avatar(): Set up the unit avatar display.
        _setup_summary_box(): Set up the summary information box.
        _setup_unit_list(): Set up the unit list display.
        _setup_item_list(): Set up the item list display.
        _setup_stats_box(): Set up the unit stats display.
        _setup_traits_box(): Set up the unit traits display.
        _setup_fire_button(): Set up the fire button for units.
        _setup_basic_info_box(): Set up the basic information display for units.
        _finalize_ui_setup(): Finalize the UI setup after all components are created.

    """
    # Custom signals for equipment changes
    equipment_changed = Signal(str, str)  # (slot_name, item_name)
    unit_equipped = Signal(str)  # unit_name

    def __init__(self, parent=None):
        """Initialize the barracks screen widget."""
        super().__init__(parent)

        from engine.engine.game import TGame
        self.game = TGame()

        # Initialize state variables
        self.unit_inventory_manager = TUnitInventoryManager()
        self.current_unit: Optional[str] = None
        self.saved_templates: Dict[str, InventoryTemplate] = {}  # Store multiple templates
        self.current_template_name: str = "Default"
        self.selected_unit_data: Optional[TUnit] = None

        # Widget references
        self.equipment_slots = []
        self.item_list_widget = None
        self.weight_label = None
        self.unit_info_label = None
        self.unit_list_widget = None
        self.load_template_button = None
        self.template_combo = None
        self.summary_label = None
        self.stat_bars = {}
        self.traits_layout = None
        self.unit_avatar_label = None

        # Set up the UI
        self._setup_ui()

        # Connect internal signals
        self.equipment_changed.connect(self._on_equipment_changed)
        self.unit_equipped.connect(self._update_unit_equipment_status)

    def _setup_ui(self) -> None:
        """
        Set up all UI components for the barracks screen.
        This method is split into smaller helpers for clarity and maintainability.
        """
        self._setup_equipment_slots()
        self._setup_template_controls()
        self._setup_weight_label()
        self._setup_unit_avatar()
        self._setup_summary_box()
        self._setup_unit_list()
        self._setup_item_list()
        self._setup_stats_box()
        self._setup_traits_box()
        self._setup_fire_button()
        self._setup_basic_info_box()
        self._finalize_ui_setup()

    def _setup_equipment_slots(self) -> None:
        """Create and configure equipment slot widgets."""

        for slot_data in self.game.mod.get_equipment_slots():
            gx, gy = slot_data["position"]
            r_adj, g_adj, b_adj = slot_data["color_adjust"]
            slot_bg = self._adjust_color(XcomTheme.BG_LIGHT,
                                       int(r_adj * 255),
                                       int(g_adj * 255),
                                       int(b_adj * 255))
            slot = TUnitInventorySlot(
                parent=self,
                slot_type=slot_data["type"],
                slot_name=slot_data["name"],
                size=px(GRID * 4),
                border_width=2,
                accept_types=None,  # You may want to set this based on slot_data
                bg_color=slot_bg,
                border_color=XcomTheme.BORDER_COLOR,
                hover_color="#3399ff",
                locked=False
            )
            slot.setToolTip(slot_data.get("description", f"Equipment slot for {slot_data['name']}"))
            slot.move(px(GRID * gx), px(GRID * gy))
            slot.show()
            self.equipment_slots.append(slot)

    def _setup_template_controls(self) -> None:
        """Create template combo box and template management buttons."""
        template_label = QLabel("Templates:", self)
        template_label.setFixedSize(int(px(GRID * 4)), int(px(GRID * 0.7)))
        template_label.move(int(px(GRID * 25)), int(px(GRID * 7)))
        template_label.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_SMALL))
        template_label.setStyleSheet(f"color: {XcomTheme.TEXT_BRIGHT}; background: transparent;")
        template_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        template_label.show()

        self.template_combo = QComboBox(self)
        self.template_combo.setFixedSize(int(px(GRID * 4)), int(px(GRID * 1)))
        self.template_combo.move(int(px(GRID * 25)), int(px(GRID * 7.7)))
        self.template_combo.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_SMALL))
        self.template_combo.setStyleSheet(XcomStyle.combobox())
        self.template_combo.addItem("Default")
        self.template_combo.currentTextChanged.connect(self._on_template_selected)
        self.template_combo.setToolTip("Select equipment template")
        self.template_combo.show()

        # Create save/load buttons in the middle between ARMOUR and WEAPON
        save_template_button = QPushButton("SAVE", self)
        save_template_button.setFixedSize(int(px(GRID * 2)), int(px(GRID * 1)))
        save_template_button.move(int(px(GRID * 25)), int(px(GRID * 9)))
        save_template_button.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_SMALL))
        save_template_button.setStyleSheet(XcomStyle.pushbutton(rounded=True, border_width=1))
        save_template_button.clicked.connect(self._save_template)
        save_template_button.setToolTip("Save current equipment setup as a template")
        save_template_button.show()

        self.load_template_button = QPushButton("LOAD", self)
        self.load_template_button.setFixedSize(int(px(GRID * 2)), int(px(GRID * 1)))
        self.load_template_button.move(int(px(GRID * 27)), int(px(GRID * 9)))
        self.load_template_button.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_SMALL))
        self.load_template_button.setStyleSheet(XcomStyle.pushbutton(rounded=True, border_width=1))
        self.load_template_button.clicked.connect(self._load_template)
        self.load_template_button.setEnabled(True)  # Default template is always available
        self.load_template_button.setToolTip("Load selected equipment template")
        self.load_template_button.show()

    def _setup_weight_label(self) -> None:
        """Create and configure the weight display label."""
        # Weight display label between Armour and Weapon slots
        self.weight_label = QLabel("Weight: 0", self)
        self.weight_label.setFixedSize(px(GRID * 4), px(GRID // 2))
        self.weight_label.move(px(GRID * 24), px(GRID * 6))
        self.weight_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.weight_label.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_NORMAL, QFont.Weight.Bold))
        self.weight_label.setStyleSheet(f"color: {XcomTheme.ACCENT_YELLOW}; background: transparent;")
        self.weight_label.setToolTip("Total weight of all equipped items")
        self.weight_label.show()

    def _setup_unit_avatar(self) -> None:
        """Create and configure the unit avatar label."""
        # Soldier head image - Enhanced with actual unit avatar support
        self.unit_avatar_label = QLabel(self)
        self.unit_avatar_label.setFixedSize(px(GRID * 4), px(GRID * 4))
        self.unit_avatar_label.move(px(GRID * 24), px(GRID * 1))
        self.unit_avatar_label.setStyleSheet(f"""
            QLabel {{
                background: {self._adjust_color(XcomTheme.BG_LIGHT, -int(0.05 * 255), -int(0.05 * 255), -int(0.05 * 255))};
                border: 3px solid {XcomTheme.BORDER_COLOR};
                border-radius: 4px;
            }}
        """)
        self.unit_avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.unit_avatar_label.setScaledContents(True)
        self.unit_avatar_label.setText("No Avatar")
        self.unit_avatar_label.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_SMALL))
        self.unit_avatar_label.show()

    def _setup_summary_box(self) -> None:
        """Create and configure the summary group box."""
        # Place summary groupbox
        summary_groupbox = QGroupBox("Summary", self)
        summary_groupbox.setStyleSheet(XcomStyle.groupbox())
        summary_groupbox.setFixedSize(px(GRID * 6), px(GRID * 4))
        summary_groupbox.move(px(GRID * 1), px(GRID * 1))
        summary_groupbox.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        summary_groupbox.setToolTip("Base personnel summary")

        # Add summary content with left-top alignment and monospace font for table formatting
        summary_layout = QVBoxLayout(summary_groupbox)
        summary_layout.setContentsMargins(px(1), px(3), px(1), px(1))
        summary_layout.setSpacing(0)
        summary_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.summary_label = QLabel("Units:     0\nTanks:     0\nPets:      0\nAliens:    0\nCapacity: 50", summary_groupbox)
        self.summary_label.setFont(QFont("Courier", XcomTheme.FONT_SIZE_SMALL))  # Monospace font for alignment
        self.summary_label.setStyleSheet(f"color: {XcomTheme.TEXT_BRIGHT}; background: transparent;")
        self.summary_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        summary_layout.addWidget(self.summary_label)

        summary_groupbox.show()

    def _setup_unit_list(self) -> None:
        """Create and configure the unit list widget and filter."""
        # Unit list widget
        unit_list_groupbox = QGroupBox("", self)
        unit_list_groupbox.setStyleSheet(XcomStyle.groupbox())
        unit_list_groupbox.setFixedSize(int(px(GRID * 6)), int(px(GRID * 14)))
        unit_list_groupbox.move(int(px(GRID * 1)), int(px(GRID * 6)))
        unit_list_groupbox.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        unit_list_groupbox.setContentsMargins(int(px(0.5)), int(px(0.5)), 0, 0)

        unit_list_layout = QVBoxLayout(unit_list_groupbox)
        unit_list_layout.setContentsMargins(int(px(0.5)), int(px(0.5)), 0, 0)
        unit_list_layout.setSpacing(int(px(0.5)))

        unit_filter_combo = QComboBox(unit_list_groupbox)
        unit_filter_combo.clear()
        for unit_category in self.game.mod.get_unit_categories():
            unit_image = self.game.mod.tileset_manager.get_tile(unit_category["icon"])
            unit_filter_combo.addItem(unit_image, unit_category["name"])
        unit_filter_combo.setStyleSheet(XcomStyle.combobox())
        unit_filter_combo.setToolTip("Filter units by type")
        unit_list_layout.addWidget(unit_filter_combo)

        self.unit_list_widget = UnitListWidget(unit_list_groupbox)

        # Load initial units
        for name, unit in self.game.get_current_base_units():
            unit_type = unit.unit_type
            unit_icon = self.game.mod.tileset_manager.get_tile(unit_type)
            item = QListWidgetItem(QIcon(unit_icon), name)
            self.unit_list_widget.addUnitWithInfo(item, unit)
        self.unit_list_widget.setStyleSheet(XcomStyle.listwidget())

        # Connect unit selection signal
        self.unit_list_widget.unitSelected.connect(self._on_unit_selected)

        # Connect filter combo to filtering function
        unit_filter_combo.currentTextChanged.connect(self.unit_list_widget.filter_units)

        unit_list_layout.addWidget(self.unit_list_widget)
        unit_list_groupbox.show()

    def _setup_item_list(self) -> None:
        """Create and configure the item list widget and filter."""
        # Item list widget
        item_list = QGroupBox("", self)
        item_list.setStyleSheet(XcomStyle.groupbox())
        item_list.setFixedSize(int(px(GRID * 6)), int(px(GRID * 21)))
        item_list.move(int(px(GRID * 33)), int(px(GRID * 1)))
        item_list.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        item_list.setContentsMargins(int(px(0.5)), int(px(0.5)), 0, 0)

        item_list_layout = QVBoxLayout(item_list)
        item_list_layout.setContentsMargins(int(px(0.5)), int(px(0.5)), 0, 0)
        item_list_layout.setSpacing(int(px(0.5)))

        item_filter_combo = QComboBox(item_list)
        item_filter_combo.clear()
        for category in self.game.mod.get_item_categories():
            category_icon = self.game.mod.tileset_manager.get_tile(category["icon"])
            item_filter_combo.addItem(QIcon(category_icon), category["name"])
        item_filter_combo.setStyleSheet(XcomStyle.combobox())
        item_list_layout.addWidget(item_filter_combo)

        self.item_list_widget = ItemListWidget(item_list)

        # Initialize with current base items
        for name, item_data in self.game.get_current_base_items():
            item_type = item_data.item_type
            item_icon = self.game.mod.tileset_manager.get_tile(item_type)
            count = item_data.quantity if hasattr(item_data, 'quantity') else 1
            item = QListWidgetItem(QIcon(item_icon), f"{name} ({count})")
            self.item_list_widget.addItemWithInfo(item, item_data, count)
        self.item_list_widget.setStyleSheet(XcomStyle.listwidget())

        # Connect filter combo to filtering function
        item_filter_combo.currentTextChanged.connect(self.item_list_widget.filter_items)

        item_list_layout.addWidget(self.item_list_widget)
        item_list.show()

    def _setup_stats_box(self) -> None:
        """Create and configure the stats group box with progress bars."""
        # Stats groupbox - ENHANCED with progress bars
        unit_stats_groupbox = QGroupBox("Stats", self)
        unit_stats_groupbox.setStyleSheet(XcomStyle.groupbox())
        unit_stats_groupbox.setFixedSize(px(GRID * 11), px(GRID * 8))
        unit_stats_groupbox.move(px(GRID * 8), px(GRID * 6))
        unit_stats_groupbox.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        unit_stats_groupbox.setContentsMargins(px(0.5), px(0.5), 0, 0)

        # Create scrollable stats area
        stats_scroll = QScrollArea(unit_stats_groupbox)
        stats_scroll.setWidgetResizable(True)
        stats_scroll.setStyleSheet("background: transparent; border: none;")
        stats_scroll.setFixedSize(px(GRID * 10.5), px(GRID * 7))
        stats_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        stats_content = QWidget()
        stats_layout = QVBoxLayout(stats_content)
        stats_layout.setContentsMargins(px(0.5), px(0.5), px(0.5), px(0.5))
        stats_layout.setSpacing(px(0.5))
        stats_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Create attribute progress bars
        self.stat_bars = {}
        stat_attributes = ["health", "stamina", "strength", "reactions", "accuracy", "throwing"]

        for attr in stat_attributes:
            attr_layout = QHBoxLayout()
            attr_layout.setContentsMargins(0, 0, 0, 0)
            attr_layout.setSpacing(px(0.5))

            attr_label = QLabel(attr.capitalize())
            attr_label.setFixedWidth(px(GRID * 3))
            attr_label.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_SMALL))
            attr_label.setStyleSheet(f"color: {XcomTheme.TEXT_BRIGHT}; background: transparent;")

            attr_bar = QProgressBar()
            attr_bar.setRange(0, 100)
            attr_bar.setValue(0)  # Default value
            attr_bar.setTextVisible(True)
            attr_bar.setFixedHeight(px(GRID * 0.6))
            attr_bar.setStyleSheet(f"""
                QProgressBar {{
                    background: {XcomTheme.BG_DARK};
                    border: 1px solid {XcomTheme.BORDER_COLOR};
                    border-radius: 2px;
                    text-align: center;
                }}
                QProgressBar::chunk {{
                    background: {XcomTheme.ACCENT_BLUE};
                }}
            """)

            attr_layout.addWidget(attr_label)
            attr_layout.addWidget(attr_bar)
            stats_layout.addLayout(attr_layout)

            # Store reference to the progress bar
            self.stat_bars[attr] = attr_bar

        stats_scroll.setWidget(stats_content)
        unit_stats_groupbox.show()

    def _setup_traits_box(self) -> None:
        """Create and configure the traits group box with scroll area."""
        # Traits groupbox - ENHANCED with scrollable trait list
        traits_groupbox = QGroupBox("Traits", self)
        traits_groupbox.setStyleSheet(XcomStyle.groupbox())
        traits_groupbox.setFixedSize(px(GRID * 11), px(GRID * 8))
        traits_groupbox.move(px(GRID * 8), px(GRID * 14))
        traits_groupbox.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        traits_groupbox.setContentsMargins(px(0.5), px(0.5), 0, 0)

        # Create scrollable traits area
        traits_scroll = QScrollArea(traits_groupbox)
        traits_scroll.setWidgetResizable(True)
        traits_scroll.setStyleSheet("background: transparent; border: none;")
        traits_scroll.setFixedSize(px(GRID * 10.5), px(GRID * 7))
        traits_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        traits_content = QWidget()
        traits_layout = QVBoxLayout(traits_content)
        traits_layout.setContentsMargins(px(0.5), px(0.5), px(0.5), px(0.5))
        traits_layout.setSpacing(px(0.5))
        traits_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # This will be populated dynamically based on the selected unit
        self.traits_layout = traits_layout
        traits_scroll.setWidget(traits_content)
        traits_groupbox.show()

    def _setup_fire_button(self) -> None:
        """Create and configure the fire button."""
        # Fire button
        fire_button = QPushButton("Fire", self)
        fire_button.setFixedSize(px(GRID * 2 - 2), px(GRID - 2))
        fire_button.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_NORMAL))
        fire_button.move(px(GRID * 3), px(GRID * 21))
        fire_button.show()

    def _setup_basic_info_box(self) -> None:
        """Create and configure the basic info group box."""
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
        self.unit_info_label.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_NORMAL, QFont.Weight.Bold))
        self.unit_info_label.setStyleSheet(f"color: {XcomTheme.ACCENT_BLUE}; background: transparent;")
        self.unit_info_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        basic_info_layout.addWidget(self.unit_info_label)

        basic_info_groupbox.show()

    def _finalize_ui_setup(self) -> None:
        """
        Finalize UI setup: initialize equipment slot states, update summary, set globals, and auto-select first unit.
        """
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
        units = self.game.get_current_base_units()
        if units and len(units) > 0:
            self.unit_list_widget.setCurrentRow(0)
            first_unit_name = units[0][0]
            self._on_unit_selected(first_unit_name)

    def screen_activated(self):
        """Called when this screen becomes active."""
        # Refresh data when screen becomes active
        self.refresh_base_data()

    def screen_deactivated(self):
        """
        Called when another screen becomes active.
        This method can be used to perform cleanup or save state if needed
        when the barracks screen is no longer the active view.
        """
        pass

    def refresh_base_data(self):
        """
        Refresh unit and item lists for the current active base.

        This method resets the current unit selection, clears all equipment slots,
        and reloads all units and items from the game data. It should be called
        whenever the active base changes or when inventory items are modified outside
        of the barracks screen.
        """
        # Reset current unit
        self.current_unit = None
        self.unit_info_label.setText("No unit selected")

        # Clear equipment slots
        for slot in self.equipment_slots:
            if slot.item:
                slot.remove_item()

        # Load new base data
        units = self.game.get_current_base_units()
        items = self.game.get_current_base_items()

        # Populate unit list
        if self.unit_list_widget:
            self.unit_list_widget.clear()  # Clear before adding new items
            for name, unit in units:
                unit_type = unit.unit_type
                unit_icon = self.game.mod.tileset_manager.get_tile(unit_type)
                item = QListWidgetItem(QIcon(unit_icon), name)
                self.unit_list_widget.addUnitWithInfo(item, unit)

            # Auto-select first unit if any units exist
            if units and len(units) > 0:
                self.unit_list_widget.setCurrentRow(0)
                first_unit_name = units[0][0]
                self._on_unit_selected(first_unit_name)

        # Populate item list
        if self.item_list_widget:
            self.item_list_widget.clear()  # Clear before adding new items
            for name, item_data in items:
                item_type = item_data.item_type
                item_icon = self.game.mod.tileset_manager.get_tile(item_type)
                count = item_data.quantity if hasattr(item_data, 'quantity') else 1
                item = QListWidgetItem(QIcon(item_icon), f"{name} ({count})")
                self.item_list_widget.addItemWithInfo(item, item_data, count)

        # Update summary
        self.update_summary_display()

    def update_summary_display(self):
        """
        Update summary statistics with formatted table display.

        Retrieves the latest base statistics from the game and updates
        the summary label with a formatted table showing soldier counts
        by type and base capacity information.
        """
        if self.summary_label:
            stats = self.game.get_base_summary()
            # Format as table with aligned columns
            summary_text = f"Units:    {stats['soldiers']:2d}\nTanks:    {stats['tanks']:2d}\nDogs:     {stats['dogs']:2d}\nAliens:   {stats['aliens']:2d}\nCapacity: {stats['capacity']:2d}"
            self.summary_label.setText(summary_text)

    def _update_weight_display(self):
        """
        Update the weight display label with total equipment weight.

        Calculates the total weight of all equipped items across all
        equipment slots and updates the weight display label accordingly.
        This should be called whenever items are added or removed from
        equipment slots.
        """
        if not self.weight_label or not self.equipment_slots:
            return

        total_weight: int = 0
        for slot in self.equipment_slots:
            if slot.item:
                total_weight += slot.item.weight

        self.weight_label.setText(f"Weight: {total_weight}")

    def _update_equipment_slot_states(self, enabled_count: int):
        """
        Enable or disable equipment slots based on armor configuration.

        Args:
            enabled_count: Number of equipment slots to enable

        Enables the specified number of equipment slots and disables the rest.
        Disabled slots will have their items returned to inventory and will
        be shown with a gray border to indicate they are unavailable.
        This is typically called when armor is changed, as different armor
        types allow different numbers of equipment slots.
        """
        if not self.equipment_slots:
            return

        equipment_slots = [slot for slot in self.equipment_slots if slot.slot_type == TItemType.ITEM_UNIT_EQUIPMENT]

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
        """
        Handle unit selection from the list.

        Args:
            unit_name: The name of the unit selected by the user

        Updates the UI to display the selected unit's information, stats, traits,
        and avatar. Also validates equipment slots and updates related widgets.
        """
        self.current_unit = unit_name

        # Get unit data for detailed display
        unit = self.game.get_unit_by_name(unit_name)
        if unit:
            # Store selected unit data for other methods to access
            self.selected_unit_data = unit

            # Update unit info with comprehensive details
            combat_effectiveness = self._calculate_combat_effectiveness(unit)
            unit_type = unit.unit_type.capitalize() if hasattr(unit, 'unit_type') else "Unknown"
            experience = unit.experience if hasattr(unit, 'experience') else 0
            rank = unit.rank if hasattr(unit, 'rank') else "Rookie"

            unit_info_text = f"Unit: {unit_name}\n"
            unit_info_text += f"Type: {unit_type}\n"
            unit_info_text += f"Rank: {rank}\n"
            unit_info_text += f"XP: {experience}\n"
            unit_info_text += f"Combat Rating: {combat_effectiveness:.1f}%"

            self.unit_info_label.setText(unit_info_text)
        else:
            self.unit_info_label.setText(f"Unit: {unit_name}")
            self.selected_unit_data = None

        # Validate equipment slots after unit selection
        # FIXME validate_and_update_equipment_slots()

        # Update unit stats and traits display
        self._update_unit_stats(unit_name)
        self._update_unit_traits(unit_name)

        # Display unit avatar
        self._display_unit_avatar(unit_name)

    def _calculate_combat_effectiveness(self, unit: TUnit) -> float:
        """
        Calculate combat effectiveness rating for the unit.

        Args:
            unit: Unit object to calculate effectiveness for

        Returns:
            Combat effectiveness rating as a percentage (0-100)
        """
        if not unit:
            return 0.0

        # Base effectiveness is average of primary stats
        base_stats = ["health", "stamina", "strength", "reactions", "accuracy"]
        base_values = []

        for stat in base_stats:
            if hasattr(unit, stat):
                base_values.append(getattr(unit, stat))

        if not base_values:  # No valid stats found
            return 0.0

        base_effectiveness = sum(base_values) / len(base_values)

        # Apply equipment bonuses
        equipment_bonus = 0.0
        if hasattr(unit, 'inventory'):
            # Count weapons and armor
            has_weapon = any(getattr(item, 'item_type', None) == getattr(TItemType, 'ITEM_WEAPON', None) for item in unit.inventory)
            has_armor = any(getattr(item, 'item_type', None) == getattr(TItemType, 'ITEM_ARMOR', None) for item in unit.inventory)

            if has_weapon:
                equipment_bonus += 15.0
            if has_armor:
                equipment_bonus += 10.0

        # Apply experience multiplier (0.8 - 1.2 based on XP)
        exp_multiplier = 0.8
        if hasattr(unit, 'experience'):
            exp_multiplier += min(0.4, unit.experience / 100.0)

        # Apply traits bonuses/penalties
        trait_modifier = 0.0
        if hasattr(unit, 'traits'):
            positive_traits = ["brave", "strong", "accurate", "genius", "fast"]
            negative_traits = ["weak", "slow", "coward", "clumsy", "imprecise"]

            for trait in unit.traits:
                trait_str = str(trait)
                if trait_str.lower() in positive_traits:
                    trait_modifier += 5.0
                elif trait_str.lower() in negative_traits:
                    trait_modifier -= 5.0

        # Calculate final effectiveness
        effectiveness = (base_effectiveness + equipment_bonus + trait_modifier) * exp_multiplier

        # Clamp to valid range (0-100)
        return max(0.0, min(100.0, effectiveness))

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
        template_name = self.current_template_name if self.current_template_name else "Default"
        self.saved_templates[template_name] = InventoryTemplate(template_name, equipment_data)

        # Update template combo box
        if self.template_combo:
            self.template_combo.addItem(template_name)
            self.template_combo.setCurrentText(template_name)

        # Enable load button
        if self.load_template_button:
            self.load_template_button.setEnabled(True)

        print(f"Template '{template_name}' saved to memory")

    def _load_template(self):
        """Load template from memory."""
        if not self.current_template_name or not self.saved_templates or not self.equipment_slots:
            print("No template available or no equipment slots")
            return

        # Clear current equipment and return to inventory
        for slot in self.equipment_slots:
            if slot.item:
                item = slot.remove_item()
                if item and self.item_list_widget:
                    self.item_list_widget.add_item_to_inventory(item, 1)

        # Load template equipment
        template = self.saved_templates.get(self.current_template_name)
        if template and template.equipment_data:
            for slot in self.equipment_slots:
                slot_key = slot.slot_name
                if slot_key in template.equipment_data and template.equipment_data[slot_key]:
                    try:
                        item = TItem.from_dict(template.equipment_data[slot_key], getattr(self.game.mod, 'item_types', {}))
                        slot.add_item(item)
                        # Remove from inventory if it exists
                        if self.item_list_widget:
                            self.item_list_widget.remove_item_from_inventory(item.name, 1)
                    except Exception as e:
                        print(f"Error loading item for slot {slot_key}: {e}")

        # After loading template, validate equipment slots based on loaded armor
        # FIXME validate_and_update_equipment_slots()

        print(f"Template '{self.current_template_name}' loaded from memory")

    def _new_template(self):
        """Create a new empty template."""
        new_template_name = "New Template"
        base_name = new_template_name
        counter = 1

        # Find a unique name for the new template
        while new_template_name in self.saved_templates:
            new_template_name = f"{base_name} ({counter})"
            counter += 1

        # Create an empty template and save it
        self.saved_templates[new_template_name] = InventoryTemplate(new_template_name, {})
        self.template_combo.addItem(new_template_name)
        self.template_combo.setCurrentText(new_template_name)

        print(f"New template created: {new_template_name}")

    def _rename_template(self):
        """Rename the currently selected template."""
        if not self.current_template_name or not self.saved_templates:
            return

        new_name, ok = QInputDialog.getText(self, "Rename Template", "Enter new template name:", text=self.current_template_name)
        if ok and new_name and new_name != self.current_template_name:
            # Ensure the new name is unique
            if new_name in self.saved_templates:
                # Use a dummy QRect for QToolTip.showText as required by PySide6
                from PySide6.QtCore import QRect
                QToolTip.showText(QCursor.pos(), "Template name already exists", self, QRect(0,0,1,1), 3000)
                return

            # Rename the template
            template = self.saved_templates.pop(self.current_template_name)
            template.name = new_name
            self.saved_templates[new_name] = template

            # Update template combo box
            index = self.template_combo.findText(self.current_template_name)
            if index != -1:
                self.template_combo.setItemText(index, new_name)

            self.current_template_name = new_name

            print(f"Template renamed to: {new_name}")

    def _delete_template(self):
        """Delete the currently selected template."""
        if not self.current_template_name or not self.saved_templates:
            return

        # Confirm deletion
        from PySide6.QtWidgets import QMessageBox
        reply = QMessageBox.question(self, "Delete Template",
                                     f"Are you sure you want to delete the template '{self.current_template_name}'?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            # Delete the template
            del self.saved_templates[self.current_template_name]

            # Update template combo box
            self.template_combo.removeItem(self.template_combo.currentIndex())
            self.template_combo.setCurrentIndex(0)

            # Load default template if available
            if "Default" in self.saved_templates:
                self.current_template_name = "Default"
                default_template = self.saved_templates["Default"]
                for slot in self.equipment_slots:
                    slot_key = slot.slot_name
                    if slot_key in default_template.equipment_data and default_template.equipment_data[slot_key]:
                        try:
                            item = TItem.from_dict(default_template.equipment_data[slot_key], getattr(self.game.mod, 'item_types', {}))
                            slot.add_item(item)
                        except Exception as e:
                            print(f"Error loading default item for slot {slot_key}: {e}")

            print(f"Template '{self.current_template_name}' deleted")

    def _on_template_selected(self, template_name: str):
        """Handle template selection from the combo box."""
        self.current_template_name = template_name

        # Load the selected template if it exists
        if template_name in self.saved_templates:
            template = self.saved_templates[template_name]
            for slot in self.equipment_slots:
                slot_key = slot.slot_name
                if slot_key in template.equipment_data and template.equipment_data[slot_key]:
                    try:
                        item = TItem.from_dict(template.equipment_data[slot_key], getattr(self.game.mod, 'item_types', {}))
                        slot.add_item(item)
                    except Exception as e:
                        print(f"Error loading item for slot {slot_key}: {e}")

    def _test_equipment_slots(self):
        """
        Test function for equipment slot validation.
        This is a developer utility to verify that equipment slot logic is working as intended.
        """
        import engine


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
        c = QColor(hex_color)
        c = QColor(min(255, max(0, c.red() + r)),
                  min(255, max(0, c.green() + g)),
                  min(255, max(0, c.blue() + b)))
        return c.name()

    def _update_unit_stats(self, unit_name: str):
        """
        Update the displayed stats for the selected unit.

        Args:
            unit_name: The name of the unit whose stats are to be displayed

        Retrieves the stats of the specified unit and updates the progress bars
        in the stats groupbox to reflect the current values.
        """
        unit = self.game.get_unit_by_name(unit_name)
        if not unit or not self.stat_bars:
            return

        # Update each stat progress bar with the unit's current stat value
        for stat, bar in self.stat_bars.items():
            if hasattr(unit, stat):
                value = getattr(unit, stat)
                bar.setValue(value)

    def _update_unit_traits(self, unit_name: str):
        """
        Update the displayed traits for the selected unit.

        Args:
            unit_name: The name of the unit whose traits are to be displayed

        Populates the traits groupbox with the traits of the specified unit.
        Each trait is displayed as a separate label in the traits list.
        """
        unit = self.game.get_unit_by_name(unit_name)
        if not unit or not self.traits_layout:
            return

        # Clear existing traits
        for i in reversed(range(self.traits_layout.count())):
            self.traits_layout.itemAt(i).widget().deleteLater()

        # Add each trait as a label
        for trait in unit.traits:
            trait_label = QLabel(f"- {trait}", self)
            trait_label.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_SMALL))
            trait_label.setStyleSheet(f"color: {XcomTheme.TEXT_BRIGHT}; background: transparent;")
            self.traits_layout.addWidget(trait_label)

        # Adjust size of traits groupbox to fit content
        self.traits_layout.parentWidget().adjustSize()

    def _on_equipment_changed(self, slot_name: str, item_name: str):
        """
        Slot for handling equipment changes.

        This slot is called whenever an equipment change occurs, either
        through direct user action or programmatic changes. It ensures that
        the UI components are updated to reflect the current equipment state.

        Args:
            slot_name: The name of the equipment slot that was changed
            item_name: The name of the item that was equipped or unequipped
        """
        print(f"Equipment changed - Slot: {slot_name}, Item: {item_name}")
        # Refresh item list and update summary
        self.item_list_widget.refresh_items()
        self.update_summary_display()

    def _update_unit_equipment_status(self, unit_name: str):
        """
        Update the equipment status of the specified unit.

        This method is called when a unit is equipped or unequipped to
        update the internal state and UI components accordingly.

        Args:
            unit_name (str): The name of the unit whose equipment status is to be updated.
        """
        unit = self.game.get_unit_by_name(unit_name)
        if not unit:
            return

        # Update equipment slots based on unit's current equipment
        for slot in self.equipment_slots:
            if slot.slot_type == TItemType.ITEM_UNIT_EQUIPMENT:
                # Find corresponding equipment item
                item = next((i for i in unit.inventory if i.equipment_slot == slot.slot_name), None)
                if item:
                    slot.add_item(item)
                else:
                    slot.remove_item()

        # Update weight display
        self._update_weight_display()

        # Refresh item list to show updated inventory
        self.item_list_widget.refresh_items()

        # Update summary to reflect current unit status
        self.update_summary_display()

    def _display_unit_avatar(self, unit_name: str):
        """
        Display the avatar of the selected unit.

        Args:
            unit_name (str): The name of the unit whose avatar is to be displayed.

        This method sets the pixmap of the unit avatar label to the avatar of the selected unit.
        If the unit has no avatar, a default "No Avatar" text is shown.
        """
        unit = self.game.get_unit_by_name(unit_name)
        if not unit or not self.unit_avatar_label:
            return

        # Get avatar image path from unit data
        avatar_path = unit.avatar_path if unit.avatar_path and os.path.exists(unit.avatar_path) else None

        if avatar_path:
            # Load and set the avatar pixmap
            pixmap = QPixmap(avatar_path)
            self.unit_avatar_label.setPixmap(pixmap)
            self.unit_avatar_label.setText("")  # Clear text if image is set
        else:
            # Set default text if no avatar image is available
            self.unit_avatar_label.setPixmap(QPixmap())  # Clear pixmap
            self.unit_avatar_label.setText("No Avatar")

        # Adjust size of the avatar label to fit the image
        self.unit_avatar_label.adjustSize()


# Custom widget classes
class UnitListWidget(QListWidget):
    """
    Custom QListWidget for displaying the list of units in the barracks.

    Provides unit selection, filtering by category, and stores unit data.
    """
    # Signal emitted when a unit is selected
    unitSelected = Signal(str)

    def __init__(self, parent=None):
        """Initialize the unit list widget."""
        super().__init__(parent)
        # Storage for unit info by name
        self.unit_info = {}
        # Full list of all units for filtering
        self.all_units = []
        self.current_filter = "All"

        # Configure widget appearance and behavior
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Connect selection change signal
        self.itemSelectionChanged.connect(self._on_selection_changed)

    def addUnitWithInfo(self, item, unit_data):
        """Add a unit item with associated data to the list."""
        unit_name = item.text()

        # Store for filtering
        self.all_units.append({
            'name': unit_name,
            'icon': item.icon(),
            'unit_type': unit_data.unit_type if hasattr(unit_data, 'unit_type') else "Unknown",
            'unit': unit_data
        })

        # Add to the visible list
        self.addItem(item)
        self.unit_info[unit_name] = unit_data

    def filter_units(self, category):
        """Filter units by category."""
        self.current_filter = category
        self.clear()

        for unit in self.all_units:
            # Show all units or only those matching the filter
            if category == "All" or unit['unit_type'].lower() == category.lower():
                item = QListWidgetItem(unit['icon'], unit['name'])
                self.addItem(item)

    def _on_selection_changed(self):
        """Handle selection changes and emit unitSelected signal."""
        selected_items = self.selectedItems()
        if selected_items:
            unit_name = selected_items[0].text()
            self.unitSelected.emit(unit_name)

    def get_unit_data(self, unit_name):
        """Get stored unit data for the given name."""
        return self.unit_info.get(unit_name)


class ItemListWidget(QListWidget):
    """
    Custom QListWidget for displaying the list of items available for equipment.

    Provides item filtering by category and maintains item quantities.
    """
    def __init__(self, parent=None):
        """Initialize the item list widget."""
        super().__init__(parent)
        # Storage for item info by name
        self.item_info = {}
        # Track quantities for each item
        self.item_quantities = {}
        # Full list of all items for filtering
        self.all_items = []
        self.current_filter = "All"

        # Configure widget appearance and behavior
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def addItemWithInfo(self, item, item_data, quantity=1):
        """Add an item with its data and quantity to the list."""
        item_name = item_data.name

        # Store for filtering
        self.all_items.append({
            'name': item_name,
            'icon': item.icon(),
            'item_type': item_data.item_type if hasattr(item_data, 'item_type') else "Unknown",
            'item': item_data
        })

        # Track item quantity
        self.item_quantities[item_name] = quantity

        # Add to the visible list
        self.addItem(item)
        self.item_info[item_name] = item_data

    def filter_items(self, category):
        """Filter items by category."""
        self.current_filter = category
        self.clear()

        for item in self.all_items:
            # Skip items with quantity 0
            if self.item_quantities.get(item['name'], 0) <= 0:
                continue

            # Show all items or only those matching the filter
            if category == "All" or item['item_type'].lower() == category.lower():
                quantity = self.item_quantities.get(item['name'], 0)
                list_item = QListWidgetItem(item['icon'], f"{item['name']} ({quantity})")
                self.addItem(list_item)

    def add_item_to_inventory(self, item, quantity=1):
        """Add an item (or increase quantity) in the inventory."""
        item_name = item.name

        # Update or create quantity entry
        current_quantity = self.item_quantities.get(item_name, 0)
        self.item_quantities[item_name] = current_quantity + quantity

        # Update or add to the item_info dict
        if item_name not in self.item_info:
            self.item_info[item_name] = item

            # Add to all_items if it doesn't exist
            found = False
            for existing in self.all_items:
                if existing['name'] == item_name:
                    found = True
                    break

            if not found:
                self.all_items.append({
                    'name': item_name,
                    'icon': QIcon(self.game.mod.tileset_manager.get_tile(item.item_type)),
                    'item_type': item.item_type,
                    'item': item
                })

        # Refresh the view
        self.refresh_items()

    def remove_item_from_inventory(self, item_name, quantity=1):
        """Remove an item (or decrease quantity) from the inventory."""
        if item_name in self.item_quantities:
            # Update quantity
            current_quantity = self.item_quantities[item_name]
            new_quantity = max(0, current_quantity - quantity)
            self.item_quantities[item_name] = new_quantity

            # Refresh the view
            self.refresh_items()

            return True
        return False

    def refresh_items(self):
        """Refresh the item list using the current filter."""
        self.filter_items(self.current_filter)
