"""
Test suite for engine.item.item_weapon (TItemWeapon)
Covers initialization and attribute defaults using pytest.
"""
import pytest
from engine.item.item_weapon import TItemWeapon
from unittest.mock import patch, MagicMock

class DummyWeaponType:
    def __init__(self):
        self.name = 'Plasma Rifle'
        self.sprite = 'plasma.png'
        self.weight = 6
        self.pid = 'plasma_rifle'
        self.category = 1
        self.unit_ammo = 10
        self.unit_action_point = 2
        self.unit_range = 30
        self.unit_accuracy = 90
        self.unit_shots = 1
        self.unit_damage = 40
        self.unit_rearm_cost = 3
        self.unit_modes = {'snap': MagicMock(apply=lambda x: {'ap_cost': 2, 'range': 30, 'accuracy': 90, 'shots': 1, 'damage': 40})}
        self.unit_stats = {'accuracy': 3}

class DummyGame:
    def __init__(self):
        self.mod = MagicMock()
        self.mod.items = {'plasma_rifle': DummyWeaponType()}

@patch('engine.item.item.TGame', new=DummyGame)
def test_weapon_init_and_modes():
    weapon = TItemWeapon('plasma_rifle')
    assert weapon.active
    assert weapon.ammo == 10
    assert weapon.current_mode == 'snap'
    assert weapon.get_mode_params('snap')['damage'] == 40

@patch('engine.item.item.TGame', new=DummyGame)
def test_set_mode():
    weapon = TItemWeapon('plasma_rifle')
    assert weapon.set_mode('snap')
    assert weapon.current_mode == 'snap'
    assert not weapon.set_mode('invalid')

@patch('engine.item.item.TGame', new=DummyGame)
def test_ammo_and_rearm():
    weapon = TItemWeapon('plasma_rifle')
    weapon.ammo = 5
    assert weapon.ammo_needed() == 5
    assert weapon.get_rearm_cost() == 15

@patch('engine.item.item.TGame', new=DummyGame)
def test_can_fire_and_fire():
    weapon = TItemWeapon('plasma_rifle')
    weapon.ammo = 2
    assert weapon.can_fire(current_ap=2)
    assert weapon.fire()
    assert weapon.ammo == 1
    weapon.ammo = 0
    assert not weapon.can_fire(current_ap=2)
    assert not weapon.fire()

@patch('engine.item.item.TGame', new=DummyGame)
def test_getters():
    weapon = TItemWeapon('plasma_rifle')
    assert weapon.get_shots() == 1
    assert weapon.get_range() == 30
    assert weapon.get_accuracy() == 90
    assert weapon.get_damage() == 40
    assert weapon.get_ap_cost() == 2
    assert weapon.get_stat_modifiers() == {'accuracy': 3}

def test_init_defaults(weapon):
    """Test initialization and attribute values from item type."""
    assert weapon.name == 'Laser Rifle'
    assert weapon.sprite == 'laser_rifle.png'
    assert weapon.weight == 3
    assert weapon.ammo == 6
    assert weapon.active is True
    assert weapon.current_mode == 'snap'
    assert isinstance(weapon.mode_params, dict)

