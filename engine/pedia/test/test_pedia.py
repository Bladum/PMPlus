import pytest
from engine.pedia.pedia import TPedia
from engine.pedia.pedia_entry import TPediaEntry
from engine.pedia.pedia_entry_type import TPediaEntryType

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
    def test_add_and_get_entry(self):
        pedia = TPedia()
        entry = TPediaEntry('rifle', {'type': 1})
        pedia.add_entry(entry)
        assert pedia.get_entry('rifle') == entry

    def test_list_entries_by_type(self):
        pedia = TPedia()
        entry1 = TPediaEntry('rifle', {'type': 1})
        entry2 = TPediaEntry('pistol', {'type': 2})
        entry3 = TPediaEntry('sniper', {'type': 1})
        pedia.add_entry(entry1)
        pedia.add_entry(entry2)
        pedia.add_entry(entry3)
        result = pedia.list_entries_by_type(1)
        assert entry1 in result and entry3 in result and entry2 not in result

    def test_add_and_get_category(self):
        pedia = TPedia()
        cat = TPediaEntryType(1, 'Weapons')
        pedia.add_category(cat)
        assert pedia.get_category(1) == cat

