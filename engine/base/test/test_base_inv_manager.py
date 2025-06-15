"""
Test suite for engine.base.base_inv_manager (TBaseInventory)
Covers initialization, attribute defaults, and add_item method using pytest.
"""
import pytest
from engine.base.base_inv_manager import TBaseInventory

class DummyCategory:
    pass

@pytest.fixture
def base_inventory():
    return TBaseInventory(storage_capacity=10, craft_capacity=2)

def test_init_defaults(base_inventory):
    """Test initialization and default attributes."""
    assert base_inventory.items == {}
    assert base_inventory.units == []
    assert base_inventory.crafts == []
    assert base_inventory.item_categories == {}
    assert base_inventory.captures == {}
    assert base_inventory.item_sizes == {}
    assert base_inventory.storage_capacity == 10
    assert base_inventory.craft_capacity == 2

def test_add_item_new_and_existing(base_inventory):
    """Test adding a new item and increasing its quantity."""
    assert base_inventory.add_item('item1', 2.0) is True
    assert base_inventory.items['item1'] == 2.0
    # Add more of the same item
    assert base_inventory.add_item('item1', 3.0) is True
    assert base_inventory.items['item1'] == 5.0

def test_add_item_over_capacity(base_inventory):
    """Test that adding items over storage capacity fails."""
    base_inventory.item_sizes['big_item'] = 11.0
    assert base_inventory.add_item('big_item', 1.0) is False
