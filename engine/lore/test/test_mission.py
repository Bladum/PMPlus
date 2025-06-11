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

