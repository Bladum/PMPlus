"""
Test suite for engine.economy.black_market (BlackMarketSupplier, BlackMarket)
Covers initialization and attribute defaults for BlackMarketSupplier using pytest.
"""
import pytest
from engine.economy.black_market import BlackMarketSupplier

@pytest.fixture
def supplier():
    data = {
        'reputation': 'trusted',
        'region_specialization': ['Europe'],
        'item_specialization': ['weapons'],
        'availability_schedule': 'daily',
        'price_variance_range': [0.8, 1.5],
        'reliability': 0.95,
        'discovery_requirements': {'techs': ['Alien Alloys']},
        'is_discovered': True,
    }
    return BlackMarketSupplier('SupplierX', data)

def test_init_defaults(supplier):
    """Test initialization and attribute values from data dict."""
    assert supplier.name == 'SupplierX'
    assert supplier.reputation == 'trusted'
    assert supplier.region_specialization == ['Europe']
    assert supplier.item_specialization == ['weapons']
    assert supplier.availability_schedule == 'daily'
    assert supplier.price_variance_range == (0.8, 1.5)
    assert supplier.reliability == 0.95
    assert supplier.discovery_requirements == {'techs': ['Alien Alloys']}
    assert supplier.is_discovered is True
    assert isinstance(supplier.current_stock, list)
