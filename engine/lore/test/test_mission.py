"""
Test suite for TMission class.
Covers initialization and attribute assignment.
"""
import pytest
from engine.lore.mission import TMission

def test_mission_init_basic():
    data = {
        'ufo': 'Scout',
        'site': 'CrashSite',
        'base': 'AlienBase',
        'count': 2,
        'chance': 0.5,
        'timer': 3,
        'tech_start': ['AlienTech'],
        'tech_end': ['EndTech'],
        'deployments': {'aliens': 5}
    }
    m = TMission(data)
    assert m.ufo == 'Scout'
    assert m.site == 'CrashSite'
    assert m.base == 'AlienBase'
    assert m.count == 2
    assert m.chance == 0.5
    assert m.timer == 3
    assert m.tech_start == ['AlienTech']
    assert m.tech_end == ['EndTech']
    assert m.deployments == {'aliens': 5}

def test_mission_init_defaults():
    """Test TMission initializes with default values."""
    data = {}
    m = TMission(data)
    assert m.ufo is None
    assert m.site is None
    assert m.base is None
    assert m.count == 1
    assert m.chance == 1
    assert m.timer == 0
    assert m.tech_start == []
    assert m.tech_end == []
    assert isinstance(m.deployments, dict)


def test_mission_init_with_data():
    """Test TMission initializes with provided data."""
    data = {'ufo': 'UFO1', 'site': 'SITE1', 'base': 'BASE1', 'count': 2, 'chance': 0.5, 'timer': 3, 'tech_start': ['A'], 'tech_end': ['B'], 'deployments': {'D': 1}}
    m = TMission(data)
    assert m.ufo == 'UFO1'
    assert m.site == 'SITE1'
    assert m.base == 'BASE1'
    assert m.count == 2
    assert m.chance == 0.5
    assert m.timer == 3
    assert m.tech_start == ['A']
    assert m.tech_end == ['B']
    assert m.deployments == {'D': 1}

