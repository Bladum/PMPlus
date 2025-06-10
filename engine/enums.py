from enum import Enum, auto


# Inventory/Base
class EItemCategory(Enum):
    CRAFT_ITEM = "craft_item"
    UNIT_ITEM = "unit_armour"
    OTHER = "other"
    PRISONER = "prisoner"

# Unit Inventory
class EUnitItemCategory(Enum):
    ARMOR = "armor"
    WEAPON = "weapon"
    EQUIPMENT = "equipment"

# Craft Inventory
class ECraftItemCategory(Enum):
    WEAPON = "weapon"
    EQUIPMENT = "equipment"
    CARGO = "cargo"

# Theme/UI
class ThemeType(Enum):
    XCOM_DARK = auto()
    XCOM_LIGHT = auto()
    CUSTOM = auto()

class EUnitType(Enum):
    SOLDIER = "soldier"
    TANK = "tank"
    ROBOT = "robot"
    PET = "pet"
    ALIEN = "alien"

