import pytest
from engine.economy.research_tree import TResearchTree
from engine.economy.research_entry import TResearchEntry

class TestTResearchTree:
    def test_add_and_get_entry(self):
        tree = TResearchTree()
        entry = TResearchEntry('tech1', {'name': 'Laser Weapons'})
        entry.id = 'tech1'
        tree.add_entry(entry)
        assert tree.get_entry('tech1') is entry

    def test_start_and_progress_research(self):
        tree = TResearchTree()
        entry = TResearchEntry('tech1', {'name': 'Laser Weapons', 'cost': 10})
        entry.id = 'tech1'
        tree.add_entry(entry)
        tree.available.add('tech1')
        tree.start_research('tech1')
        assert 'tech1' in tree.in_progress
        tree.progress_research('tech1', 5)
        assert tree.in_progress['tech1'] == 5
        tree.progress_research('tech1', 5)
        assert 'tech1' not in tree.in_progress
        assert 'tech1' in tree.completed

    def test_get_research_progress(self):
        tree = TResearchTree()
        entry = TResearchEntry('tech1', {'name': 'Laser Weapons', 'cost': 20})
        entry.id = 'tech1'
        tree.add_entry(entry)
        tree.available.add('tech1')
        tree.start_research('tech1')
        tree.progress_research('tech1', 10)
        progress, percent = tree.get_research_progress('tech1')
        assert 0.49 < progress < 0.51
        assert percent == 50

    def test_lock_and_unlock_entry(self):
        tree = TResearchTree()
        entry = TResearchEntry('tech1', {'name': 'Laser Weapons'})
        entry.id = 'tech1'
        tree.add_entry(entry)
        tree.lock_entry('tech1')
        assert 'tech1' in tree.locked
        tree.unlock_entry('tech1')
        assert 'tech1' not in tree.locked

