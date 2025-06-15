"""
Test suite for engine.economy.manufacturing_project (ManufacturingProject)
Covers initialization and attribute defaults using pytest.
"""
import pytest
from engine.economy.manufacturing_project import ManufacturingProject

@pytest.fixture
def project():
    return ManufacturingProject('LR1', 'base1', 5, 10, workshop_capacity=2)

def test_init_defaults(project):
    """Test initialization and attribute values."""
    assert isinstance(project.project_id, str)
    assert project.entry_id == 'LR1'
    assert project.base_id == 'base1'
    assert project.quantity == 5
    assert project.progress == 0.0
    assert project.total_time == 50
    assert project.workshop_capacity == 2
    assert project.status == 'active'
    assert project.items_completed == 0
    assert project.cost_paid is False
    assert project.build_time_per_item == 10
    assert hasattr(project, 'start_date')
    assert hasattr(project, 'estimated_completion')
