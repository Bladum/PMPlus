"""
Test suite for engine.globe.funding (TFunding)
Covers initialization, add_tile_score, and monthly_report using pytest.
"""
import pytest
from engine.globe.funding import TFunding

class DummyCountry:
    def __init__(self, pid, name):
        self.pid = pid
        self.name = name
        self.relation = 0
        self.funding = 0
        self.active = True
        def monthly_update(score):
            self.relation += score
            self.funding += score
        self.monthly_update = monthly_update

@pytest.fixture
def funding():
    countries = [DummyCountry('FR', 'France'), DummyCountry('US', 'USA')]
    return TFunding(countries)

def test_init_defaults(funding):
    """Test initialization sets countries and month_scores."""
    assert isinstance(funding.countries, list)
    assert set(funding.month_scores.keys()) == {'FR', 'US'}

def test_add_tile_score_and_monthly_report(funding):
    """Test add_tile_score and monthly_report update scores and call monthly_update."""
    funding.add_tile_score('FR', 5)
    funding.add_tile_score('US', 10)
    report = funding.monthly_report()
    assert report['France']['score'] == 5
    assert report['USA']['score'] == 10
    assert funding.month_scores['FR'] == 0
    assert funding.month_scores['US'] == 0

def test_tfunding_add_score_and_report():
    c1 = TCountry('A', {'name': 'A'})
    c2 = TCountry('B', {'name': 'B'})
    funding = TFunding([c1, c2])
    funding.add_tile_score('A', 10)
    funding.add_tile_score('B', -5)
    report = funding.monthly_report()
    assert 'A' in report and 'B' in report
    assert report['A']['score'] == 10
    assert report['B']['score'] == -5

