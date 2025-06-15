"""
Test suite for engine.enums
Covers enum existence and values using pytest.
"""
import pytest
from engine import enums

def test_eitemcategory_values():
    assert enums.EItemCategory.CRAFT_ITEM.value == "craft_item"
    assert enums.EItemCategory.UNIT_ITEM.value == "unit_armour"
    assert enums.EItemCategory.OTHER.value == "other"
    assert enums.EItemCategory.PRISONER.value == "prisoner"

def test_eunititemcategory_values():
    assert enums.EUnitItemCategory.ARMOR.value == "armor"
    assert enums.EUnitItemCategory.WEAPON.value == "weapon"
    assert enums.EUnitItemCategory.EQUIPMENT.value == "equipment"

def test_ecraftitemcategory_values():
    assert enums.ECraftItemCategory.WEAPON.value == "weapon"
    assert enums.ECraftItemCategory.EQUIPMENT.value == "equipment"
    assert enums.ECraftItemCategory.CARGO.value == "cargo"

def test_themetype_values():
    assert enums.ThemeType.XCOM_DARK.name == "XCOM_DARK"
    assert enums.ThemeType.XCOM_LIGHT.name == "XCOM_LIGHT"
    assert enums.ThemeType.CUSTOM.name == "CUSTOM"

def test_eunittype_values():
    assert enums.EUnitType.SOLDIER.value == "soldier"
    assert enums.EUnitType.TANK.value == "tank"
    assert enums.EUnitType.ROBOT.value == "robot"
    assert enums.EUnitType.PET.value == "pet"
    assert enums.EUnitType.ALIEN.value == "alien"
