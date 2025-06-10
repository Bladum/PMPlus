import pytest
from engine.item.item_transfer import TItemTransferManager
from unittest.mock import MagicMock
from PySide6.QtCore import QMimeData, QByteArray, Qt

class DummySlot:
    def __init__(self, compatible_types=None, preferred_types=None):
        self.compatible_types = compatible_types or []
        self.preferred_types = preferred_types or []
        self.allow_self_drop = False
        self.item = None
    def add_item(self, item):
        self.item = item
    def remove_item(self):
        self.item = None

class DummyItem:
    def __init__(self, item_type):
        self.item_type = item_type
    def get_pixmap(self, size):
        class DummyPixmap:
            def rect(self):
                class DummyRect:
                    def center(self):
                        return (0, 0)
                return DummyRect()
            def isNull(self):
                return False
            def scaled(self, *args, **kwargs):
                return self
        return DummyPixmap()

class DummyWidget:
    def __init__(self):
        self.item = None
        self.allow_self_drop = False
    def add_item(self, item):
        self.item = item
    def remove_item(self):
        self.item = None

@pytest.fixture
def manager():
    return TItemTransferManager()

def test_default_validate_compatibility(manager):
    item = DummyItem('typeA')
    slot = DummySlot(['typeA', 'typeB'])
    assert manager._default_validate_compatibility(item, slot)
    item2 = DummyItem('typeC')
    assert not manager._default_validate_compatibility(item2, slot)

def test_can_accept_drop(manager):
    widget = DummyWidget()
    item = DummyItem('typeA')
    manager._current_drag_item = item
    mime = QMimeData()
    mime.setData(manager.MIME_TYPE, QByteArray(b'source1'))
    widget.compatible_types = ['typeA']
    assert manager.can_accept_drop(widget, 'target1', mime)

def test_accept_drop_and_swap(manager):
    source = DummyWidget()
    target = DummyWidget()
    item1 = DummyItem('typeA')
    item2 = DummyItem('typeA')
    source.item = item1
    target.item = item2
    manager._current_drag_item = item1
    manager._source_widget = source
    manager._source_id = 'source1'
    mime = QMimeData()
    mime.setData(manager.MIME_TYPE, QByteArray(b'source1'))
    success, src, tgt = manager.accept_drop(target, 'target1', mime)
    assert success
    assert target.item == item1
    assert source.item == item2

def test_inventory_action_history(manager):
    action = {'type': 'move', 'source': 'A', 'target': 'B', 'item_id': 'id1'}
    manager.record_inventory_action(action)
    assert manager._history[-1] == action
    assert manager.undo()
    assert manager.redo()

def test_get_item_compatibility_report(manager):
    item = DummyItem('typeA')
    slot = DummySlot(['typeA'], ['typeA'])
    report = manager.get_item_compatibility_report(item, slot)
    assert report['compatible']
    assert report['reason'] == ''
    slot2 = DummySlot(['typeB'])
    report2 = manager.get_item_compatibility_report(item, slot2)
    assert not report2['compatible']
    assert 'incompatible' in report2['reason']

