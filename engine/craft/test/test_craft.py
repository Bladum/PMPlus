"""
Test suite for engine.craft.craft (TCraft)
Covers initialization and attribute defaults using pytest.
"""
import pytest
from engine.craft.craft import TCraft

class DummyGame:
    class Mod:
        def __init__(self):
            self.craft_types = {'default': DummyCraftType()}
    def __init__(self):
        self.mod = self.Mod()

class DummyCraftType:
    range = 1000
    health = 200

@pytest.fixture
def craft(monkeypatch):
    import engine.craft.craft as craft_mod
    monkeypatch.setattr(craft_mod, 'TGame', DummyGame)
    return TCraft('craft1', data={'type': 'default'})

def test_init_defaults(craft):
    """Test initialization and attribute values from data dict."""
    assert craft.position == [0, 0]
    assert craft.craft_type.range == 1000
    assert craft.max_fuel == 1000
    assert craft.current_fuel == 1000
    assert craft.health == 200
    assert craft.health_current == 200
    assert hasattr(craft, 'game')
