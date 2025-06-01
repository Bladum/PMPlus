# Scaling constants
from PySide6.QtCore import Qt, QTimer, QPoint, QMimeData, QByteArray, QRect
from PySide6.QtGui import QFont, QIcon, QPixmap, QColor, QPainter, QDrag, QCursor, QDragEnterEvent, QDropEvent, \
    QMouseEvent, QPen, QBrush
from PySide6.QtWidgets import QVBoxLayout, QToolTip, QListWidget, QListWidgetItem, QAbstractItemView, QLabel, QGroupBox, \
    QMessageBox, QWidget, QApplication
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


# Updated item categories
class ItemType(Enum):
    ARMOUR = "armour"
    WEAPON = "weapon"
    EQUIPMENT = "equipment"
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


# External data structures for easier management
class GameData:
    @staticmethod
    def get_unit_types():
        return [
            {"name": "All", "icon": "icon_a.png"},
            {"name": "Soldiers", "icon": "icon_b.png"},
            {"name": "Vehicles", "icon": "icon_c.png"},
            {"name": "Robots", "icon": "icon_d.png"},
        ]

    @staticmethod
    def get_item_categories():
        return [
            {"name": "All", "icon": "other/item2.png"},
            {"name": "Armour", "icon": "other/item2.png"},
            {"name": "Weapon", "icon": "other/item2.png"},
            {"name": "Equipment", "icon": "other/item.png"},
            {"name": "Other", "icon": "other/item.png"},
        ]

    @staticmethod
    def get_units():
        return [
            ("Tom Bladko", "icon_a.png",
             {"type": "Soldier", "class": "Sniper", "level": 5, "desc": "Veteran marksman."}),
            ("Jak Kowalski", "icon_b.png",
             {"type": "Soldier", "class": "Heavy", "level": 3, "desc": "Explosives expert."}),
            ("Megan Fox", "icon_c.png", {"type": "Soldier", "class": "Scout", "level": 2, "desc": "Fast and agile."}),
            ("John Smith", "icon_d.png", {"type": "Soldier", "class": "Medic", "level": 4, "desc": "Field medic."}),
            ("Sarah Connor", "icon_a.png",
             {"type": "Soldier", "class": "Leader", "level": 6, "desc": "Squad commander."}),
            ("RoboCop", "icon_b.png",
             {"type": "Robot", "class": "Enforcer", "level": 7, "desc": "Law enforcement droid."}),
            ("Tank", "icon_c.png",
             {"type": "Vehicle", "class": "Support", "level": 2, "desc": "Armored support vehicle."}),
            ("Drone", "icon_d.png", {"type": "Robot", "class": "Recon", "level": 1, "desc": "Aerial recon drone."}),
        ]

    @staticmethod
    def get_items():
        return [
            # Weapons
            ("Laser Rifle", "other/item2.png",
             {"type": "Weapon", "class": "Rifle", "level": 3, "desc": "High-energy laser weapon.",
              "item_type": "weapon", "rarity": "rare", "weight": 4}, 2),
            ("Plasma Pistol", "other/item2.png",
             {"type": "Weapon", "class": "Pistol", "level": 2, "desc": "Compact plasma sidearm.", "item_type": "weapon",
              "rarity": "uncommon", "weight": 2}, 3),
            ("Heavy Cannon", "other/item2.png",
             {"type": "Weapon", "class": "Heavy", "level": 4, "desc": "Devastating heavy weapon.",
              "item_type": "weapon", "rarity": "epic", "weight": 8}, 1),

            # Armours with equipment slots
            ("Light Armour", "other/item2.png",
             {"type": "Armour", "class": "Light", "level": 2, "desc": "Basic protection armor.", "item_type": "armour",
              "rarity": "common", "weight": 5, "equipment_slots": 2}, 1),
            ("Nano Armour", "other/item2.png",
             {"type": "Armour", "class": "Nano", "level": 4, "desc": "Lightweight, strong armor.",
              "item_type": "armour", "rarity": "epic", "weight": 3, "equipment_slots": 4}, 1),
            ("Power Armour", "other/item2.png",
             {"type": "Armour", "class": "Power", "level": 5, "desc": "Heavy powered armor.", "item_type": "armour",
              "rarity": "legendary", "weight": 10, "equipment_slots": 3}, 1),
            ("Stealth Suit", "other/item2.png",
             {"type": "Armour", "class": "Stealth", "level": 3, "desc": "Cloaking technology armor.",
              "item_type": "armour", "rarity": "rare", "weight": 4, "equipment_slots": 1}, 1),

            # Equipment
            ("Grenade", "other/item.png",
             {"type": "Equipment", "class": "Explosive", "level": 1, "desc": "Standard frag grenade.",
              "item_type": "equipment", "rarity": "common", "weight": 1}, 8),
            ("Medikit", "other/item.png",
             {"type": "Equipment", "class": "Medical", "level": 1, "desc": "Heals wounds in battle.",
              "item_type": "equipment", "rarity": "common", "weight": 2}, 5),
            ("Shield Generator", "other/item.png",
             {"type": "Equipment", "class": "Defensive", "level": 5, "desc": "Projects a protective shield.",
              "item_type": "equipment", "rarity": "legendary", "weight": 6}, 1),
            ("Scanner", "other/item.png",
             {"type": "Equipment", "class": "Tech", "level": 2, "desc": "Motion detection device.",
              "item_type": "equipment", "rarity": "uncommon", "weight": 1}, 3),

            # Other
            ("Alien Artifact", "other/item.png",
             {"type": "Other", "class": "Misc", "level": 1, "desc": "Unknown alien technology.", "item_type": "other",
              "rarity": "rare", "weight": 3}, 2),
            ("Data Chip", "other/item.png",
             {"type": "Other", "class": "Data", "level": 1, "desc": "Contains encrypted data.", "item_type": "other",
              "rarity": "common", "weight": 1}, 15),
        ]

    @staticmethod
    def get_equipment_slots():
        return [
            {"name": "Armour", "type": ItemType.ARMOUR, "position": (20, 7), "color_adjust": (0, 0, 0.05)},  # Blue tint
            {"name": "Weapon", "type": ItemType.WEAPON, "position": (28, 7), "color_adjust": (0.05, 0, 0)},  # Red tint
            {"name": "Equipment 1", "type": ItemType.EQUIPMENT, "position": (21, 13), "color_adjust": (0, 0.05, 0)},
            # Green tint
            {"name": "Equipment 2", "type": ItemType.EQUIPMENT, "position": (21, 18), "color_adjust": (0, 0.05, 0)},
            # Green tint
            {"name": "Equipment 3", "type": ItemType.EQUIPMENT, "position": (27, 13), "color_adjust": (0, 0.05, 0)},
            # Green tint
            {"name": "Equipment 4", "type": ItemType.EQUIPMENT, "position": (27, 18), "color_adjust": (0, 0.05, 0)},
            # Green tint
        ]


# Enhanced Item class with proper attributes and drag/drop support
class InventoryItem:
    def __init__(self, name, icon_path, properties=None, item_type=ItemType.OTHER, rarity=ItemRarity.COMMON,
                 stackable=False, max_stack=1, item_id=None, weight=1):
        self.name = name
        self.icon_path = icon_path or 'other/item.png'
        self.properties = properties or {}
        self.item_type = item_type
        self.rarity = rarity
        self.stackable = stackable
        self.max_stack = max_stack
        self.id = item_id or f"{name}_{hash(name) % 10000}"
        self.weight = weight

        # Extract description from properties if available
        self.description = self.properties.get('desc', f"A {self.item_type.value}")

    def get_pixmap(self, size=64):
        # Use Qt.FastTransformation for crisp scaling without blurring
        return QPixmap(self.icon_path).scaled(size, size, Qt.KeepAspectRatio, Qt.FastTransformation)

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
            'description': self.description,
            'weight': self.weight
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
            item_id=data.get('id'),
            weight=data.get('weight', 1)
        )


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


# Global references
item_list_widget_global = None
equipment_slots_global = []
weight_label_global = None


def update_weight_display():
    """Update the weight display label"""
    global equipment_slots_global, weight_label_global

    if not weight_label_global or not equipment_slots_global:
        return

    total_weight = 0
    for slot in equipment_slots_global:
        if slot.item:
            total_weight += slot.item.weight

    weight_label_global.setText(f"Weight: {total_weight}")


# Top panel with grid-aligned buttons
def create_top_panel():
    from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QFrame, QLabel, QHBoxLayout, QVBoxLayout, \
        QButtonGroup
    from PySide6.QtGui import QFont
    from PySide6.QtCore import Qt
    global item_list_widget_global, equipment_slots_global, weight_label_global

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
    for unit_type in GameData.get_unit_types():
        filter_combo.addItem(QIcon(QPixmap(unit_type["icon"]).scaled(32, 32)), unit_type["name"])
    filter_combo.setStyleSheet(XcomStyle.combobox())
    unit_list_layout.addWidget(filter_combo)

    unit_list_widget = ItemListWidget(unit_list_groupbox)
    for name, icon_path, info in GameData.get_units():
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
    for category in GameData.get_item_categories():
        item_filter_combo.addItem(QIcon(QPixmap(category["icon"]).scaled(32, 32)), category["name"])
    item_filter_combo.setStyleSheet(XcomStyle.combobox())
    item_list_layout.addWidget(item_filter_combo)

    item_list_widget = ItemListWidget(item_list)
    item_list_widget_global = item_list_widget  # Store global reference

    # Initialize with item counts
    for name, icon_path, info, count in GameData.get_items():
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

    # Initialize equipment slot states (default 2 equipment slots enabled)
    update_equipment_slot_states(2)

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


def update_equipment_slot_states(enabled_count):
    """Enable/disable equipment slots based on armor"""
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


class EquipmentSlotWidget(QWidget):
    def __init__(self, slot_name, parent=None, label_text=None, slot_type=None):
        super().__init__(parent)
        self.slot_name = slot_name
        self.slot_type = slot_type  # ItemType enum value
        self.item = None  # InventoryItem or None
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

    def move(self, x, y):
        super().move(x, y)
        # Position label above the slot
        if hasattr(self, 'label'):
            self.label.move(x, y - px(GRID // 2) - 2)

    def set_background_color(self, color):
        self._bg_color = color
        self.update()

    def set_border_color(self, color):
        self._border_color = color
        self._original_border_color = color
        self.update()

    def can_accept_item(self, item: InventoryItem) -> bool:
        """Check if this slot can accept the given item"""
        if not self.enabled:
            return False

        if self.slot_type and item.item_type != self.slot_type:
            return False

        # Only allow one item per slot - no stacking
        return self.item is None

    def add_item(self, item: InventoryItem) -> bool:
        """Add an item to this slot"""
        if not self.can_accept_item(item):
            return False

        self.item = item
        self.update()

        # Update equipment slots if this is armor
        if self.slot_type == ItemType.ARMOUR:
            equipment_slots = item.properties.get('equipment_slots', 2)
            update_equipment_slot_states(equipment_slots)

        # Update weight display
        update_weight_display()
        return True

    def remove_item(self) -> Optional[InventoryItem]:
        """Remove item from this slot"""
        if self.item is None:
            return None

        item = self.item
        was_armor = (self.slot_type == ItemType.ARMOUR)
        self.item = None
        self.update()

        # Reset equipment slots if armor was removed
        if was_armor:
            update_equipment_slot_states(2)  # Default 2 slots

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

        # Draw icon (centered in slot area) - maintain size during drag
        slot_rect = QRect(self._border_width * 2, self._border_width * 2,
                          w - 4 * self._border_width,
                          h - 4 * self._border_width)

        if self.item:
            pixmap = self.item.get_pixmap(min(slot_rect.width(), slot_rect.height()) - px(8))
            icon_x = slot_rect.x() + (slot_rect.width() - pixmap.width()) // 2
            icon_y = slot_rect.y() + (slot_rect.height() - pixmap.height()) // 2
            painter.drawPixmap(icon_x, icon_y, pixmap)
        else:
            # Draw a subtle placeholder (dashed line square)
            pen = QPen(QColor(self._border_color))
            pen.setStyle(Qt.DashLine)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(slot_rect.adjusted(px(4), px(4), -px(4), -px(4)))

    def dragEnterEvent(self, event: QDragEnterEvent):
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
                    # Visual feedback - keep same border width, just change color
                    self._border_color = XcomTheme.ACCENT_GREEN
                    self.update()
                else:
                    event.ignore()
                    # Visual feedback - keep same border width, just change color
                    self._border_color = XcomTheme.ACCENT_RED
                    self.update()
            except Exception as e:
                print(f"Drag enter error: {e}")
                event.ignore()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        # Restore original border color
        self._border_color = self._original_border_color
        self.update()

    def dropEvent(self, event: QDropEvent):
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
                    if old_item and item_list_widget_global:
                        item_list_widget_global.add_item_to_inventory(old_item, 1)

                self.add_item(item)
                event.acceptProposedAction()
            else:
                event.ignore()
        except Exception as e:
            print(f"Drop error: {e}")
            event.ignore()

        # Restore original border color
        self._border_color = self._original_border_color
        self.update()

    def mousePressEvent(self, event: QMouseEvent):
        if self.item and self.enabled:
            if event.button() == Qt.MouseButton.LeftButton:
                self.start_drag()
            elif event.button() == Qt.MouseButton.RightButton:
                # Right click - move item back to inventory
                self.move_to_inventory()
        else:
            super().mousePressEvent(event)

    def move_to_inventory(self):
        """Move item from slot to inventory (right-click functionality)"""
        if self.item and item_list_widget_global:
            item = self.remove_item()
            item_list_widget_global.add_item_to_inventory(item, 1)

    def start_drag(self):
        """Start dragging this slot's item"""
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.item_info = {}
        self.item_counts = {}  # Track item quantities
        self.all_items = []  # Store all items for filtering
        self.current_filter = "All"
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setMouseTracking(True)
        self.setDragDropMode(QAbstractItemView.DragDrop)  # Allow both drag and drop

    def addItemWithInfo(self, item, info_dict, count=1):
        """Add an item with associated information and count to the list"""
        # Normalize the info dictionary and ensure weight is included
        if 'icon_path' not in info_dict and hasattr(item, 'icon'):
            icon = item.sprite()
            if not icon.isNull():
                info_dict['icon_path'] = 'other/item.png'

        # Ensure weight is set
        if 'weight' not in info_dict:
            info_dict['weight'] = 1

        # Extract base name (remove count if present)
        base_name = item.text().split(' (')[0]

        # Store in all_items for filtering
        self.all_items.append({
            'name': base_name,
            'icon': item.sprite(),
            'info': info_dict,
            'count': count
        })

        self.addItem(item)
        self.item_info[base_name] = info_dict
        self.item_counts[base_name] = count

        # Sort items after adding
        self.sort_items()

    def sort_items(self):
        """Sort items by category then by name"""
        category_order = {"armour": 0, "weapon": 1, "equipment": 2, "other": 3}

        # Sort all_items
        self.all_items.sort(key=lambda x: (
            category_order.get(x['info'].get('item_type', 'other'), 3),
            x['name']
        ))

        # Reapply current filter to refresh display
        self.filter_items(self.current_filter)

    def filter_items(self, category):
        """Filter items based on selected category"""
        self.current_filter = category
        self.clear()
        self.item_info.clear()
        self.item_counts.clear()

        for item_data in self.all_items:
            base_name = item_data['name']
            info = item_data['info']
            count = item_data['count']

            # Check if item should be shown based on filter
            should_show = False
            if category == "All":
                should_show = True
            else:
                item_type = info.get('item_type', 'other')
                if category.lower() == item_type:
                    should_show = True

            if should_show:
                # Create new list item with proper icon
                new_item = QListWidgetItem(item_data['icon'], f"{base_name} ({count})")
                self.addItem(new_item)
                self.item_info[base_name] = info
                self.item_counts[base_name] = count

    def add_item_to_inventory(self, item: InventoryItem, count: int = 1):
        """Add an item back to the inventory list"""
        base_name = item.name

        # Update all_items list
        found_in_all = False
        for item_data in self.all_items:
            if item_data['name'] == base_name:
                item_data['count'] += count
                found_in_all = True
                break

        if not found_in_all:
            # Add to all_items
            self.all_items.append({
                'name': base_name,
                'icon': QIcon(QPixmap(item.icon_path).scaled(32, 32, Qt.KeepAspectRatio, Qt.FastTransformation)),
                'info': item.properties,
                'count': count
            })

        # Check if item already exists in current filtered view
        if base_name in self.item_counts:
            # Update existing item count
            self.item_counts[base_name] += count
            self.update_item_display(base_name)
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

                # Create new list item with proper icon scaling
                new_item = QListWidgetItem(
                    QIcon(QPixmap(item.icon_path).scaled(32, 32, Qt.KeepAspectRatio, Qt.FastTransformation)),
                    f"{base_name} ({count})"
                )
                self.addItem(new_item)

        # Sort items after adding
        self.sort_items()

    def update_item_display(self, base_name):
        """Update the display text for an item with its current count"""
        for i in range(self.count()):
            item = self.item(i)
            if item.text().split(' (')[0] == base_name:
                count = self.item_counts[base_name]
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
            name=base_name,  # Use base name without count
            icon_path=icon_path,
            properties=info,
            item_type=item_type,
            rarity=rarity,
            stackable=info.get('stackable', False),
            max_stack=info.get('max_stack', 1),
            weight=info.get('weight', 1)
        )

    def auto_equip_item(self, item: InventoryItem):
        """Automatically equip item to appropriate slot (RMB functionality)"""
        global equipment_slots_global

        if not equipment_slots_global:
            return False

        # Find appropriate slot
        target_slot = None

        if item.item_type == ItemType.ARMOUR:
            # Find armour slot
            for slot in equipment_slots_global:
                if slot.slot_type == ItemType.ARMOUR and slot.item is None:
                    target_slot = slot
                    break
        elif item.item_type == ItemType.WEAPON:
            # Find weapon slot
            for slot in equipment_slots_global:
                if slot.slot_type == ItemType.WEAPON and slot.item is None:
                    target_slot = slot
                    break
        elif item.item_type == ItemType.EQUIPMENT:
            # Find first available equipment slot
            for slot in equipment_slots_global:
                if slot.slot_type == ItemType.EQUIPMENT and slot.item is None and slot.enabled:
                    target_slot = slot
                    break

        if target_slot:
            target_slot.add_item(item)
            return True

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
        if event.button() == Qt.LeftButton:  # Only LMB for drag
            self.drag_start_position = event.position().toPoint()
        elif event.button() == Qt.RightButton:  # RMB for auto-equip
            current_item = self.currentItem()
            if current_item:
                item_data = self.getItemData(current_item)
                if item_data and self.item_counts.get(item_data.name, 0) > 0:
                    if self.auto_equip_item(item_data):
                        # Successfully equipped, remove from inventory
                        self.remove_item_from_inventory(item_data.name, 1)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):  # Only LMB for drag
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
    win.setWindowTitle("XCOM UI Theme Demo - Enhanced Inventory System v2")
    win.setFixedSize(SCALED_WIDTH, SCALED_HEIGHT)
    top_panel = create_top_panel()
    win.setCentralWidget(top_panel)
    win.show()
    sys.exit(app.exec())