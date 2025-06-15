"""
Test suite for engine.economy.manufacturing_manager (ManufacturingManager)
Covers initialization and workshop capacity methods using pytest.
"""
import pytest
from engine.economy.manufacturing_manager import ManufacturingManager

@pytest.fixture
def manager():
    return ManufacturingManager()

def test_init_defaults(manager):
    """Test initialization sets active_projects and workshop_capacity as dicts."""
    assert isinstance(manager.active_projects, dict)
    assert isinstance(manager.workshop_capacity, dict)

def test_set_and_get_base_workshop_capacity(manager):
    """Test setting and getting workshop capacity for a base."""
    manager.set_base_workshop_capacity('base1', 10)
    assert manager.get_base_workshop_capacity('base1') == 10

def test_get_used_and_available_workshop_capacity(manager):
    """Test used and available workshop capacity returns correct values when no projects."""
    manager.set_base_workshop_capacity('base2', 20)
    assert manager.get_used_workshop_capacity('base2') == 0
    assert manager.get_available_workshop_capacity('base2') == 20
