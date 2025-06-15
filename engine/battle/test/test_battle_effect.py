"""
Test suite for engine.battle.battle_effect (TBattleEffect)
Covers initialization and attribute defaults using pytest.
"""
import pytest
from engine.battle.battle_effect import TBattleEffect

@pytest.fixture
def effect():
    data = {
        'name': 'Smoke',
        'description': 'Obscures vision',
        'icon': 'smoke_icon.png',
    }
    return TBattleEffect('smoke', data)

def test_init_defaults(effect):
    """Test initialization and attribute values from data dict."""
    assert effect.pid == 'smoke'
    assert effect.name == 'Smoke'
    assert effect.description == 'Obscures vision'
    assert effect.icon == 'smoke_icon.png'
