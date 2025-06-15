"""
Test suite for TQuestEngine (quest_engine.py).
Covers class existence and docstring.
"""
import pytest
from engine.lore.quest_engine import TQuestEngine

def test_quest_engine_exists():
    """Test TQuestEngine class exists and has docstring."""
    assert hasattr(TQuestEngine, '__doc__')
    assert isinstance(TQuestEngine(), TQuestEngine)
