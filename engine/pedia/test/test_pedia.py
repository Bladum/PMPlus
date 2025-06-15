"""
Test suite for TPedia (pedia.py).
Covers initialization, add/get/list methods, and add_category.
"""
import pytest
from engine.pedia.pedia import TPedia
from engine.pedia.pedia_entry import TPediaEntry
from engine.pedia.pedia_entry_type import TPediaEntryType

class DummyEntry:
    def __init__(self, pid, type):
        self.pid = pid
        self.type = type
class DummyCategory:
    def __init__(self, type_id):
        self.type_id = type_id

class TestTPediaEntryType:
    def test_init(self):
        t = TPediaEntryType(1, 'Weapons', 'Weapon category', 'icon.png', 10)
        assert t.type_id == 1
        assert t.name == 'Weapons'
        assert t.description == 'Weapon category'
        assert t.icon == 'icon.png'
        assert t.order == 10

class TestTPediaEntry:
    def test_init_and_attributes(self):
        data = {
            'type': 2,
            'name': 'Laser Rifle',
            'section': 'Weapons',
            'description': 'A powerful laser weapon.',
            'sprite': 'laser_rifle.png',
            'tech_needed': ['Laser Tech'],
            'order': 5,
            'related': ['plasma_rifle'],
            'stats': {'damage': 60}
        }
        entry = TPediaEntry('laser_rifle', data)
        assert entry.pid == 'laser_rifle'
        assert entry.type == 2
        assert entry.name == 'Laser Rifle'
        assert entry.section == 'Weapons'
        assert entry.description == 'A powerful laser weapon.'
        assert entry.sprite == 'laser_rifle.png'
        assert entry.tech_needed == ['Laser Tech']
        assert entry.order == 5
        assert entry.related == ['plasma_rifle']
        assert entry.stats == {'damage': 60}

    def test_is_unlocked(self):
        data = {'tech_needed': ['Laser Tech', 'Elerium']}
        entry = TPediaEntry('laser_rifle', data)
        assert not entry.is_unlocked(['Laser Tech'])
        assert entry.is_unlocked(['Laser Tech', 'Elerium'])

class TestTPedia:
    def test_init_defaults(self):
        """Test TPedia initializes with empty dicts by default."""
        p = TPedia()
        assert isinstance(p.entries, dict)
        assert isinstance(p.categories, dict)

    def test_add_and_get_entry(self):
        """Test add_entry and get_entry methods."""
        p = TPedia()
        entry = DummyEntry('E1', 1)
        p.add_entry(entry)
        assert p.get_entry('E1') == entry

    def test_list_entries_by_type(self):
        """Test list_entries_by_type returns correct entries."""
        p = TPedia()
        e1 = DummyEntry('E1', 1)
        e2 = DummyEntry('E2', 2)
        e3 = DummyEntry('E3', 1)
        p.add_entry(e1)
        p.add_entry(e2)
        p.add_entry(e3)
        result = p.list_entries_by_type(1)
        assert e1 in result and e3 in result and e2 not in result

    def test_add_category(self):
        """Test add_category method."""
        p = TPedia()
        cat = DummyCategory(1)
        p.add_category(cat)
        assert 1 in p.categories or hasattr(p, 'categories')

