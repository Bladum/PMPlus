import pytest
from engine.engine.mod import TMod

def test_mod_init():
    mod = TMod({}, '.')
    assert isinstance(mod, TMod)
    assert hasattr(mod, 'mod_data')
    assert hasattr(mod, 'mod_path')
    assert hasattr(mod, 'facilities')
    assert hasattr(mod, 'items')
    assert hasattr(mod, 'units')
    assert hasattr(mod, 'traits')
    assert hasattr(mod, 'campaigns')
    assert hasattr(mod, 'factions')
    assert hasattr(mod, 'starting_base')

def test_load_objects_from_data_empty():
    mod = TMod({}, '.')
    mod.load_objects_from_data()
    # Should not raise

def test_get_equipment_slots():
    slots = TMod.get_equipment_slots()
    assert isinstance(slots, list)
    assert any('name' in slot for slot in slots)

def test_get_unit_categories():
    cats = TMod.get_unit_categories()
    assert isinstance(cats, list)
    assert any('name' in cat for cat in cats)

def test_get_item_categories():
    cats = TMod.get_item_categories()
    assert isinstance(cats, list)
    assert any('name' in cat for cat in cats)

