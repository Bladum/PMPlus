from engine.globe.country import TCountry
from engine.globe.funding import TFunding

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

