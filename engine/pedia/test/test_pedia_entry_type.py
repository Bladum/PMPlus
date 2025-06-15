"""
Test suite for TPediaEntryType (pedia_entry_type.py).
Covers initialization and attribute defaults.
"""
import pytest
from engine.pedia.pedia_entry_type import TPediaEntryType

def test_pedia_entry_type_init_defaults():
    """Test TPediaEntryType initializes with provided values."""
    t = TPediaEntryType(1, 'Weapons', 'desc', 'icon', 2)
    assert t.type_id == 1
    assert t.name == 'Weapons'
    assert t.description == 'desc'
    assert t.icon == 'icon'
    assert t.order == 2
