# Scaling constants
from PySide6.QtCore import Qt, QTimer, QPoint, QMimeData, QByteArray, QRect
from PySide6.QtGui import QFont, QIcon, QPixmap, QColor, QPainter, QDrag, QCursor, QDragEnterEvent, QDropEvent, \
    QMouseEvent, QPen, QBrush
from PySide6.QtWidgets import QVBoxLayout, QToolTip, QListWidget, QListWidgetItem, QAbstractItemView, QLabel, QGroupBox, \
    QMessageBox, QWidget
import json
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict, Any

SCALE = 2
BASE_WIDTH = 640
BASE_HEIGHT = 400
SCALED_WIDTH = BASE_WIDTH * SCALE
SCALED_HEIGHT = BASE_HEIGHT * SCALE

# Interface grid step and widget margin/padding
GRID = 16  # All widgets aligned to 8px grid
WIDGET_MARGIN = 1  # 1px margin for all widgets
WIDGET_PADDING = 1  # 1px padding for all widgets


# XCOM UI Theme Constants
class XcomTheme:
    # Colors - Covert Operations Theme
    BG_DARK = "#0a0e14"  # Darkest background - almost black with blue tint
    BG_MID = "#121a24"  # Mid-level background - dark navy blue
    BG_LIGHT = "#1e2836"  # Lighter background elements - steel blue

    ACCENT_GREEN = "#00cc66"  # Green accent (success, confirm) - neon green
    ACCENT_RED = "#ff3333"  # Red accent (danger, cancel) - bright red
    ACCENT_BLUE = "#3399ff"  # Blue accent (info, selection) - bright blue
    ACCENT_YELLOW = "#ffcc00"  # Yellow accent (warning, attention) - gold/amber

    TEXT_BRIGHT = "#ffffff"  # Bright text - white
    TEXT_MID = "#99ccff"  # Secondary text - light blue
    TEXT_DIM = "#607080"  # Disabled text - slate gray

    BORDER_COLOR = "#30465d"  # Border color for panels - dark slate blue

    # Dimensions
    BORDER_RADIUS = 0  # Border radius for elements (in pixels) - sharp corners for military look
    BORDER_WIDTH = 1  # Border width (in pixels)

    # Fonts
    FONT_FAMILY = "Consolas"  # Monospace font for tech/military look
    FONT_SIZE_SMALL = 9
    FONT_SIZE_NORMAL = 11
    FONT_SIZE_LARGE = 14


# Enhanced enums for item system
class ItemType(Enum):
    WEAPON = "weapon"
    ARMOR = "armor"
    HELMET = "helmet"
    EQUIPMENT = "equipment"
    AMMO = "ammo"
    OTHER = "other"


class ItemRarity(Enum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


# Helper function to scale pixel values
def px(x):
    return x * SCALE


# Enhanced Item class with proper attributes and drag/drop support
class InventoryItem:
    def __init__(self, name, icon_path, properties=None, item_type=ItemType.OTHER, rarity=ItemRarity.COMMON,
                 stackable=False, max_stack=1, item_id=None):
        self.name = name
        self.icon_path = icon_path or 'other/item.png'
        self.properties = properties or {}
        self.item_type = item_type
        self.rarity = rarity
        self.stackable = stackable
        self.max_stack = max_stack
        self.id = item_id or f"{name}_{hash(name) % 10000}"

        # Extract description from properties if available
        self.description = self.properties.get('desc', f"A {self.item_type.value}")

    def get_pixmap(self, size=64):
        return QPixmap(self.icon_path).scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    def get_icon(self, size=32):
        return QIcon(self.get_pixmap(size))

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'icon_path': self.icon_path,
            'properties': self.properties,
            'item_type': self.item_type.value,
            'rarity': self.rarity.value,
            'stackable': self.stackable,
            'max_stack': self.max_stack,
            'description': self.description
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'InventoryItem':
        return cls(
            name=data['name'],
            icon_path=data['icon_path'],
            properties=data.get('properties', {}),
            item_type=ItemType(data.get('item_type', 'other')),
            rarity=ItemRarity(data.get('rarity', 'common')),
            stackable=data.get('stackable', False),
            max_stack=data.get('max_stack', 1),
            item_id=data.get('id')
        )

    def can_stack_with(self, other: 'InventoryItem') -> bool:
        return (self.stackable and other.stackable and
                self.id == other.id and self.name == other.name)


# Centralized style helpers
class XcomStyle:
    @staticmethod
    def groupbox(bg=None, border_col=None, border_width=2, font_size=None, margin_top=3.5, label_font_size=None,
                 rounded=True):
        bg = bg or XcomTheme.BG_LIGHT
        border_col = border_col or XcomTheme.BORDER_COLOR
        font_size = font_size or (XcomTheme.FONT_SIZE_LARGE + 2)
        label_font_size = label_font_size or font_size
        border_radius = 4 if rounded else 0
        label_bg = bg  # Use the same as groupbox background for a subtle look
        return (
            f"QGroupBox {{ background: {bg}; border: {border_width}px solid {border_col}; border-radius: {border_radius}px; margin-top: {px(margin_top)}px; "
            f"color: {XcomTheme.TEXT_MID}; font-size: {font_size}px; padding-left: {px(0.5)}px; }} "
            f"QGroupBox:title {{ subcontrol-origin: margin; subcontrol-position: top center; left: 0px; top: 0px; "
            f"padding: 0 {px(3)}px; background: {label_bg}; font-size: {label_font_size}px; border-radius: {border_radius}px; }}"
        )

    @staticmethod
    def combobox():
        return (
            f"QComboBox {{ background: {XcomTheme.BG_DARK}; color: {XcomTheme.TEXT_BRIGHT}; font-size: {XcomTheme.FONT_SIZE_LARGE}px; font-family: {XcomTheme.FONT_FAMILY}; "
            f"border: 1px solid {XcomTheme.BORDER_COLOR}; border-radius: 0px; padding: {px(0.5)}px; }} "
            f"QComboBox:hover {{ border: 1px solid {XcomTheme.ACCENT_BLUE}; }} "
            f"QComboBox::drop-down {{ border: 0px; background: {XcomTheme.BG_MID}; width: {px(GRID * 0.8)}px; }} "
            f"QComboBox::down-arrow {{ width: {px(GRID * 0.5)}px; height: {px(GRID * 0.5)}px; background: {XcomTheme.TEXT_MID}; }}"
            f"QComboBox QAbstractItemView {{ background: {XcomTheme.BG_LIGHT}; color: {XcomTheme.TEXT_BRIGHT}; "
            f"border: 2px solid {XcomTheme.BORDER_COLOR}; selection-background-color: {XcomTheme.BG_MID}; outline: 0; }}"
        )

    @staticmethod
    def listwidget():
        return (
            f"QListWidget {{ background: {XcomTheme.BG_DARK}; color: {XcomTheme.TEXT_BRIGHT}; font-size: {XcomTheme.FONT_SIZE_LARGE}px; font-family: {XcomTheme.FONT_FAMILY}; "
            f"border: 1px solid {XcomTheme.BORDER_COLOR}; border-radius: 0px; outline: 0; padding: 2px; }} "
            f"QListWidget::item {{ padding: {px(0.5)}px; border: none; }} "
            f"QListWidget::item:hover {{ background: {XcomTheme.BG_MID}; color: {XcomTheme.TEXT_BRIGHT}; }} "
            f"QListWidget::item:selected {{ background: {XcomTheme.BG_MID}; color: {XcomTheme.ACCENT_BLUE}; }}"
        )

    @staticmethod
    def pushbutton(rounded=True, border_width=1):
        border_radius = 4 if rounded else 0
        return (
            f"QPushButton {{ "
            f"background: {XcomTheme.BG_LIGHT}; "
            f"color: {XcomTheme.TEXT_BRIGHT}; "
            f"border: {border_width}px solid {XcomTheme.BORDER_COLOR if border_width else 'transparent'}; "
            f"border-radius: {border_radius}px; "
            f"margin: {px(WIDGET_MARGIN)}px; "
            f"padding: {px(WIDGET_PADDING)}px; "
            f"font-family: {XcomTheme.FONT_FAMILY}; "
            f"font-size: {XcomTheme.FONT_SIZE_NORMAL}px; "
            f"}} "
            f"QPushButton:hover {{ background: {XcomTheme.ACCENT_BLUE}; color: {XcomTheme.BG_DARK}; }} "
            f"QPushButton:pressed {{ background: {XcomTheme.BG_DARK}; color: {XcomTheme.ACCENT_BLUE}; }}"
        )

    @staticmethod
    def pushbutton_changebase():
        # Square, no border, no rounding, custom hover
        return (
            f"QPushButton.changebase {{ "
            f"background: {XcomTheme.BG_MID}; "
            f"color: {XcomTheme.TEXT_BRIGHT}; "
            f"border: none; "
            f"border-radius: 0px; "
            f"margin: 0px; "
            f"padding: 0px; "
            f"font-family: {XcomTheme.FONT_FAMILY}; "
            f"font-size: {XcomTheme.FONT_SIZE_SMALL}px; "
            f"}} "
            f"QPushButton.changebase:hover {{ background: {XcomTheme.ACCENT_YELLOW}; color: {XcomTheme.BG_DARK}; }} "
            f"QPushButton.changebase:pressed {{ background: {XcomTheme.BG_DARK}; color: {XcomTheme.ACCENT_YELLOW}; }}"
        )

    @staticmethod
    def label():
        return (
            f"QLabel {{ "
            f"color: {XcomTheme.TEXT_BRIGHT}; "
            f"background: transparent; "
            f"font-family: {XcomTheme.FONT_FAMILY}; "
            f"padding: 0px; "
            f"margin: 0px; "
            f"}}"
        )

    @staticmethod
    def get_global_stylesheet():
        """Returns a complete stylesheet for the entire application"""
        border_radius = 4
        return f"""
        /* Base Widget Styling */
        QWidget {{
            background: {XcomTheme.BG_MID};
            color: {XcomTheme.TEXT_BRIGHT};
            font-family: {XcomTheme.FONT_FAMILY};
        }}

        /* Button Styling */
        {XcomStyle.pushbutton(rounded=True, border_width=2)}

        /* ChangeBase Button Styling */
        {XcomStyle.pushbutton_changebase()}

        /* Label Styling */
        {XcomStyle.label()}

        /* GroupBox Styling */
        QGroupBox {{
            background: {XcomTheme.BG_LIGHT};
            border: 2px solid {XcomTheme.BORDER_COLOR};
            border-radius: {border_radius}px;
            margin-top: {px(3.5)}px;
            color: {XcomTheme.TEXT_MID};
            font-size: {XcomTheme.FONT_SIZE_LARGE + 2}px;
            padding-left: {px(0.5)}px;
        }}

        QGroupBox:title {{
            subcontrol-origin: margin;
            subcontrol-position: top center;
            left: 0px;
            top: 0px;
            padding: 0 {px(3)}px;
            background: {XcomTheme.BG_LIGHT};
            font-size: {XcomTheme.FONT_SIZE_LARGE}px;
            border-radius: {border_radius}px;
        }}

        /* ComboBox Styling */
        {XcomStyle.combobox()}

        /* ListWidget Styling */
        {XcomStyle.listwidget()}

        /* Special Panel Styling */
        #topPanel {{
            background: {XcomTheme.BG_DARK};
        }}

        #bottomPanel {{
            background: {XcomTheme.BG_MID};
        }}
        """


# Top panel with grid-aligned buttons
def create_top_panel():
    from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QFrame, QLabel, QHBoxLayout, QVBoxLayout, \
        QButtonGroup
    from PySide6.QtGui import QFont
    from PySide6.QtCore import Qt

    panel = QWidget()
    panel.setFixedHeight(px(GRID * 2))
    panel.setStyleSheet(f"background: {XcomTheme.BG_DARK};")

    # Layout for main buttons
    layout_change_panel = QHBoxLayout()
    layout_change_panel.setContentsMargins(0, 0, 0, 0)
    layout_change_panel.setSpacing(0)
    button_labels = [
        "GEO", "BUILD", "BARRACKS", "HANGAR", "STORAGE", "TRANSFER",
        "PRISON", "ACADEMY", "WORKSHOP", "LAB", "MARKET", "ARCHIVE", "INFO"
    ]
    for label in button_labels:
        btn = QPushButton(label)
        btn.setFixedSize(px(GRID * 2 - 2 * WIDGET_MARGIN), px(GRID * 2 - 2 * WIDGET_MARGIN))
        btn.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_NORMAL))
        btn.setStyleSheet(XcomStyle.pushbutton(rounded=True, border_width=2))
        layout_change_panel.addWidget(btn)

    # Layout for 12 large base switch buttons (A-L)
    layout_change_base = QGridLayout()
    layout_change_base.setContentsMargins(0, 0, 0, 0)
    layout_change_base.setSpacing(0)
    base_letters = [
        'A', 'B', 'C', 'D', 'E', 'F',
        'G', 'H', 'I', 'J', 'K', 'L'
    ]
    base_btn_group = QButtonGroup(panel)
    base_btn_group.setExclusive(True)
    base_btns = []
    for idx, letter in enumerate(base_letters):
        btn = QPushButton(letter)
        btn.setFixedSize(px(GRID), px(GRID))

        btn.setProperty("class", "changebase")
        btn.setStyleSheet(XcomStyle.pushbutton_changebase())
        btn.setCheckable(True)
        btn.setFont(QFont(XcomTheme.FONT_FAMILY, px(GRID * 2)))  # Much larger font, scales with GRID
        base_btn_group.addButton(btn, idx)
        row = 0 if idx < 6 else 1
        col = idx if idx < 6 else idx - 6
        layout_change_base.addWidget(btn, row, col)
        base_btns.append(btn)
    base_btns[0].setChecked(True)

    # Ensure at least one button is always selected
    def ensure_one_selected(id):
        checked = [b for b in base_btns if b.isChecked()]
        if not checked:
            base_btns[id].setChecked(True)

    base_btn_group.buttonClicked.connect(lambda btn: ensure_one_selected(base_btn_group.id(btn)))

    # Layout for labels
    layout_labels = QGridLayout()
    layout_labels.setContentsMargins(0, 0, 0, 0)
    layout_labels.setSpacing(0)
    base_name = "OMEGA"
    current_date = "MAY 29, 2025"
    current_money = "$3,500,000"
    label1 = QLabel(base_name)
    label1.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_LARGE))
    label1.setStyleSheet(f"color: {XcomTheme.ACCENT_YELLOW}; background: transparent; padding: 0px; margin: 0px;")
    label1.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
    label2 = QLabel(current_date)
    label2.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_NORMAL))
    label2.setStyleSheet(f"color: {XcomTheme.TEXT_BRIGHT}; background: transparent; padding: 0px; margin: 0px;")
    label2.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
    label3 = QLabel(current_money)
    label3.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_NORMAL))
    label3.setStyleSheet(f"color: {XcomTheme.ACCENT_GREEN}; background: transparent; padding: 0px; margin: 0px;")
    label3.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
    layout_labels.addWidget(label1, 0, 0, 1, 4)
    layout_labels.addWidget(label2, 1, 0, 1, 2)
    layout_labels.addWidget(label3, 1, 2, 1, 2)

    # Main horizontal layout to combine all sections
    main_layout = QHBoxLayout(panel)
    main_layout.setContentsMargins(0, 0, 0, 0)
    main_layout.setSpacing(0)
    main_layout.addLayout(layout_change_panel, 26)
    main_layout.addLayout(layout_change_base, 6)
    main_layout.addLayout(layout_labels, 12)
    panel.setLayout(main_layout)

    # --- Bottom panel ---
    from PySide6.QtWidgets import QVBoxLayout, QComboBox, QListWidgetItem
    from PySide6.QtGui import QColor, QIcon, QPixmap
    bottom_panel = QWidget()
    bottom_panel.setStyleSheet(f"background: {XcomTheme.BG_MID};")
    bottom_layout = QVBoxLayout(bottom_panel)
    bottom_layout.setContentsMargins(0, 0, 0, 0)
    bottom_layout.setSpacing(0)

    # Helper function to adjust color
    def adjust_color(hex_color, r=0, g=0, b=0):
        c = QColor(hex_color)
        c = QColor(min(255, c.red() + r), min(255, c.green() + g), min(255, c.blue() + b))
        return c.name()

    # Use centralized styles for all groupboxes and widgets
    # Head (24x1), black tint (5% darker)
    head_bg = adjust_color(XcomTheme.BG_LIGHT, -int(0.05 * 255), -int(0.05 * 255), -int(0.05 * 255))
    head_slot = EquipmentSlotWidget('Head', bottom_panel, label_text='Head', slot_type=ItemType.HELMET)
    head_slot.set_background_color(head_bg)
    head_slot.set_border_color(XcomTheme.BORDER_COLOR)
    head_slot.setFixedSize(px(GRID * 4), px(GRID * 4))
    head_slot.move(px(GRID * 24), px(GRID * 1))
    head_slot.show()

    # Armour (20x7), blue tint (5% more blue)
    armour_bg = adjust_color(XcomTheme.BG_LIGHT, 0, 0, int(0.05 * 255))
    armour_slot = EquipmentSlotWidget('Armour', bottom_panel, label_text='Armour', slot_type=ItemType.ARMOR)
    armour_slot.set_background_color(armour_bg)
    armour_slot.set_border_color(XcomTheme.BORDER_COLOR)
    armour_slot.setFixedSize(px(GRID * 4), px(GRID * 4))
    armour_slot.move(px(GRID * 20), px(GRID * 7))
    armour_slot.show()

    # Primary Weapon (28x7), red tint (5% more red)
    weapon_bg = adjust_color(XcomTheme.BG_LIGHT, int(0.05 * 255), 0, 0)
    weapon_slot = EquipmentSlotWidget('Weapon', bottom_panel, label_text='Weapon', slot_type=ItemType.WEAPON)
    weapon_slot.set_background_color(weapon_bg)
    weapon_slot.set_border_color(XcomTheme.BORDER_COLOR)
    weapon_slot.setFixedSize(px(GRID * 4), px(GRID * 4))
    weapon_slot.move(px(GRID * 28), px(GRID * 7))
    weapon_slot.show()

    # Equipment slots (green tint - 5% more green)
    equip_bg = adjust_color(XcomTheme.BG_LIGHT, 0, int(0.05 * 255), 0)
    equip_positions = [(21, 13), (21, 18), (27, 13), (27, 18)]
    equip_slots = []
    for idx, (gx, gy) in enumerate(equip_positions):
        slot = EquipmentSlotWidget(f'Equipment{idx + 1}', bottom_panel, label_text=f'Equipment {idx + 1}',
                                   slot_type=ItemType.EQUIPMENT)
        slot.set_background_color(equip_bg)
        slot.set_border_color(XcomTheme.BORDER_COLOR)
        slot.setFixedSize(px(GRID * 4), px(GRID * 4))
        slot.move(px(GRID * gx), px(GRID * gy))
        slot.show()
        equip_slots.append(slot)

    # Place screen_summary at absolute position (2*GRID, 4*GRID)
    summary_groupbox = QGroupBox("Summary", bottom_panel)
    summary_groupbox.setStyleSheet(XcomStyle.groupbox())
    summary_groupbox.setFixedSize(px(GRID * 6), px(GRID * 4))
    summary_groupbox.move(px(GRID * 1), px(GRID * 1))
    summary_groupbox.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
    summary_groupbox.setContentsMargins(px(0.5), px(0.5), 0, 0)
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

    filter_combo = QComboBox(unit_list_groupbox)
    filter_combo.clear()
    filter_combo.addItem(QIcon(QPixmap('icon_a.png').scaled(32, 32)), "All")
    filter_combo.addItem(QIcon(QPixmap('icon_b.png').scaled(32, 32)), "Soldiers")
    filter_combo.addItem(QIcon(QPixmap('icon_c.png').scaled(32, 32)), "Vehicles")
    filter_combo.addItem(QIcon(QPixmap('icon_d.png').scaled(32, 32)), "Robots")
    filter_combo.setStyleSheet(XcomStyle.combobox())
    unit_list_layout.addWidget(filter_combo)

    unit_list_widget = ItemListWidget(unit_list_groupbox)
    items_with_icons = [
        ("Tom Bladko", "icon_a.png", {"type": "Soldier", "class": "Sniper", "level": 5, "desc": "Veteran marksman."}),
        ("Jak Kowalski", "icon_b.png", {"type": "Soldier", "class": "Heavy", "level": 3, "desc": "Explosives expert."}),
        ("Megan Fox", "icon_c.png", {"type": "Soldier", "class": "Scout", "level": 2, "desc": "Fast and agile."}),
        ("John Smith", "icon_d.png", {"type": "Soldier", "class": "Medic", "level": 4, "desc": "Field medic."}),
        ("Sarah Connor", "icon_a.png", {"type": "Soldier", "class": "Leader", "level": 6, "desc": "Squad commander."}),
        ("RoboCop", "icon_b.png", {"type": "Robot", "class": "Enforcer", "level": 7, "desc": "Law enforcement droid."}),
        ("Tank", "icon_c.png", {"type": "Vehicle", "class": "Support", "level": 2, "desc": "Armored support vehicle."}),
        ("Drone", "icon_d.png", {"type": "Robot", "class": "Recon", "level": 1, "desc": "Aerial recon drone."}),
    ]
    for name, icon_path, info in items_with_icons:
        item = QListWidgetItem(QIcon(QPixmap(icon_path).scaled(32, 32)), name)
        unit_list_widget.addItemWithInfo(item, info)
    unit_list_widget.setStyleSheet(XcomStyle.listwidget())
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
    item_filter_combo.addItem(QIcon(QPixmap('other/item2.png').scaled(32, 32)), "All")
    item_filter_combo.addItem(QIcon(QPixmap('other/item2.png').scaled(32, 32)), "Armours")
    item_filter_combo.addItem(QIcon(QPixmap('other/item2.png').scaled(32, 32)), "Weapons")
    item_filter_combo.addItem(QIcon(QPixmap('other/item.png').scaled(32, 32)), "Equipment")
    item_filter_combo.addItem(QIcon(QPixmap('other/item.png').scaled(32, 32)), "Ammo")
    item_filter_combo.addItem(QIcon(QPixmap('other/item.png').scaled(32, 32)), "Other")
    item_filter_combo.setStyleSheet(XcomStyle.combobox())
    item_list_layout.addWidget(item_filter_combo)

    item_list_widget = ItemListWidget(item_list)
    items_with_icons = [
        ("Laser Rifle", "other/item2.png",
         {"type": "Weapon", "class": "Rifle", "level": 3, "desc": "High-energy laser weapon.", "item_type": "weapon",
          "rarity": "rare"}),
        ("Plasma Pistol", "other/item2.png",
         {"type": "Weapon", "class": "Pistol", "level": 2, "desc": "Compact plasma sidearm.", "item_type": "weapon",
          "rarity": "uncommon"}),
        ("Nano Armour", "other/item2.png",
         {"type": "Armour", "class": "Nano", "level": 4, "desc": "Lightweight, strong armor.", "item_type": "armor",
          "rarity": "epic"}),
        ("Combat Helmet", "other/item2.png",
         {"type": "Helmet", "class": "Combat", "level": 2, "desc": "Standard issue helmet.", "item_type": "helmet",
          "rarity": "common"}),
        ("Grenade", "other/item.png",
         {"type": "Equipment", "class": "Explosive", "level": 1, "desc": "Standard frag grenade.",
          "item_type": "equipment", "rarity": "common", "stackable": True, "max_stack": 5}),
        ("Medikit", "other/item.png",
         {"type": "Equipment", "class": "Medical", "level": 1, "desc": "Heals wounds in battle.",
          "item_type": "equipment", "rarity": "common", "stackable": True, "max_stack": 3}),
        ("Ammo Pack", "other/item.png",
         {"type": "Ammo", "class": "Universal", "level": 1, "desc": "Ammunition for various weapons.",
          "item_type": "ammo", "rarity": "common", "stackable": True, "max_stack": 10}),
        ("Shield Generator", "other/item.png",
         {"type": "Equipment", "class": "Defensive", "level": 5, "desc": "Projects a protective shield.",
          "item_type": "equipment", "rarity": "legendary"}),
    ]
    for name, icon_path, info in items_with_icons:
        item = QListWidgetItem(QIcon(QPixmap(icon_path).scaled(32, 32)), name)
        item_list_widget.addItemWithInfo(item, info)
    item_list_widget.setStyleSheet(XcomStyle.listwidget())
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
    fire_button.setFixedSize(px(GRID * 2 - 2 * WIDGET_MARGIN), px(GRID - 2 * WIDGET_MARGIN))
    fire_button.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_NORMAL))
    fire_button.move(px(GRID * 3), px(GRID * 21))
    fire_button.show()

    # Add new summary-like widget at position (8*GRID, 1*GRID), size (11x5 grid cells)
    summary4 = QGroupBox("Basic info", bottom_panel)
    summary4.setStyleSheet(XcomStyle.groupbox())
    summary4.setFixedSize(px(GRID * 11), px(GRID * 4))
    summary4.move(px(GRID * 8), px(GRID * 1))
    summary4.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
    summary4.setContentsMargins(px(0.5), px(0.5), 0, 0)
    summary4.show()

    # No layout, just absolute positioning
    # Add bottom_panel to a main vertical layout with the top panel
    from PySide6.QtWidgets import QVBoxLayout
    main_vertical_layout = QVBoxLayout()
    main_vertical_layout.setContentsMargins(0, 0, 0, 0)
    main_vertical_layout.setSpacing(0)
    main_vertical_layout.addWidget(panel)
    main_vertical_layout.addWidget(bottom_panel)

    # Create a container widget to hold both panels
    container = QWidget()
    container.setLayout(main_vertical_layout)
    return container


class EquipmentSlotWidget(QWidget):
    def __init__(self, slot_name, parent=None, label_text=None, slot_type=None):
        super().__init__(parent)
        self.slot_name = slot_name
        self.slot_type = slot_type  # ItemType enum value
        self.item = None  # InventoryItem or None
        self.stack_size = 0
        self.setAcceptDrops(True)

        # Make the widget perfectly square and grid-aligned
        self.setFixedSize(px(4 * GRID), px(4 * GRID))

        # Widget style settings
        self._border_radius = 4
        self._border_width = 3
        self._border_color = XcomTheme.BORDER_COLOR
        self._bg_color = XcomTheme.BG_LIGHT
        self._icon_size = px(3 * GRID)
        self.setToolTip(label_text if label_text else slot_name)

        # Make widget transparent so our custom painting works properly
        self.setAttribute(Qt.WA_StyledBackground, False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

    def set_background_color(self, color):
        self._bg_color = color
        self.update()

    def set_border_color(self, color):
        self._border_color = color
        self.update()

    def can_accept_item(self, item: InventoryItem) -> bool:
        """Check if this slot can accept the given item"""
        if self.slot_type and item.item_type != self.slot_type:
            return False

        if self.item is None:
            return True

        # Check if items can stack
        if (self.item.can_stack_with(item) and
                self.stack_size < self.item.max_stack):
            return True

        return False

    def add_item(self, item: InventoryItem, quantity: int = 1) -> bool:
        """Add an item to this slot"""
        if not self.can_accept_item(item):
            return False

        if self.item is None:
            self.item = item
            self.stack_size = quantity
        elif self.item.can_stack_with(item):
            self.stack_size += quantity
            if self.stack_size > self.item.max_stack:
                self.stack_size = self.item.max_stack
        else:
            return False

        self.update()
        return True

    def remove_item(self, quantity: int = None) -> Optional[InventoryItem]:
        """Remove item(s) from this slot"""
        if self.item is None:
            return None

        if quantity is None or quantity >= self.stack_size:
            # Remove all
            item = self.item
            self.item = None
            self.stack_size = 0
            self.update()
            return item
        else:
            # Remove partial stack
            self.stack_size -= quantity
            if self.stack_size <= 0:
                item = self.item
                self.item = None
                self.stack_size = 0
                self.update()
                return item
            else:
                self.update()
                return self.item

    def set_item(self, item):
        """Legacy method for compatibility"""
        if item:
            self.add_item(item)
        else:
            self.clear_item()

    def clear_item(self):
        """Clear the item from this slot"""
        self.item = None
        self.stack_size = 0
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()

        # Draw widget background and border
        painter.setPen(QPen(QColor(self._border_color), self._border_width))
        painter.setBrush(QBrush(QColor(self._bg_color)))
        painter.drawRoundedRect(self._border_width / 2, self._border_width / 2,
                                w - self._border_width, h - self._border_width,
                                self._border_radius, self._border_radius)

        # Draw icon (centered in slot area)
        slot_rect = QRect(self._border_width * 2, self._border_width * 2,
                          w - 4 * self._border_width,
                          h - 4 * self._border_width)

        if self.item:
            pixmap = self.item.get_pixmap(min(slot_rect.width(), slot_rect.height()) - px(8))
            icon_x = slot_rect.x() + (slot_rect.width() - pixmap.width()) // 2
            icon_y = slot_rect.y() + (slot_rect.height() - pixmap.height()) // 2
            painter.drawPixmap(icon_x, icon_y, pixmap)

            # Draw stack size if applicable
            if self.item.stackable and self.stack_size > 1:
                painter.setPen(QPen(QColor(XcomTheme.TEXT_BRIGHT), 2))
                painter.setFont(QFont(XcomTheme.FONT_FAMILY, 10, QFont.Bold))
                painter.drawText(slot_rect.adjusted(2, 2, -2, -2),
                                 Qt.AlignBottom | Qt.AlignRight, str(self.stack_size))
        else:
            # Draw a subtle placeholder (dashed line square)
            pen = QPen(QColor(self._border_color))
            pen.setStyle(Qt.DashLine)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(slot_rect.adjusted(px(4), px(4), -px(4), -px(4)))

    def dragEnterEvent(self, event: QDragEnterEvent):
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
                    # Visual feedback - green border for valid drop
                    self._border_color = XcomTheme.ACCENT_GREEN
                    self.update()
                else:
                    event.ignore()
                    # Visual feedback - red border for invalid drop
                    self._border_color = XcomTheme.ACCENT_RED
                    self.update()
            except Exception as e:
                print(f"Drag enter error: {e}")
                event.ignore()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        # Restore original border color
        self._border_color = XcomTheme.BORDER_COLOR
        self.update()

    def dropEvent(self, event: QDropEvent):
        try:
            data = json.loads(event.mimeData().text())
            item = InventoryItem.from_dict(data['item'])
            stack_size = data.get('stack_size', 1)

            if self.can_accept_item(item):
                # Handle item swapping or stacking
                if self.item and not self.item.can_stack_with(item):
                    # TODO: Implement item swapping
                    pass

                self.add_item(item, stack_size)
                event.acceptProposedAction()
            else:
                event.ignore()
        except Exception as e:
            print(f"Drop error: {e}")
            event.ignore()

        # Restore original border color
        self._border_color = XcomTheme.BORDER_COLOR
        self.update()

    def mousePressEvent(self, event: QMouseEvent):
        if self.item and event.button() == Qt.MouseButton.LeftButton:
            self.start_drag()
        else:
            super().mousePressEvent(event)

    def start_drag(self):
        """Start dragging this slot's item"""
        if not self.item:
            return

        # Create drag object
        drag = QDrag(self)
        mime_data = QMimeData()

        # Store item data as JSON
        item_data = {
            'item': self.item.to_dict(),
            'stack_size': self.stack_size,
            'source_slot': id(self)
        }
        mime_data.setText(json.dumps(item_data))
        drag.setMimeData(mime_data)

        # Create drag pixmap
        pixmap = self.item.get_pixmap(64)

        # Add visual effects to drag pixmap
        painter = QPainter(pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceAtop)
        painter.fillRect(pixmap.rect(), QColor(255, 255, 255, 100))  # Semi-transparent overlay
        painter.end()

        drag.setPixmap(pixmap)
        drag.setHotSpot(QPoint(32, 32))

        # Execute drag
        result = drag.exec(Qt.MoveAction)
        if result == Qt.MoveAction:
            # Item was moved, remove from this slot
            self.remove_item()

    def enterEvent(self, event):
        """Show tooltip with item information"""
        if self.item:
            tooltip_text = f"<b>{self.item.name}</b><br>"
            tooltip_text += f"<i>{self.item.rarity.value.title()}</i><br>"
            tooltip_text += f"Type: {self.item.item_type.value.title()}<br>"
            tooltip_text += f"{self.item.description}"
            if self.item.stackable and self.stack_size > 1:
                tooltip_text += f"<br>Stack: {self.stack_size}/{self.item.max_stack}"

            QToolTip.showText(self.mapToGlobal(QPoint(0, 0)), tooltip_text)


class ItemListWidget(QListWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        QToolTip.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_LARGE))
        self.item_info = {}
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setMouseTracking(True)
        self.setDragDropMode(QAbstractItemView.DragOnly)
        self.tooltip_bg = XcomTheme.BG_LIGHT
        self.tooltip_border = XcomTheme.ACCENT_BLUE

    def addItemWithInfo(self, item, info_dict):
        """Add an item with associated information to the list"""
        # Normalize the info dictionary
        if 'icon_path' not in info_dict and hasattr(item, 'icon'):
            icon = item.icon()
            if not icon.isNull():
                info_dict['icon_path'] = 'other/item.png'

        self.addItem(item)
        self.item_info[item.text()] = info_dict

    def getItemData(self, item):
        """Get the complete data for an item as an InventoryItem object"""
        if not item:
            return None

        name = item.text()
        info = self.item_info.get(name, {})
        icon_path = info.get('icon_path', 'other/item.png')

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

        return InventoryItem(
            name=name,
            icon_path=icon_path,
            properties=info,
            item_type=item_type,
            rarity=rarity,
            stackable=info.get('stackable', False),
            max_stack=info.get('max_stack', 1)
        )

    def startDrag(self, supportedActions):
        """Override to implement custom drag behavior"""
        current_item = self.currentItem()
        if not current_item:
            return

        item_data = self.getItemData(current_item)
        if not item_data:
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

        # Set drag pixmap
        if current_item.icon() and not current_item.icon().isNull():
            drag.setPixmap(current_item.icon().pixmap(64, 64))

        # Execute drag (using Copy action since we're not removing from list)
        drag.exec(Qt.CopyAction)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.position().toPoint()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return

        if not hasattr(self, 'drag_start_position'):
            return

        if ((event.position().toPoint() - self.drag_start_position).manhattanLength() <
                QApplication.startDragDistance()):
            return

        self.startDrag(Qt.CopyAction)


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication, QMainWindow
    import sys

    app = QApplication(sys.argv)

    # Apply the global stylesheet to the entire application
    app.setStyleSheet(XcomStyle.get_global_stylesheet())

    win = QMainWindow()
    win.setWindowTitle("XCOM UI Theme Demo - Enhanced Inventory System")
    win.setFixedSize(SCALED_WIDTH, SCALED_HEIGHT)
    top_panel = create_top_panel()
    win.setCentralWidget(top_panel)
    win.show()
    sys.exit(app.exec())