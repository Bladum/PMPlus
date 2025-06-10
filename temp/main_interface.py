"""
Main Interface Module for XCOM Inventory System

This module contains the main UI creation and management functions for the XCOM-style
inventory interface. It handles global state management, equipment templates, and
coordinates between different UI components.

Key Features:
- Global state management for equipment and units
- Template system for saving/loading equipment setups
- Base switching functionality
- Screen management (Barracks, Manufacturing, etc.)
"""

import json
import os
from typing import Optional, Dict, Any, List
from PySide6.QtCore import Qt, QTimer, QPoint, QMimeData, QByteArray, QRect
from PySide6.QtGui import (QFont, QIcon, QPixmap, QColor, QPainter, QDrag, QCursor, 
                          QDragEnterEvent, QDropEvent, QMouseEvent, QPen, QBrush)
from PySide6.QtWidgets import (QVBoxLayout, QToolTip, QListWidget, QListWidgetItem, 
                              QAbstractItemView, QLabel, QGroupBox, QMessageBox, 
                              QWidget, QApplication, QHBoxLayout, QGridLayout, 
                              QPushButton, QFrame, QButtonGroup, QComboBox, QInputDialog)

from theme_styles import XcomTheme, XcomStyle, GRID, px, SCALED_WIDTH, SCALED_HEIGHT
from game_data import GameData, ItemType, UnitCategory
from inventory_system import (InventoryItem, ItemType, ItemRarity, UnitInventoryManager, 
                             TemplateManager, InventoryTemplate)
from top_panel_widget import TopPanelWidget

# Global state management - Module-level globals for proper access
current_screen: str = "BARRACKS"  # Default screen
unit_inventory_manager: UnitInventoryManager = UnitInventoryManager()
basic_info_label_global: Optional[QLabel] = None
summary_label_global: Optional[QLabel] = None
top_panel_widget_global: Optional[TopPanelWidget] = None

# Equipment and UI globals - set by create_main_interface()
equipment_slots_global: List[Any] = []  # List of EquipmentSlotWidget instances
item_list_widget_global: Optional[Any] = None  # ItemListWidget instance
weight_label_global: Optional[QLabel] = None
unit_info_label_global: Optional[QLabel] = None
current_unit_global: Optional[str] = None

# Template system globals - simple in-memory template storage
saved_template: Optional[InventoryTemplate] = None
load_template_button_global: Optional[QPushButton] = None

def save_template() -> None:
    """Save current equipment setup as template in memory."""
    global equipment_slots_global, saved_template, load_template_button_global
    
    if not equipment_slots_global:
        print("No equipment slots available for saving template")
        return
    
    # Create equipment data dictionary
    equipment_data = {}
    for slot in equipment_slots_global:
        slot_key = slot.slot_name
        if slot.item:
            equipment_data[slot_key] = slot.item.to_dict()
        else:
            equipment_data[slot_key] = None
    
    # Save template in memory
    saved_template = InventoryTemplate("Memory Template", equipment_data)
    
    # Enable load button
    if load_template_button_global:
        load_template_button_global.setEnabled(True)
    
    print("Template saved to memory")

def load_template() -> None:
    """Load template from memory."""
    global saved_template, equipment_slots_global, item_list_widget_global
    
    if not saved_template or not equipment_slots_global:
        print("No template available or no equipment slots")
        return
    
    # Clear current equipment and return to inventory
    for slot in equipment_slots_global:
        if slot.item:
            item = slot.remove_item()
            if item and item_list_widget_global:
                item_list_widget_global.add_item_to_inventory(item, 1)
    
    # Load template equipment
    for slot in equipment_slots_global:
        slot_key = slot.slot_name
        if slot_key in saved_template.equipment_data and saved_template.equipment_data[slot_key]:
            try:
                item = InventoryItem.from_dict(saved_template.equipment_data[slot_key])
                slot.add_item(item)
                # Remove from inventory if it exists
                if item_list_widget_global:
                    item_list_widget_global.remove_item_from_inventory(item.name, 1)
            except Exception as e:
                print(f"Error loading item for slot {slot_key}: {e}")
    
    # After loading template, validate equipment slots based on loaded armor
    from engine.gui.widgets import validate_and_update_equipment_slots
    validate_and_update_equipment_slots()
    
    print("Template loaded from memory")
    if load_template_button_global:
        load_template_button_global.setEnabled(True)
        load_template_button_global.setStyleSheet(XcomStyle.pushbutton(rounded=True, border_width=1))
# TEMPLATE SYSTEM END

def update_weight_display() -> None:
    """
    Update the weight display label with total equipment weight.
    
    Calculates the total weight of all equipped items and updates the
    weight display label. Returns early if required widgets are not available.
    """
    global equipment_slots_global, weight_label_global

    if not weight_label_global or not equipment_slots_global:
        return

    total_weight: int = 0
    for slot in equipment_slots_global:
        if slot.item:
            total_weight += slot.item.weight

    weight_label_global.setText(f"Weight: {total_weight}")

def update_equipment_slot_states(enabled_count: int) -> None:
    """
    Enable or disable equipment slots based on armor configuration.
    
    Args:
        enabled_count: Number of equipment slots to enable (based on armor type)
        
    Disables excess slots and moves any equipped items back to inventory.
    Updates visual appearance to reflect enabled/disabled state.
    """
    global equipment_slots_global, item_list_widget_global

    if not equipment_slots_global:
        return

    equipment_slots = [slot for slot in equipment_slots_global if slot.slot_type == ItemType.EQUIPMENT]

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
            if slot.item and item_list_widget_global:
                item = slot.remove_item()
                item_list_widget_global.add_item_to_inventory(item, 1)

            # Set gray appearance
            slot.set_border_color(XcomTheme.TEXT_DIM)
            slot._original_border_color = XcomTheme.TEXT_DIM

        slot.update()

def switch_screen(screen_name: str) -> None:
    """
    Handle screen switching with debug output.
    
    Args:
        screen_name: The name of the screen to switch to
        
    Updates the global current screen state and provides debug feedback.
    """
    global current_screen
    current_screen = screen_name
    print(f"Switched to screen: {screen_name}")

def switch_base(base_index: int) -> bool:
    """
    Handle base switching with data refresh.
    
    Args:
        base_index: Zero-based index of the base to switch to
        
    Returns:
        True if base switch was successful, False otherwise
        
    Updates the active base, refreshes display and reloads base-specific data.
    """
    if GameData.set_active_base(base_index):
        update_base_display()
        refresh_base_data()
        print(f"Switched to base: {GameData.BASES[base_index].name}")
        return True
    return False

def refresh_base_data() -> None:
    """
    Refresh unit and item lists for the current active base.
    
    Clears all current data (units, items, equipment) and reloads
    data specific to the currently active base. Updates UI displays
    to reflect the new base information.
    """
    global item_list_widget_global, current_unit_global

    # Reset current unit
    current_unit_global = None
    if unit_info_label_global:
        unit_info_label_global.setText("No unit selected")
    
    # Clear equipment slots
    if equipment_slots_global:
        for slot in equipment_slots_global:
            if slot.item:
                slot.remove_item()
    
    # Load new base data
    units = GameData.get_current_base_units()
    items = GameData.get_current_base_items()
    
    # Populate unit list
    if hasattr(refresh_base_data, 'unit_list_widget') and refresh_base_data.unit_list_widget:
        refresh_base_data.unit_list_widget.clear()  # Clear before adding new items
        for name, icon_path, info in units:
            item = QListWidgetItem(QIcon(QPixmap(icon_path).scaled(32, 32)), name)
            refresh_base_data.unit_list_widget.addUnitWithInfo(item, info)
        
        # Auto-select first unit if any units exist
        if units and len(units) > 0:
            refresh_base_data.unit_list_widget.setCurrentRow(0)
            first_unit_name = units[0][0]
            refresh_base_data.unit_list_widget.unit_selected(first_unit_name)
            
            # Validate equipment slots after unit selection
            from engine.gui.widgets import validate_and_update_equipment_slots
            validate_and_update_equipment_slots()
    
    # Populate item list
    if item_list_widget_global:
        item_list_widget_global.clear()  # Clear before adding new items
        for name, icon_path, info, count in items:
            item = QListWidgetItem(QIcon(QPixmap(icon_path).scaled(32, 32, Qt.KeepAspectRatio, Qt.FastTransformation)),
                                   f"{name} ({count})")
            item_list_widget_global.addItemWithInfo(item, info, count)
    
    # Update summary
    update_summary_display()

def update_base_display() -> None:
    """
    Update base name label and button colors for the current active base.
    
    Updates the basic info label to show the current active base name.
    Should be called whenever the active base changes.
    """
    active_base = GameData.get_active_base()
    if basic_info_label_global:
        basic_info_label_global.setText(active_base.name)

def update_summary_display() -> None:
    """
    Update summary statistics with formatted table display.
    
    Retrieves current base statistics and formats them as an aligned
    table for consistent display. Uses monospace formatting for proper
    column alignment.
    """
    global summary_label_global
    if summary_label_global:
        stats = GameData.get_base_summary()
        # Format as table with aligned columns
        summary_text = f"Units:    {stats['soldiers']:2d}\nTanks:    {stats['tanks']:2d}\nDogs:     {stats['dogs']:2d}\nAliens:   {stats['aliens']:2d}\nCapacity: {stats['capacity']:2d}"
        summary_label_global.setText(summary_text)

def adjust_color(hex_color: str, r: int = 0, g: int = 0, b: int = 0) -> str:
    """
    Adjust RGB values of a hex color.
    
    Args:
        hex_color: Base color in hex format (#RRGGBB)
        r: Red adjustment (-255 to 255)
        g: Green adjustment (-255 to 255)  
        b: Blue adjustment (-255 to 255)
        
    Returns:
        Adjusted color in hex format
        
    Clamps values to valid RGB range (0-255) to prevent overflow.
    """
    c = QColor(hex_color)
    c = QColor(min(255, c.red() + r), min(255, c.green() + g), min(255, c.blue() + b))
    return c.name()

def create_top_panel() -> QWidget:
    """
    Create the top navigation panel using the TopPanelWidget class.

    Returns:
        QWidget: Complete top panel with screen buttons, base buttons, and info labels
    """
    global top_panel_widget_global, basic_info_label_global

    # Create the TopPanelWidget instance
    panel = TopPanelWidget()

    # Connect signals to appropriate handlers
    panel.screen_changed.connect(switch_screen)
    panel.base_changed.connect(lambda base_index: refresh_base_data())

    # Store references for global access
    top_panel_widget_global = panel
    basic_info_label_global = panel.base_info_label

    return panel

def create_bottom_panel() -> QWidget:
    """
    Create the main interface panel with equipment slots and lists.
    
    Returns:
        QWidget: Complete bottom panel containing all interactive elements
        
    Creates the main game interface including:
    - Equipment slots for character customization
    - Unit list with filtering capabilities  
    - Item inventory with filtering
    - Character information displays
    - Weight tracking and template system
    - Summary statistics and controls
    
    Sets up all widget references, event connections, and initial data loading.
    """
    global equipment_slots_global, item_list_widget_global, weight_label_global
    global current_unit_global, unit_info_label_global
    global load_template_button_global, summary_label_global
    
    # Import custom widgets after globals are set
    from engine.gui.widgets import EquipmentSlotWidget, ItemListWidget, UnitListWidget
    
    bottom_panel = QWidget()
    bottom_panel.setStyleSheet(f"background: {XcomTheme.BG_MID};")
    bottom_layout = QVBoxLayout(bottom_panel)
    bottom_layout.setContentsMargins(0, 0, 0, 0)
    bottom_layout.setSpacing(0)

    # Create equipment slots from data structure
    equipment_slots = []
    for slot_data in GameData.get_equipment_slots():
        gx, gy = slot_data["position"]
        r_adj, g_adj, b_adj = slot_data["color_adjust"]

        slot_bg = adjust_color(XcomTheme.BG_LIGHT,
                               int(r_adj * 255),
                               int(g_adj * 255),
                               int(b_adj * 255))

        slot = EquipmentSlotWidget(slot_data["name"], bottom_panel,
                                   label_text=slot_data["name"],
                                   slot_type=slot_data["type"])
        slot.set_background_color(slot_bg)
        slot.set_border_color(XcomTheme.BORDER_COLOR)
        slot.setFixedSize(px(GRID * 4), px(GRID * 4))
        slot.move(px(GRID * gx), px(GRID * gy))
        slot.show()
        equipment_slots.append(slot)

    equipment_slots_global = equipment_slots  # Store global reference

    # TEMPLATE SYSTEM START - Add template buttons at 25x8 and 25x9 (moved up 2 grid)
    save_template_button = QPushButton("SAVE", bottom_panel)
    save_template_button.setFixedSize(px(GRID * 2), px(GRID * 1))
    save_template_button.move(px(GRID * 25), px(GRID * 8))
    save_template_button.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_SMALL))
    save_template_button.setStyleSheet(XcomStyle.pushbutton(rounded=True, border_width=1))
    save_template_button.clicked.connect(save_template)
    save_template_button.show()

    load_template_button_global = QPushButton("LOAD", bottom_panel)
    load_template_button_global.setFixedSize(px(GRID * 2), px(GRID * 1))
    load_template_button_global.move(px(GRID * 25), px(GRID * 9))  # Moved up 2 grid positions (was 11)
    load_template_button_global.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_SMALL))
    load_template_button_global.setStyleSheet(XcomStyle.pushbutton(rounded=True, border_width=1))
    load_template_button_global.clicked.connect(load_template)
    load_template_button_global.setEnabled(False)  # Disabled until template is saved
    load_template_button_global.show()
    
    # Add a test button for equipment slot validation
    def test_equipment_slots():
        pass
    
    test_button = QPushButton("TEST", bottom_panel)
    test_button.setFixedSize(px(GRID * 2), px(GRID * 1))
    test_button.move(px(GRID * 25), px(GRID * 10))  # Below LOAD button
    test_button.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_SMALL))
    test_button.setStyleSheet(XcomStyle.pushbutton(rounded=True, border_width=1))
    test_button.clicked.connect(test_equipment_slots)
    test_button.show()
    # TEMPLATE SYSTEM END

    # Weight display label between Armour and Weapon slots
    weight_label_global = QLabel("Weight: 0", bottom_panel)
    weight_label_global.setFixedSize(px(GRID * 4), px(GRID // 2))
    weight_label_global.move(px(GRID * 24), px(GRID * 6))  # Between armour (20) and weapon (28)
    weight_label_global.setAlignment(Qt.AlignmentFlag.AlignCenter)
    weight_label_global.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_NORMAL, QFont.Bold))
    weight_label_global.setStyleSheet(f"color: {XcomTheme.ACCENT_YELLOW}; background: transparent;")
    weight_label_global.show()

    # Soldier head image (non-interactive, just for display)
    head_display = QLabel(bottom_panel)
    head_display.setFixedSize(px(GRID * 4), px(GRID * 4))
    head_display.move(px(GRID * 24), px(GRID * 1))
    head_display.setStyleSheet(f"""
        QLabel {{
            background: {adjust_color(XcomTheme.BG_LIGHT, -int(0.05 * 255), -int(0.05 * 255), -int(0.05 * 255))};
            border: 3px solid {XcomTheme.BORDER_COLOR};
            border-radius: 4px;
        }}
    """)
    head_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
    head_display.setText("HEAD")
    head_display.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_SMALL))
    head_display.show()

    # Place summary groupbox at absolute position (1*GRID, 1*GRID) with left-aligned content
    summary_groupbox = QGroupBox("Summary", bottom_panel)
    summary_groupbox.setStyleSheet(XcomStyle.groupbox())
    summary_groupbox.setFixedSize(px(GRID * 6), px(GRID * 4))
    summary_groupbox.move(px(GRID * 1), px(GRID * 1))
    summary_groupbox.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
    
    # Add summary content with left-top alignment and monospace font for table formatting
    summary_layout = QVBoxLayout(summary_groupbox)
    summary_layout.setContentsMargins(px(1), px(3), px(1), px(1))
    summary_layout.setSpacing(0)
    summary_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
    
    summary_label_global = QLabel("Units:     0\nTanks:     0\nDogs:      0\nAliens:    0\nCapacity: 50", summary_groupbox)
    summary_label_global.setFont(QFont("Courier", XcomTheme.FONT_SIZE_SMALL))  # Monospace font for alignment
    summary_label_global.setStyleSheet(f"color: {XcomTheme.TEXT_BRIGHT}; background: transparent;")
    summary_label_global.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
    summary_layout.addWidget(summary_label_global)
    
    summary_groupbox.show()

    # Add unit_list widget at position (1*GRID, 6*GRID), size (6x14 grid cells)
    unit_list_groupbox = QGroupBox("", bottom_panel)
    unit_list_groupbox.setStyleSheet(XcomStyle.groupbox())
    unit_list_groupbox.setFixedSize(px(GRID * 6), px(GRID * 14))
    unit_list_groupbox.move(px(GRID * 1), px(GRID * 6))
    unit_list_groupbox.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
    unit_list_groupbox.setContentsMargins(px(0.5), px(0.5), 0, 0)

    # Add filter combobox and list widget inside unit_list
    unit_list_layout = QVBoxLayout(unit_list_groupbox)
    unit_list_layout.setContentsMargins(px(0.5), px(0.5), 0, 0)
    unit_list_layout.setSpacing(px(0.5))

    unit_filter_combo = QComboBox(unit_list_groupbox)
    unit_filter_combo.clear()
    for unit_category in GameData.get_unit_categories():
        unit_filter_combo.addItem(QIcon(QPixmap(unit_category["icon"]).scaled(32, 32)), unit_category["name"])
    unit_filter_combo.setStyleSheet(XcomStyle.combobox())
    unit_list_layout.addWidget(unit_filter_combo)

    unit_list_widget = UnitListWidget(unit_list_groupbox)
    
    # Store reference for base switching
    refresh_base_data.unit_list_widget = unit_list_widget
    
    # Load initial units
    for name, icon_path, info in GameData.get_current_base_units():
        item = QListWidgetItem(QIcon(QPixmap(icon_path).scaled(32, 32)), name)
        unit_list_widget.addUnitWithInfo(item, info)
    unit_list_widget.setStyleSheet(XcomStyle.listwidget())
    
    # Connect filter combo to filtering function
    unit_filter_combo.currentTextChanged.connect(unit_list_widget.filter_units)
    
    unit_list_layout.addWidget(unit_list_widget)
    unit_list_groupbox.show()

    # Add item_list widget at position (33*GRID, 1*GRID), size (6x21 grid cells)
    item_list = QGroupBox("", bottom_panel)
    item_list.setStyleSheet(XcomStyle.groupbox())
    item_list.setFixedSize(px(GRID * 6), px(GRID * 21))
    item_list.move(px(GRID * 33), px(GRID * 1))
    item_list.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
    item_list.setContentsMargins(px(0.5), px(0.5), 0, 0)

    # Add filter combobox and list widget inside item_list
    item_list_layout = QVBoxLayout(item_list)
    item_list_layout.setContentsMargins(px(0.5), px(0.5), 0, 0)
    item_list_layout.setSpacing(px(0.5))

    item_filter_combo = QComboBox(item_list)
    item_filter_combo.clear()
    for category in GameData.get_item_categories():
        item_filter_combo.addItem(QIcon(QPixmap(category["icon"]).scaled(32, 32)), category["name"])
    item_filter_combo.setStyleSheet(XcomStyle.combobox())
    item_list_layout.addWidget(item_filter_combo)

    item_list_widget = ItemListWidget(item_list)
    item_list_widget_global = item_list_widget  # Store global reference

    # Initialize with current base items
    for name, icon_path, info, count in GameData.get_current_base_items():
        # Use the same icon scaling as the list widget
        item = QListWidgetItem(QIcon(QPixmap(icon_path).scaled(32, 32, Qt.KeepAspectRatio, Qt.FastTransformation)),
                               f"{name} ({count})")
        item_list_widget.addItemWithInfo(item, info, count)
    item_list_widget.setStyleSheet(XcomStyle.listwidget())

    # Connect filter combo to filtering function
    item_filter_combo.currentTextChanged.connect(item_list_widget.filter_items)

    item_list_layout.addWidget(item_list_widget)
    item_list.show()

    # Add summary-like widget at position (8*GRID, 6*GRID), size (11x8 grid cells)
    unit_stats_groupbox = QGroupBox("Stats", bottom_panel)
    unit_stats_groupbox.setStyleSheet(XcomStyle.groupbox())
    unit_stats_groupbox.setFixedSize(px(GRID * 11), px(GRID * 8))
    unit_stats_groupbox.move(px(GRID * 8), px(GRID * 6))
    unit_stats_groupbox.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
    unit_stats_groupbox.setContentsMargins(px(0.5), px(0.5), 0, 0)
    unit_stats_groupbox.show()

    # Add another summary-like widget at position (8*GRID, 14*GRID), size (11x8 grid cells)
    traits_groupbox = QGroupBox("Traits", bottom_panel)
    traits_groupbox.setStyleSheet(XcomStyle.groupbox())
    traits_groupbox.setFixedSize(px(GRID * 11), px(GRID * 8))
    traits_groupbox.move(px(GRID * 8), px(GRID * 14))
    traits_groupbox.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
    traits_groupbox.setContentsMargins(px(0.5), px(0.5), 0, 0)
    traits_groupbox.show()

    # Add Fire button at position (3*GRID, 21*GRID), size (2x1 grid cells)
    fire_button = QPushButton("Fire", bottom_panel)
    fire_button.setFixedSize(px(GRID * 2 - 2), px(GRID - 2))
    fire_button.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_NORMAL))
    fire_button.move(px(GRID * 3), px(GRID * 21))
    fire_button.show()

    # Add basic info widget at position (8*GRID, 1*GRID), size (11x4 grid cells) with left-aligned content
    basic_info_groupbox = QGroupBox("Basic info", bottom_panel)
    basic_info_groupbox.setStyleSheet(XcomStyle.groupbox())
    basic_info_groupbox.setFixedSize(px(GRID * 11), px(GRID * 4))
    basic_info_groupbox.move(px(GRID * 8), px(GRID * 1))
    basic_info_groupbox.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
    
    # Add unit info label with left-top alignment
    basic_info_layout = QVBoxLayout(basic_info_groupbox)
    basic_info_layout.setContentsMargins(px(1), px(3), px(1), px(1))
    basic_info_layout.setSpacing(px(1))
    basic_info_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
    
    # Unit name and category label
    unit_info_label_global = QLabel("No unit selected", basic_info_groupbox)
    unit_info_label_global.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_NORMAL, QFont.Bold))
    unit_info_label_global.setStyleSheet(f"color: {XcomTheme.ACCENT_BLUE}; background: transparent;")
    unit_info_label_global.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
    basic_info_layout.addWidget(unit_info_label_global)
    
    basic_info_groupbox.show()

    # Initialize equipment slot states (default 2 equipment slots enabled)
    update_equipment_slot_states(2)
    
    # Update initial summary
    update_summary_display()
    
    # Update globals in widgets module to ensure proper cross-module communication
    import engine.gui.widgets
    engine.gui.widgets.equipment_slots_global = equipment_slots_global
    engine.gui.widgets.item_list_widget_global = item_list_widget_global
    engine.gui.widgets.weight_label_global = weight_label_global
    engine.gui.widgets.unit_inventory_manager_global = unit_inventory_manager
    engine.gui.widgets.current_unit_global = current_unit_global
    engine.gui.widgets.unit_info_label_global = unit_info_label_global
    print(f"🔧 MAIN_INTERFACE: Updated widgets globals - equipment_slots: {len(equipment_slots_global) if equipment_slots_global else 0}")

    return bottom_panel

def create_main_interface() -> QWidget:
    """
    Create the complete main interface layout.
    
    Returns:
        QWidget: Container widget with complete interface
        
    Combines top navigation panel and bottom main panel into
    a single vertical layout. This is the root widget for
    the entire application interface.
    """
    # Create top and bottom panels
    top_panel = create_top_panel()
    bottom_panel = create_bottom_panel()
    
    # Create main vertical layout
    main_vertical_layout = QVBoxLayout()
    main_vertical_layout.setContentsMargins(0, 0, 0, 0)
    main_vertical_layout.setSpacing(0)
    main_vertical_layout.addWidget(top_panel)
    main_vertical_layout.addWidget(bottom_panel)

    # Create container widget
    container = QWidget()
    container.setLayout(main_vertical_layout)
    return container

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QMainWindow

    app = QApplication(sys.argv)

    # Apply the global stylesheet to the entire application
    app.setStyleSheet(XcomStyle.get_global_stylesheet())

    win = QMainWindow()
    win.setWindowTitle("XCOM UI Enhanced - Full System v7.0")
    win.setFixedSize(SCALED_WIDTH, SCALED_HEIGHT)
    
    main_interface = create_main_interface()
    win.setCentralWidget(main_interface)
    win.show()
    
    sys.exit(app.exec())
