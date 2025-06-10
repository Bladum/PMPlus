import pytest
from engine.lore.calendar import TCalendar
from unittest.mock import MagicMock

class DummyCampaignStep:
    def __init__(self, month, info):
        self.month = month
        self.weights = info.get('weights', {})
        self.qty_min = info.get('qty_min', 1)
        self.qty_max = info.get('qty_max', 1)

class DummyCampaign:
    def __init__(self, faction, regions=None, missions=None, tech_start=None, tech_end=None):
        self.faction = faction
        self.regions = regions or {'Region1': 1}
        self.missions = missions or []
        self.tech_start = tech_start or []
        self.tech_end = tech_end or []

class DummyFaction:
    def __init__(self, name, tech_start=None, tech_end=None):
        self.name = name
        self.tech_start = tech_start or []
        self.tech_end = tech_end or []

class DummyMission:
    def __init__(self, count=1, chance=1.0, timer=0, tech_start=None, tech_end=None):
        self.count = count
        self.chance = chance
        self.timer = timer
        self.tech_start = tech_start or []
        self.tech_end = tech_end or []

class DummyWorldMap:
    def __init__(self):
        self.regions = [MagicMock(name='Region1')]
    def get_random_tile_in_region(self, region):
        return 'Tile1'

def test_calendar_init_and_date():
    data = {'m01': {'qty_min': 1, 'qty_max': 2, 'weights': {'Alien': 1}}}
    cal = TCalendar(data)
    assert cal.year == 2000
    assert cal.month == 1
    assert cal.day == 1
    assert isinstance(cal.campaign_months, dict)
    cal.set_start_date(2025, 5, 10)
    assert cal.get_date() == (2025, 5, 10)

def test_advance_days_and_triggers():
    cal = TCalendar({'m01': {'qty_min': 1, 'qty_max': 1, 'weights': {'Alien': 1}}})
    cal.on_day = MagicMock()
    cal.on_week = MagicMock()
    cal.on_month = MagicMock()
    cal.on_quarter = MagicMock()
    cal.on_year = MagicMock()
    cal.advance_days(31)
    assert cal.on_day.call_count == 31
    assert cal.on_week.call_count > 0
    assert cal.on_month.call_count > 0
    assert cal.on_quarter.call_count > 0
    assert cal.on_year.call_count > 0

def test_generate_monthly_campaigns():
    data = {'m01': {'qty_min': 1, 'qty_max': 1, 'weights': {'Alien': 1}}}
    cal = TCalendar(data)
    # Patch campaign_months to use dummy step
    cal.campaign_months[0] = DummyCampaignStep(0, data['m01'])
    research_status = lambda t: True
    all_campaigns = [DummyCampaign('Alien', missions=[DummyMission()])]
    all_factions = [DummyFaction('Alien')]
    worldmap = DummyWorldMap()
    result = cal.generate_monthly_campaigns(0, research_status, all_campaigns, all_factions, worldmap)
    assert isinstance(result, list)
    assert result and 'campaign' in result[0]

def test_daily_campaign_check():
    cal = TCalendar({'m01': {'qty_min': 1, 'qty_max': 1, 'weights': {'Alien': 1}}})
    worldmap = DummyWorldMap()
    active_campaigns = [{
        'missions': [{'scheduled_day': 1, 'region': 'Region1', 'mission': DummyMission()}],
        'faction': DummyFaction('Alien'),
        'active_missions': []
    }]
    cal.daily_campaign_check(1, active_campaigns, worldmap)
    assert active_campaigns[0]['active_missions']

