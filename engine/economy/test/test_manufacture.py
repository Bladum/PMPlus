"""
Test suite for engine.economy.manufacture (TManufacture)
Covers initialization and load method using pytest.
"""
import pytest
from engine.economy.manufacture import TManufacture

class DummyManager:
    pass

def test_init_defaults():
    """Test initialization sets entries and manufacturing_manager."""
    m = TManufacture()
    assert isinstance(m.entries, dict)
    assert hasattr(m, 'manufacturing_manager')

def test_load_with_no_data_warns(caplog):
    """Test load with no manufacturing section logs a warning."""
    m = TManufacture()
    with caplog.at_level('WARNING'):
        m.load({})
    assert "No 'manufacturing' section found in data." in caplog.text
