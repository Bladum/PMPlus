import pytest
from engine.item.item_craft import TCraftItem
from unittest.mock import patch, MagicMock

class DummyCraftType:
    def __init__(self):
        self.name = 'CraftWeapon'
        self.sprite = 'craft.png'
        self.weight = 15
        self.pid = 'craft_type'
        self.category = 3
        self.craft_ammo = 6
        self.craft_rearm_cost = 2
        self.craft_reload_time = 3
        self.craft_rearm_time = 4

class DummyGame:
    def __init__(self):
        self.mod = MagicMock()
        self.mod.items = {'craft_type': DummyCraftType()}

@patch('engine.item.item.TGame', new=DummyGame)
def test_craft_item_init():
    item = TCraftItem('craft_type')
    assert item.maintenance_status == 100
    assert item.active
    assert item.ammo == 0
    assert item.hardpoint_type == 'WEAPON'

@patch('engine.item.item.TGame', new=DummyGame)
def test_ammo_needed_and_rearm_cost():
    item = TCraftItem('craft_type')
    item.ammo = 2
    assert item.ammo_needed() == 4
    assert item.get_rearm_cost() == 8

@patch('engine.item.item.TGame', new=DummyGame)
def test_reload_and_rearm():
    item = TCraftItem('craft_type')
    item.start_reload()
    assert item.reload_time_left == 3
    for _ in range(3):
        item.tick_reload()
    assert item.reload_time_left == 0
    item.ammo = 0
    item.start_rearm()
    assert item.rearm_time_left == 4
    for _ in range(4):
        item.tick_rearm()
    assert item.rearm_time_left == 0
    assert item.ammo == 6

@patch('engine.item.item.TGame', new=DummyGame)
def test_activation():
    item = TCraftItem('craft_type')
    item.deactivate()
    assert not item.is_active()
    item.activate()
    assert item.is_active()

@patch('engine.item.item.TGame', new=DummyGame)
def test_is_ready():
    item = TCraftItem('craft_type')
    item.ammo = 2
    item.reload_time_left = 0
    item.active = True
    assert item.is_ready()
    item.active = False
    assert not item.is_ready()

@patch('engine.item.item.TGame', new=DummyGame)
def test_get_compatible_hardpoints():
    item = TCraftItem('craft_type')
    assert item.get_compatible_hardpoints() == ['WEAPON']

