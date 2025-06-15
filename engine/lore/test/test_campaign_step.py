"""
Test suite for TCampaignStep class.
Covers initialization, default values, and error handling for weights and numeric fields.
"""
import pytest
from engine.lore.campaign_step import TCampaignStep

def test_campaign_step_init_full():
    data = {
        'qty_min': 2,
        'qty_max': 5,
        'events': 3,
        'weights': {'Alien': 2, 'Human': 1}
    }
    step = TCampaignStep(7, data)
    assert step.month == 7
    assert step.qty_min == 2
    assert step.qty_max == 5
    assert step.events == 3
    assert step.weights == {'Alien': 2, 'Human': 1}

def test_campaign_step_init_defaults():
    data = {}
    step = TCampaignStep(1, data)
    assert step.month == 1
    assert step.qty_min == 0
    assert step.qty_max == 0
    assert step.events == 0
    assert step.weights == {}

def test_campaign_step_weights_type():
    data = {'weights': ['not', 'a', 'dict']}
    step = TCampaignStep(2, data)
    assert step.weights == {}

def test_campaign_step_init_with_data():
    """Test TCampaignStep initializes with provided data."""
    data = {'qty_min': 2, 'qty_max': 5, 'events': 3, 'weights': {'A': 1}}
    step = TCampaignStep(2, data)
    assert step.qty_min == 2
    assert step.qty_max == 5
    assert step.events == 3
    assert step.weights == {'A': 1}

