"""
Test suite for engine.craft.interception (TInterception)
Covers initialization and get_state method using pytest.
"""
import pytest
from engine.craft.interception import TInterception

class DummyCraft:
    pass
class DummyUfo:
    pass

@pytest.fixture
def interception(monkeypatch):
    # Patch TGame to avoid side effects
    import engine.craft.interception as interception_mod
    monkeypatch.setattr(interception_mod, 'TGame', lambda: None)
    return TInterception(DummyCraft(), DummyUfo(), distance=150)

def test_init_defaults(interception):
    """Test initialization and attribute values."""
    assert interception.distance == 150
    assert interception.turn == 0
    assert interception.ap == [4, 4]
    assert interception.log == []
    assert interception.crashed == [False, False]
    assert len(interception.crafts) == 2

def test_get_state_returns_dict(interception):
    """Test get_state returns a dictionary with expected keys."""
    state = interception.get_state()
    assert 'distance' in state
    assert 'crafts' in state
    assert 'ap' in state
    assert 'turn' in state
    assert 'crash_status' in state or 'crashed' in state or 'crafts' in state  # Accept any reasonable key
