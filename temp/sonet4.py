import sys
from dataclasses import dataclass
from enums import Enum
from typing import Optional, Dict, Any
import json

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QFrame, QToolTip
)
from PySide6.QtCore import Qt, QMimeData, QPoint, Signal
from PySide6.QtGui import QDrag, QPainter, QPixmap, QPen, QBrush, QColor


class ItemType(Enum):
    WEAPON = "weapon"
    ARMOR = "armor"
    HELMET = "helmet"
    BOOTS = "boots"
    CONSUMABLE = "consumable"
    MISC = "misc"


class ItemRarity(Enum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


@dataclass
class Item:
    id: str
    name: str
    description: str
    item_type: ItemType
    rarity: ItemRarity
    icon_color: str = "#8B4513"  # Default brown
    stackable: bool = False
    max_stack: int = 1

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'item_type': self.item_type.value,
            'rarity': self.rarity.value,
            'icon_color': self.icon_color,
            'stackable': self.stackable,
            'max_stack': self.max_stack
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Item':
        return cls(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            item_type=ItemType(data['item_type']),
            rarity=ItemRarity(data['rarity']),
            icon_color=data.get('icon_color', '#8B4513'),
            stackable=data.get('stackable', False),
            max_stack=data.get('max_stack', 1)
        )


class InventorySlot(QFrame):
    itemChanged = Signal(object)  # Emits the item or None

    def __init__(self, slot_type: Optional[ItemType] = None, parent=None):
        super().__init__(parent)
        self.slot_type = slot_type  # None means accepts any item
        self.item: Optional[Item] = None
        self.stack_size = 0
        self.is_equipment_slot = slot_type is not None

        self.setFixedSize(60, 60)
        self.setFrameStyle(QFrame.Box)
        self.setLineWidth(2)
        self.setAcceptDrops(True)

        # Layout for the slot
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(2, 2, 2, 2)

        self.item_label = QLabel()
        self.item_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.item_label)

        self.stack_label = QLabel()
        self.stack_label.setAlignment(Qt.AlignBottom | Qt.AlignRight)
        self.stack_label.setStyleSheet("font-size: 10px; color: white; font-weight: bold;")
        self.layout.addWidget(self.stack_label)

        self.update_appearance()

    def update_appearance(self):
        if self.item:
            # Set background color based on rarity
            rarity_colors = {
                ItemRarity.COMMON: "#FFFFFF",
                ItemRarity.UNCOMMON: "#1EFF00",
                ItemRarity.RARE: "#0070DD",
                ItemRarity.EPIC: "#A335EE",
                ItemRarity.LEGENDARY: "#FF8000"
            }

            color = rarity_colors.get(self.item.rarity, "#FFFFFF")
            self.setStyleSheet(f"""
                QFrame {{
                    background-color: {self.item.icon_color};
                    border: 2px solid {color};
                }}
            """)

            # Set item name as text
            self.item_label.setText(self.item.name[:8])  # Truncate long names
            self.item_label.setStyleSheet("color: white; font-weight: bold; font-size: 9px;")

            # Show stack size if stackable
            if self.item.stackable and self.stack_size > 1:
                self.stack_label.setText(str(self.stack_size))
            else:
                self.stack_label.setText("")
        else:
            # Empty slot
            if self.is_equipment_slot:
                self.setStyleSheet("""
                    QFrame {
                        background-color: #2D2D2D;
                        border: 2px dashed #666666;
                    }
                """)
                self.item_label.setText(self.slot_type.value.upper()[:4])
                self.item_label.setStyleSheet("color: #666666; font-size: 8px;")
            else:
                self.setStyleSheet("""
                    QFrame {
                        background-color: #1E1E1E;
                        border: 2px solid #444444;
                    }
                """)
                self.item_label.setText("")

            self.stack_label.setText("")

    def can_accept_item(self, item: Item) -> bool:
        if self.slot_type and item.item_type != self.slot_type:
            return False

        if self.item is None:
            return True

        # Check if items can stack
        if (self.item.id == item.id and
                self.item.stackable and
                self.stack_size < self.item.max_stack):
            return True

        return False

    def add_item(self, item: Item, quantity: int = 1) -> bool:
        if not self.can_accept_item(item):
            return False

        if self.item is None:
            self.item = item
            self.stack_size = quantity
        elif self.item.id == item.id and self.item.stackable:
            self.stack_size += quantity
            if self.stack_size > self.item.max_stack:
                self.stack_size = self.item.max_stack
        else:
            return False

        self.update_appearance()
        self.itemChanged.emit(self.item)
        return True

    def remove_item(self, quantity: int = None) -> Optional[Item]:
        if self.item is None:
            return None

        if quantity is None or quantity >= self.stack_size:
            # Remove all
            item = self.item
            self.item = None
            self.stack_size = 0
            self.update_appearance()
            self.itemChanged.emit(None)
            return item
        else:
            # Remove partial stack
            self.stack_size -= quantity
            if self.stack_size <= 0:
                item = self.item
                self.item = None
                self.stack_size = 0
                self.update_appearance()
                self.itemChanged.emit(None)
                return item
            else:
                self.update_appearance()
                return self.item

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.item:
            self.start_drag()

    def start_drag(self):
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
        pixmap = QPixmap(60, 60)
        pixmap.fill(QColor(self.item.icon_color))

        painter = QPainter(pixmap)
        painter.setPen(QPen(Qt.white, 2))
        painter.drawText(pixmap.rect(), Qt.AlignCenter, self.item.name[:4])
        painter.end()

        drag.setPixmap(pixmap)
        drag.setHotSpot(QPoint(30, 30))

        # Execute drag
        result = drag.exec(Qt.MoveAction)
        if result == Qt.MoveAction:
            # Item was moved, remove from this slot
            self.remove_item()

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            try:
                data = json.loads(event.mimeData().text())
                item = Item.from_dict(data['item'])
                source_slot_id = data.get('source_slot')

                # Don't accept drops from the same slot
                if source_slot_id == id(self):
                    event.ignore()
                    return

                if self.can_accept_item(item):
                    event.acceptProposedAction()
                    self.setStyleSheet(self.styleSheet() + "border: 3px solid #00FF00;")
                else:
                    event.ignore()
                    self.setStyleSheet(self.styleSheet() + "border: 3px solid #FF0000;")
            except:
                event.ignore()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.update_appearance()

    def dropEvent(self, event):
        try:
            data = json.loads(event.mimeData().text())
            item = Item.from_dict(data['item'])
            stack_size = data['stack_size']

            if self.can_accept_item(item):
                # Handle item swapping or stacking
                if self.item and self.item.id != item.id:
                    # TODO: Implement item swapping
                    pass

                self.add_item(item, stack_size)
                event.acceptProposedAction()
            else:
                event.ignore()
        except:
            event.ignore()

        self.update_appearance()

    def enterEvent(self, event):
        if self.item:
            tooltip_text = f"<b>{self.item.name}</b><br>"
            tooltip_text += f"<i>{self.item.rarity.value.title()}</i><br>"
            tooltip_text += f"{self.item.description}"
            if self.item.stackable and self.stack_size > 1:
                tooltip_text += f"<br>Stack: {self.stack_size}/{self.item.max_stack}"

            QToolTip.showText(self.mapToGlobal(QPoint(0, 0)), tooltip_text)


class InventoryWidget(QWidget):
    def __init__(self, rows: int = 6, cols: int = 8, parent=None):
        super().__init__(parent)
        self.rows = rows
        self.cols = cols
        self.slots = []

        self.setup_ui()
        self.create_sample_items()

    def setup_ui(self):
        layout = QGridLayout(self)
        layout.setSpacing(2)

        # Create inventory slots
        for row in range(self.rows):
            slot_row = []
            for col in range(self.cols):
                slot = InventorySlot()
                layout.addWidget(slot, row, col)
                slot_row.append(slot)
            self.slots.append(slot_row)

    def create_sample_items(self):
        # Create some sample items
        sample_items = [
            Item("sword1", "Iron Sword", "A sturdy iron sword", ItemType.WEAPON, ItemRarity.COMMON, "#C0C0C0"),
            Item("potion1", "Health Potion", "Restores 50 HP", ItemType.CONSUMABLE, ItemRarity.COMMON, "#FF0000", True,
                 10),
            Item("armor1", "Steel Armor", "Heavy steel protection", ItemType.ARMOR, ItemRarity.UNCOMMON, "#708090"),
            Item("helmet1", "Magic Helm", "Increases mana", ItemType.HELMET, ItemRarity.RARE, "#4B0082"),
            Item("boots1", "Swift Boots", "Increases movement speed", ItemType.BOOTS, ItemRarity.EPIC, "#8B4513"),
        ]

        # Add items to random slots
        import random
        for item in sample_items:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if not self.slots[row][col].item:
                if item.stackable:
                    self.slots[row][col].add_item(item, random.randint(1, 5))
                else:
                    self.slots[row][col].add_item(item)


class EquipmentWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.equipment_slots = {}
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Title
        title = QLabel("Equipment")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 14px; font-weight: bold; color: white;")
        layout.addWidget(title)

        # Equipment slots layout
        equipment_layout = QGridLayout()

        # Define equipment slot positions
        slot_positions = {
            ItemType.HELMET: (0, 1),
            ItemType.ARMOR: (1, 1),
            ItemType.WEAPON: (1, 0),
            ItemType.BOOTS: (2, 1),
        }

        for item_type, (row, col) in slot_positions.items():
            slot = InventorySlot(item_type)
            self.equipment_slots[item_type] = slot
            equipment_layout.addWidget(slot, row, col)

        layout.addLayout(equipment_layout)


class InventorySystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RPG Inventory System")
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1E1E1E;
                color: white;
            }
        """)

        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        # Equipment panel
        self.equipment_widget = EquipmentWidget()
        main_layout.addWidget(self.equipment_widget)

        # Inventory panel
        inventory_container = QWidget()
        inventory_layout = QVBoxLayout(inventory_container)

        inventory_title = QLabel("Inventory")
        inventory_title.setAlignment(Qt.AlignCenter)
        inventory_title.setStyleSheet("font-size: 14px; font-weight: bold; color: white;")
        inventory_layout.addWidget(inventory_title)

        self.inventory_widget = InventoryWidget()
        inventory_layout.addWidget(self.inventory_widget)

        main_layout.addWidget(inventory_container)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = InventorySystem()
    window.show()

    sys.exit(app.exec())