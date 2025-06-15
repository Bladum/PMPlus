"""
Test suite for engine.craft.craft_inv_manager (CraftInventoryTemplate, TCraftInventoryManager)
Covers initialization, to_dict, and from_dict methods using pytest.
"""
import pytest
from engine.craft.craft_inv_manager import CraftInventoryTemplate

@pytest.fixture
def template():
    hardpoint_data = {'weapon': {'id': 'laser', 'ammo': 10}}
    cargo_data = {'medkit': {'qty': 2}}
    return CraftInventoryTemplate('Alpha', hardpoint_data, cargo_data)

def test_init_defaults(template):
    """Test initialization and attribute values."""
    assert template.name == 'Alpha'
    assert template.hardpoint_data == {'weapon': {'id': 'laser', 'ammo': 10}}
    assert template.cargo_data == {'medkit': {'qty': 2}}

def test_to_dict(template):
    """Test to_dict returns correct dictionary."""
    d = template.to_dict()
    assert d['name'] == 'Alpha'
    assert d['hardpoint_data'] == {'weapon': {'id': 'laser', 'ammo': 10}}
    assert d['cargo_data'] == {'medkit': {'qty': 2}}

def test_from_dict():
    """Test from_dict creates a template with correct attributes."""
    data = {
        'name': 'Bravo',
        'hardpoint_data': {'cannon': {'id': 'plasma', 'ammo': 5}},
        'cargo_data': {'grenade': {'qty': 3}}
    }
    t = CraftInventoryTemplate.from_dict(data)
    assert t.name == 'Bravo'
    assert t.hardpoint_data == {'cannon': {'id': 'plasma', 'ammo': 5}}
    assert t.cargo_data == {'grenade': {'qty': 3}}
