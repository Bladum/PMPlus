"""
Test suite for engine.globe.diplomacy (TDiplomacy, DiplomacyState)
Covers initialization, get_state, and set_state using pytest.
"""

import pytest
from engine.globe.diplomacy import TDiplomacy, DiplomacyState

class DummyFaction:
    def __init__(self, pid):
        self.pid = pid

@pytest.fixture
def diplomacy():
    factions = [DummyFaction('XCOM'), DummyFaction('ALIENS')]
    return TDiplomacy(factions)

def test_init_defaults(diplomacy):
    """Test initialization sets all relations to NEUTRAL."""
    assert diplomacy.get_state('XCOM') == DiplomacyState.NEUTRAL
    assert diplomacy.get_state('ALIENS') == DiplomacyState.NEUTRAL

def test_set_state_and_history(diplomacy):
    """Test set_state updates relation and records history."""
    diplomacy.set_state('XCOM', DiplomacyState.ALLY)
    assert diplomacy.get_state('XCOM') == DiplomacyState.ALLY
    assert DiplomacyState.ALLY in diplomacy.history['XCOM']

def test_tdiplomacy_placeholder():
    dip = TDiplomacy()
    assert dip is not None

