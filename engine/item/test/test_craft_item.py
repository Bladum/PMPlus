"""
Test suite for engine.item.craft_item (TCraftItem)
Covers class existence and instantiation using pytest.
"""
import pytest
from engine.item.craft_item import TCraftItem

def test_craft_item_class_exists():
    """Test that TCraftItem can be instantiated."""
    item = TCraftItem()
    assert isinstance(item, TCraftItem)
