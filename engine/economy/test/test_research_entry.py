import pytest
from engine.economy.research_entry import TResearchEntry

class TestTResearchEntry:
    def test_init_defaults(self):
        entry = TResearchEntry('pid1')
        assert entry.pid == 'pid1'
        assert entry.name == ''
        assert entry.cost == 0
        assert entry.score == 0
        assert entry.tech_needed == []
        assert entry.items_needed == {}
        assert entry.services_needed == []
        assert entry.event_spawn is None
        assert entry.item_spawn == {}
        assert entry.tech_disable == []
        assert entry.tech_give == []
        assert entry.tech_unlock == []
        assert entry.pedia is None
        assert entry.complete_game is False

    def test_init_with_data(self):
        data = {
            'name': 'Alien Alloys',
            'cost': 100,
            'score': 50,
            'tech_needed': ['Alien Biology'],
            'items_needed': {'corpse': 1},
            'services_needed': ['Lab'],
            'event_spawn': 'event1',
            'item_spawn': {'alloy': 5},
            'tech_disable': ['OldTech'],
            'tech_give': ['NewTech'],
            'tech_unlock': ['UnlockTech'],
            'pedia': 'pedia_entry',
            'complete_game': True
        }
        entry = TResearchEntry('pid2', data)
        assert entry.name == 'Alien Alloys'
        assert entry.cost == 100
        assert entry.score == 50
        assert entry.tech_needed == ['Alien Biology']
        assert entry.items_needed == {'corpse': 1}
        assert entry.services_needed == ['Lab']
        assert entry.event_spawn == 'event1'
        assert entry.item_spawn == {'alloy': 5}
        assert entry.tech_disable == ['OldTech']
        assert entry.tech_give == ['NewTech']
        assert entry.tech_unlock == ['UnlockTech']
        assert entry.pedia == 'pedia_entry'
        assert entry.complete_game is True

