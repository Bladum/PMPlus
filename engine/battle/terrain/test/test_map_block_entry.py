import pytest
from engine.battle.terrain.map_block_entry import TMapBlockEntry

def test_map_block_entry_defaults():
    entry = TMapBlockEntry({})
    assert entry.map == ''
    assert entry.size == 1
    assert entry.group == 0
    assert entry.chance == 1
    assert entry.items == {}
    assert entry.units == {}
    assert entry.show is False

def test_map_block_entry_custom():
    data = {'map': 'block1', 'size': 2, 'group': 3, 'chance': 5, 'items': {'item': 1}, 'units': {'unit': 2}, 'show': True}
    entry = TMapBlockEntry(data)
    assert entry.map == 'block1'
    assert entry.size == 2
    assert entry.group == 3
    assert entry.chance == 5
    assert entry.items == {'item': 1}
    assert entry.units == {'unit': 2}
    assert entry.show is True

