"""
Test suite for engine.item.item_type (TItemType)
Covers initialization and attribute defaults using pytest.
"""
import pytest
from engine.item.item_type import TItemType
from unittest.mock import patch, MagicMock

class DummyGame:
    def __init__(self):
        self.mod = MagicMock()
        self.mod.weapon_modes = {'snap': MagicMock(apply=lambda x: {'ap_cost': 2, 'range': 10, 'accuracy': 50, 'shots': 1, 'damage': 20})}

@patch('engine.item.item_type.TGame', new=DummyGame)
def test_item_type_init_and_modes():
    data = {
        'name': 'Laser Rifle',
        'category': 1,
        'weight': 4,
        'size': 2,
        'unit_damage': 30,
        'unit_accuracy': 80,
        'unit_range': 25,
        'unit_ammo': 6,
        'unit_shots': 1,
        'unit_action_point': 2,
        'unit_modes': ['snap'],
        'resistance': {'kinetic': 0.5},
        'shield': 10,
        'shield_regen': 2,
        'armour': 5,
        'armour_cover': [1, 2],
        'armour_sight': [3, 4],
        'armour_sense': [5, 6],
        'primary_slots': 1,
        'secondary_slots': 2,
        'craft_ammo': 0,
        'craft_rearm_time': 1,
        'craft_rearm_cost': 0,
        'craft_reload_time': 0,
        'unit_stats': {'accuracy': 2},
        'modes': ['snap']
    }
    t = TItemType('laser_rifle', data)
    assert t.name == 'Laser Rifle'
    assert t.category == 1
    assert t.weight == 4
    assert t.unit_damage == 30
    assert t.armour_shield == 10
    assert t.armour_shield_regen == 2
    assert t.armour_resistance['kinetic'] == 0.5
    assert t.unit_modes['snap']
    assert t.modes['snap']

@patch('engine.item.item_type.TGame', new=DummyGame)
def test_get_mode_parameters():
    data = {'unit_action_point': 2, 'unit_range': 10, 'unit_accuracy': 50, 'unit_shots': 1, 'unit_damage': 20, 'unit_modes': ['snap'], 'modes': ['snap']}
    t = TItemType('laser_rifle', data)
    params = t.get_mode_parameters('snap')
    assert params['ap_cost'] == 2
    assert params['range'] == 10
    assert params['accuracy'] == 50
    assert params['shots'] == 1
    assert params['damage'] == 20

@pytest.fixture
def item_type():
    data = {
        'name': 'Stun Rod',
        'category': 1,
        'description': 'Non-lethal melee weapon',
        'weight': 2,
        'size': 1,
        'pedia': 'pedia_stun_rod',
        'sprite': 'stun_rod.png',
        'sound': 'zap.wav',
        'tech_needed': ['Alien Containment'],
        'unit_damage': 30,
        'unit_damage_type': 'stun',
        'unit_accuracy': 90,
        'unit_range': 1,
        'unit_ammo': 0,
        'unit_shots': 1,
        'unit_action_point': 8,
        'unit_modes': {},
        'armour_shield': 0,
        'armour_shield_regen': 0,
    }
    return TItemType('STUN_ROD', data)

def test_init_defaults(item_type):
    """Test initialization and attribute values from data dict."""
    assert item_type.pid == 'STUN_ROD'
    assert item_type.name == 'Stun Rod'
    assert item_type.category == 1
    assert item_type.description == 'Non-lethal melee weapon'
    assert item_type.weight == 2
    assert item_type.size == 1
    assert item_type.pedia == 'pedia_stun_rod'
    assert item_type.sprite == 'stun_rod.png'
    assert item_type.sound == 'zap.wav'
    assert item_type.tech_needed == ['Alien Containment']
    assert item_type.unit_damage == 30
    assert item_type.unit_damage_type == 'stun'
    assert item_type.unit_accuracy == 90
    assert item_type.unit_range == 1
    assert item_type.unit_ammo == 0
    assert item_type.unit_shots == 1
    assert item_type.unit_action_point == 8
    assert item_type.unit_modes == {}
    assert item_type.armour_shield == 0
    assert item_type.armour_shield_regen == 0

