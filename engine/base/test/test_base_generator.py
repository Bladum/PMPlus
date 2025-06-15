"""
Test suite for engine.base.base_generator (TBaseXComBattleGenerator)
Covers initialization and generate_battle_map method using pytest.
"""
import pytest
from engine.base.base_generator import TBaseXComBattleGenerator

class DummyFacilityType:
    def __init__(self, map_block):
        self.map_block = map_block

class DummyFacility:
    def __init__(self, facility_type, pos):
        self.facility_type = facility_type
        self.position = pos

class DummyBase:
    def __init__(self, facilities):
        self.facilities = facilities

@pytest.fixture
def base_generator():
    # Create a dummy base with two facilities at different positions
    facilities = {
        (1, 2): DummyFacility(DummyFacilityType('block_a'), (1, 2)),
        (3, 4): DummyFacility(DummyFacilityType('block_b'), (3, 4)),
    }
    return TBaseXComBattleGenerator(DummyBase(facilities))

def test_init_sets_base(base_generator):
    """Test that the base is set correctly on initialization."""
    assert hasattr(base_generator, 'base')

def test_generate_battle_map_shape_and_content(base_generator):
    """Test that generate_battle_map returns a 6x6 grid with correct map_blocks."""
    battle_map = base_generator.generate_battle_map()
    assert len(battle_map) == 6
    for row in battle_map:
        assert len(row) == 6
    # Check that the correct blocks are placed
    assert battle_map[2][1] == 'block_a'
    assert battle_map[4][3] == 'block_b'
    # Empty spots should be 'map_empty'
    assert battle_map[0][0] == 'map_empty'
    assert battle_map[5][5] == 'map_empty'
