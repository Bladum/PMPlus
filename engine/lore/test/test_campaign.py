"""
Test suite for TCampaign class.
Covers initialization, mission instantiation, and error handling.
"""
import pytest
from engine.lore.campaign import TCampaign
from engine.lore.mission import TMission

def test_campaign_init_basic():
    data = {
        'name': 'Alien Invasion',
        'score': 100,
        'objective': 1,
        'faction': 'Aliens',
        'tech_start': ['AlienTech'],
        'tech_end': [],
        'regions': {'Europe': 1},
        'missions': [
            {'ufo': 'Scout', 'count': 2, 'chance': 1, 'timer': 0, 'tech_start': [], 'tech_end': []}
        ]
    }
    camp = TCampaign('c1', data)
    assert camp.pid == 'c1'
    assert camp.name == 'Alien Invasion'
    assert camp.score == 100
    assert camp.objective == 1
    assert camp.faction == 'Aliens'
    assert camp.tech_start == ['AlienTech']
    assert camp.regions == {'Europe': 1}
    assert len(camp.missions) == 1
    assert isinstance(camp.missions[0], TMission)

def test_campaign_init_mission_error(monkeypatch):
    def broken_mission_init(self, data):
        raise ValueError('fail')
    monkeypatch.setattr('engine.lore.mission.TMission.__init__', broken_mission_init)
    data = {'missions': [{}]}
    # Should not raise, error is logged
    TCampaign('c2', data)

