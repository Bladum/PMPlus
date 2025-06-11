import pytest
from engine.gui.base.gui_barracks import TGuiBarracks
from PySide6.QtWidgets import QApplication

@pytest.fixture(scope="module")
def app():
    import sys
    app = QApplication.instance() or QApplication(sys.argv)
    yield app

def test_barracks_init(app):
    barracks = TGuiBarracks()
    assert hasattr(barracks, 'equipment_slots')
    assert hasattr(barracks, 'unit_list_widget')
    assert hasattr(barracks, 'item_list_widget')
    assert hasattr(barracks, 'weight_label')
    assert hasattr(barracks, 'unit_info_label')
    assert hasattr(barracks, 'summary_label')
    assert hasattr(barracks, 'stat_bars')
    assert hasattr(barracks, 'traits_layout')
    assert hasattr(barracks, 'unit_avatar_label')

def test_refresh_base_data(app):
    barracks = TGuiBarracks()
    barracks.refresh_base_data()
    assert barracks.unit_info_label.text() == "No unit selected"
    assert barracks.current_unit is None

def test_update_summary_display(app):
    barracks = TGuiBarracks()
    barracks.update_summary_display()
    assert "Units:" in barracks.summary_label.text()

def test_save_and_load_template(app):
    barracks = TGuiBarracks()
    barracks._save_template()
    barracks._load_template()
    assert barracks.current_template_name in barracks.saved_templates

def test_on_unit_selected(app):
    barracks = TGuiBarracks()
    units = barracks.game.get_current_base_units()
    if units:
        unit_name = units[0][0]
        barracks._on_unit_selected(unit_name)
        assert barracks.current_unit == unit_name
        assert barracks.selected_unit_data is not None

