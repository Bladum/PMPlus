"""
engine/enums.py

This module defines core enumerations for item, unit, craft categories, and theme types.
All enums are used throughout the engine for type safety and clarity.
"""

from enum import Enum, auto


class EItemCategory(Enum):
    """
    Enumeration for item categories in inventory and base management.
    """
    CRAFT_ITEM = "craft_item"
    UNIT_ITEM = "unit_armour"
    OTHER = "other"
    PRISONER = "prisoner"


class EUnitItemCategory(Enum):
    """
    Enumeration for unit inventory item categories.
    """
    ARMOR = "armor"
    WEAPON = "weapon"
    EQUIPMENT = "equipment"


class ECraftItemCategory(Enum):
    """
    Enumeration for craft inventory item categories.
    """
    WEAPON = "weapon"
    EQUIPMENT = "equipment"
    CARGO = "cargo"


class ThemeType(Enum):
    """
    Enumeration for theme/UI types.
    """
    XCOM_DARK = auto()
    XCOM_LIGHT = auto()
    CUSTOM = auto()


class EUnitType(Enum):
    """
    Enumeration for unit types.
    """
    SOLDIER = "soldier"
    TANK = "tank"
    ROBOT = "robot"
    PET = "pet"
    ALIEN = "alien"

