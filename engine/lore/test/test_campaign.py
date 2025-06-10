import pytest
from engine.lore.campaign import TCampaign
from unittest.mock import patch, MagicMock

def test_campaign_init_minimal():
    data = {
        'name': 'Alien Invasion',
        'score': 100,
        'objective': 1,
        'faction': 'Aliens',
        'tech_start': ['AlienTech'],
        'tech_end': ['HumanVictory'],
        'regions': {'Europe': 2, 'Asia': 1},
        'missions': [
            {'ufo': 'Scout', 'count': 2, 'chance': 1.0, 'timer': 0, 'tech_start': [], 'tech_end': []}
        ]
    }
    with patch('engine.lore.mission.TMission', autospec=True) as MockMission:
        campaign = TCampaign('camp01', data)
        assert campaign.pid == 'camp01'
        assert campaign.name == 'Alien Invasion'
        assert campaign.score == 100
        assert campaign.objective == 1
        assert campaign.faction == 'Aliens'
        assert campaign.tech_start == ['AlienTech']
        assert campaign.tech_end == ['HumanVictory']
        assert campaign.regions == {'Europe': 2, 'Asia': 1}
        assert isinstance(campaign.missions, list)
        MockMission.assert_called()

def test_campaign_init_empty():
    data = {}
    with patch('engine.lore.mission.TMission', autospec=True) as MockMission:
        campaign = TCampaign('camp02', data)
        assert campaign.pid == 'camp02'
        assert campaign.name == ''
        assert campaign.score == 0
        assert campaign.objective == 0
        assert campaign.faction == ''
        assert campaign.tech_start == []
        assert campaign.tech_end == []
        assert campaign.regions == {}
        assert campaign.missions == []
        MockMission.assert_not_called()

def test_campaign_objective_constants():
    assert TCampaign.OBJECTIVE_SCOUT == 0
    assert TCampaign.OBJECTIVE_INFILTRATE == 1
    assert TCampaign.OBJECTIVE_BASE == 2
    assert TCampaign.OBJECTIVE_TERROR == 3
    assert TCampaign.OBJECTIVE_RETALIATION == 4
    assert TCampaign.OBJECTIVE_RESEARCH == 5
    assert TCampaign.OBJECTIVE_DESTRUCTION == 6
    assert TCampaign.OBJECTIVE_SUPPLY == 7
    assert TCampaign.OBJECTIVE_HUNT == 8

