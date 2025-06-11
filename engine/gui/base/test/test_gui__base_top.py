import pytest
from engine.gui.base.gui__base_top import TGuiBaseTopPanel
from PySide6.QtWidgets import QApplication

@pytest.fixture(scope="module")
def app():
    import sys
    app = QApplication.instance() or QApplication(sys.argv)
    yield app

class TestTGuiBaseTopPanel:
    def test_init(self, app):
        panel = TGuiBaseTopPanel()
        assert panel.current_screen == "BARRACKS"
        assert hasattr(panel, 'available_screens')
        assert hasattr(panel, 'screen_buttons')
        assert hasattr(panel, 'base_buttons')

    def test_set_screen_valid(self, app):
        panel = TGuiBaseTopPanel()
        assert panel.set_screen("HANGAR") is True
        assert panel.get_current_screen() == "HANGAR"

    def test_set_screen_invalid(self, app):
        panel = TGuiBaseTopPanel()
        assert panel.set_screen("INVALID") is False
        assert panel.get_current_screen() == "BARRACKS"

    def test_update_date_and_money(self, app):
        panel = TGuiBaseTopPanel()
        panel.update_date_display("JAN 1, 2040")
        panel.update_money_display("$999,999")
        assert panel.date_label.text() == "JAN 1, 2040"
        assert panel.money_label.text() == "$999,999"

