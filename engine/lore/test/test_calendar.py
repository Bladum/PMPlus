"""
Test suite for TCalendar class.
Covers initialization, date progression, campaign generation, and error handling.
"""
import pytest
from engine.lore.calendar import TCalendar
from engine.lore.campaign_step import TCampaignStep

class DummyWorldMap:
    def __init__(self):
        self.regions = [type('Region', (), {'name': 'Region1'})()]
    def get_random_tile_in_region(self, region):
        return 'tile1'

def test_calendar_init_and_set_start_date():
    data = {'m01': {'qty_min': 1, 'qty_max': 2, 'events': 1, 'weights': {'Alien': 1}}}
    cal = TCalendar(data)
    assert cal.year == 2000
    assert cal.month == 1
    assert cal.day == 1
    assert isinstance(cal.campaign_months[1], TCampaignStep)
    cal.set_start_date(2025, 5, 10)
    assert cal.year == 2025
    assert cal.month == 5
    assert cal.day == 10

def test_calendar_advance_days():
    cal = TCalendar({'m01': {'qty_min': 1, 'qty_max': 1, 'events': 1, 'weights': {'Alien': 1}}})
    cal.set_start_date(2025, 1, 29)
    cal.advance_days(3)
    assert cal.day == 2
    assert cal.month == 2
    assert cal.year == 2025

def test_generate_monthly_campaigns_empty():
    cal = TCalendar()
    result = cal.generate_monthly_campaigns(1, lambda t: True, [], [], DummyWorldMap())
    assert result == []

def test_calendar_init_defaults():
    """Test TCalendar initializes with default values."""
    cal = TCalendar()
    assert cal.year == 2000
    assert cal.month == 1
    assert cal.day == 1
    assert cal.total_days == 0
    assert isinstance(cal.campaign_months, dict)


def test_calendar_init_with_data():
    """Test TCalendar parses campaign month data correctly."""
    data = {"m01": {"qty_min": 1, "qty_max": 2, "events": 3, "weights": {"A": 1}}}
    cal = TCalendar(data)
    assert 1 in cal.campaign_months
    step = cal.campaign_months[1]
    assert hasattr(step, 'qty_min')
    assert hasattr(step, 'qty_max')
    assert hasattr(step, 'events')
    assert hasattr(step, 'weights')

