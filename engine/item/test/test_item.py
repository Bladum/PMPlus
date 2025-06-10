import pytest
from engine.item.item import TItem
from unittest.mock import MagicMock, patch

class DummyItemType:
    def __init__(self):
        self.name = 'TestItem'
        self.sprite = 'test_sprite.png'
        self.weight = 5
        self.pid = 'test_itemtype'
        self.category = 1

class DummyGame:
    def __init__(self):
        self.mod = MagicMock()
        self.mod.items = {'test_itemtype': DummyItemType()}

@patch('engine.item.item.TGame', new=DummyGame)
def test_item_init():
    item = TItem('test_itemtype')
    assert item.name == 'TestItem'
    assert item.sprite == 'test_sprite.png'
    assert item.weight == 5
    assert item.item_type.name == 'TestItem'
    assert isinstance(item.id, str)

@patch('engine.item.item.TGame', new=DummyGame)
def test_item_to_dict_and_from_dict():
    item = TItem('test_itemtype')
    d = item.to_dict()
    assert d['id'] == item.id
    assert d['item_type_id'] == 'test_itemtype'
    assert isinstance(d['properties'], dict)
    # from_dict
    registry = {'test_itemtype': DummyItemType()}
    item2 = TItem.from_dict({'id': 'abc', 'item_type_id': 'test_itemtype', 'properties': {'foo': 1}}, registry)
    assert item2.id == 'abc'
    assert item2.properties['foo'] == 1

@patch('engine.item.item.TGame', new=DummyGame)
def test_item_equality_and_hash():
    item1 = TItem('test_itemtype', 'id1')
    item2 = TItem('test_itemtype', 'id1')
    item3 = TItem('test_itemtype', 'id2')
    assert item1 == item2
    assert item1 != item3
    assert hash(item1) == hash(item2)
    assert hash(item1) != hash(item3)

@patch('engine.item.item.TGame', new=DummyGame)
def test_item_str_and_repr():
    item = TItem('test_itemtype', 'abcdef123456')
    s = str(item)
    r = repr(item)
    assert 'TestItem' in s
    assert 'abcdef12' in s
    assert 'TItem' in r
    assert 'test_itemtype' in r

@patch('engine.item.item.TGame', new=DummyGame)
def test_item_get_category():
    item = TItem('test_itemtype')
    assert item.get_category() == 1

@patch('engine.item.item.TGame', new=DummyGame)
def test_item_get_display_name():
    item = TItem('test_itemtype')
    assert item.get_display_name() == 'TestItem'

@patch('engine.item.item.TGame', new=DummyGame)
def test_item_get_compatible_slots():
    item = TItem('test_itemtype')
    item.properties['compatible_slots'] = ['slot1', 'slot2']
    assert item.get_compatible_slots() == ['slot1', 'slot2']

