"""
Test suite for engine.unit.unit (TUnit)
Covers initialization and attribute defaults using pytest.
"""
import pytest
from engine.unit.unit import TUnit
from unittest.mock import MagicMock
from unit.unit import TUnit
from unit.unit_type import TUnitType
from unit.unit_stat import TUnitStats
from unit.race import TRace
from unit.trait import TTrait

class DummyInventoryManager:
    def __init__(self, unit):
        self.equipment_slots = {'Armor': None, 'Primary': None}
        self.stat_modifiers = {}
    def get_all_items(self):
        return []

class DummyTrait:
    def __init__(self):
        self.stats = TUnitStats({'health': 1})

class TestTUnit:
    def test_init(self):
        unit_type = MagicMock(spec=TUnitType)
        side_id = 1
        unit = TUnit(unit_type, side_id)
        assert unit.unit_type == unit_type
        assert unit.side_id == side_id
        assert unit.name == ''
        assert unit.nationality == ''
        assert unit.face == ''
        assert unit.female is False
        assert unit.inventory == []
        assert unit.position is None
        assert unit.direction is None
        assert unit.alive is True
        assert unit.dead is False
        assert unit.mind_controlled is False
        assert unit.panicked is False
        assert unit.crazy is False
        assert unit.stunned is False
        assert unit.kneeling is False
        assert unit.running is False

    def test_properties(self, monkeypatch):
        unit_type = MagicMock(spec=TUnitType)
        unit = TUnit(unit_type, 1)
        dummy_inv = DummyInventoryManager(unit)
        monkeypatch.setattr(unit, 'inventory_manager', dummy_inv)
        assert unit.armour is None
        assert unit.weapon is None
        assert unit.equipment == []

    def test_calculate_stats(self, monkeypatch):
        unit_type = MagicMock(spec=TUnitType)
        unit = TUnit(unit_type, 1)
        unit.race = MagicMock(spec=TRace)
        unit.race.stats = TUnitStats({'health': 10})
        trait = DummyTrait()
        unit.traits = [trait]
        dummy_inv = DummyInventoryManager(unit)
        monkeypatch.setattr(unit, 'inventory_manager', dummy_inv)
        stats = unit.calculate_stats()
        assert isinstance(stats, TUnitStats)
        assert stats.health == 11

class DummyUnitType:
    pass

@pytest.fixture
def unit():
    return TUnit(DummyUnitType(), side_id=1)

def test_init_defaults(unit):
    """Test initialization and attribute presence."""
    assert hasattr(unit, 'unit_type')
    assert hasattr(unit, 'side_id')
    assert hasattr(unit, 'name')
    assert hasattr(unit, 'stats')
    assert hasattr(unit, 'traits')
    assert hasattr(unit, 'inventory_manager')
    assert hasattr(unit, 'alive')
    assert hasattr(unit, 'dead')
    assert hasattr(unit, 'mind_controlled')
    assert hasattr(unit, 'panicked')
    assert hasattr(unit, 'crazy')
    assert hasattr(unit, 'stunned')
    assert hasattr(unit, 'kneeling')
    assert hasattr(unit, 'running')

