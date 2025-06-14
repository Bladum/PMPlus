"""
Test suite for engine.unit.unit_inv_manager (InventoryTemplate, TUnitInventoryManager)
Covers initialization, to_dict, and from_dict methods using pytest.
"""
import pytest
from engine.unit.unit_inv_manager import InventoryTemplate
from unittest.mock import MagicMock
from unit.unit_inv_manager import TUnitInventoryManager

@pytest.fixture
def template():
    equipment_data = {'slot1': {'id': 'rifle', 'ammo': 5}}
    return InventoryTemplate('Alpha', equipment_data)

def test_init_defaults(template):
    """Test initialization and attribute values."""
    assert template.name == 'Alpha'
    assert template.equipment_data == {'slot1': {'id': 'rifle', 'ammo': 5}}

def test_to_dict(template):
    """Test to_dict returns correct dictionary."""
    d = template.to_dict()
    assert d['name'] == 'Alpha'
    assert d['equipment_data'] == {'slot1': {'id': 'rifle', 'ammo': 5}}

def test_from_dict():
    """Test from_dict creates a template with correct attributes."""
    data = {
        'name': 'Bravo',
        'equipment_data': {'slot2': {'id': 'pistol', 'ammo': 2}}
    }
    t = InventoryTemplate.from_dict(data)
    assert t.name == 'Bravo'
    assert t.equipment_data == {'slot2': {'id': 'pistol', 'ammo': 2}}

class DummyItem:
    def __init__(self, item_type='equipment', weight=1, stat_modifiers=None):
        self.item_type = item_type
        self.weight = weight
        self.stat_modifiers = stat_modifiers or {}
        self.to_dict = lambda: {'item_type': self.item_type, 'weight': self.weight}

class TestTUnitInventoryManager:
    def test_init_and_slots(self):
        mgr = TUnitInventoryManager()
        assert 'Armor' in mgr.equipment_slots
        assert 'Weapon' in mgr.equipment_slots
        assert isinstance(mgr.available_slots, set)

    def test_equip_and_unequip(self):
        mgr = TUnitInventoryManager()
        item = DummyItem('armor')
        assert mgr.equip_item('Armor', item)
        assert mgr.equipment_slots['Armor'] == item
        assert mgr.unequip_item('Armor') == item
        assert mgr.equipment_slots['Armor'] is None

    def test_get_total_weight(self):
        mgr = TUnitInventoryManager()
        item = DummyItem('armor', weight=5)
        mgr.equip_item('Armor', item)
        assert mgr.get_total_weight() >= 5

    def test_template_save_load(self):
        mgr = TUnitInventoryManager()
        item = DummyItem('armor')
        mgr.equip_item('Armor', item)
        template = mgr.save_template()
        mgr.unequip_item('Armor')
        mgr.load_template(template)
        assert mgr.equipment_slots['Armor'] is not None

    def test_auto_equip(self):
        mgr = TUnitInventoryManager()
        item = DummyItem('armor')
        success, slot = mgr.auto_equip(item)
        assert success and slot == 'Armor'

