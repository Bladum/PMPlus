import pytest
from engine.item.item_armour import TItemArmour
from unittest.mock import patch, MagicMock

class DummyArmourType:
    def __init__(self):
        self.name = 'Armour'
        self.sprite = 'armour.png'
        self.weight = 10
        self.pid = 'armour_type'
        self.category = 2
        self.armour_shield = 20
        self.armour_shield_regen = 5
        self.armour_resistance = {'kinetic': 0.5, 'laser': 1.0}
        self.unit_stats = {'defense': 2}

class DummyGame:
    def __init__(self):
        self.mod = MagicMock()
        self.mod.items = {'armour_type': DummyArmourType()}

@patch('engine.item.item.TGame', new=DummyGame)
def test_armour_init():
    armour = TItemArmour('armour_type')
    assert armour.max_shield == 20
    assert armour.shield_regen == 5
    assert armour.shield == 0

@patch('engine.item.item.TGame', new=DummyGame)
def test_shield_regeneration():
    armour = TItemArmour('armour_type')
    armour.shield = 10
    val = armour.shield_regeneration()
    assert val == 15
    armour.shield = 20
    val = armour.shield_regeneration()
    assert val == 20

@patch('engine.item.item.TGame', new=DummyGame)
def test_is_shield_empty_and_reset():
    armour = TItemArmour('armour_type')
    assert armour.is_shield_empty()
    armour.reset_shield()
    assert armour.shield == 20
    assert not armour.is_shield_empty()

@patch('engine.item.item.TGame', new=DummyGame)
def test_apply_damage():
    armour = TItemArmour('armour_type')
    armour.reset_shield()
    # Damage less than shield
    dmg = armour.apply_damage(5, 'kinetic')
    assert dmg == 0.0
    assert armour.shield == 15
    # Damage more than shield
    armour.shield = 3
    dmg = armour.apply_damage(10, 'kinetic')
    assert dmg == (7 * 0.5)
    assert armour.shield == 0

@patch('engine.item.item.TGame', new=DummyGame)
def test_get_stat_modifiers():
    armour = TItemArmour('armour_type')
    assert armour.get_stat_modifiers() == {'defense': 2}

