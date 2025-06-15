"""
Test suite for gui_world.py (TGuiGlobe main globe GUI class).
Mocks PySide6 widgets for headless testing.
"""
import pytest
from unittest.mock import patch, MagicMock

gui_world = pytest.importorskip('engine.gui.gui_world', reason="gui_world requires PySide6")

@pytest.fixture
def mock_parent():
    return MagicMock()

@pytest.fixture
def tgui_globe(mock_parent):
    with patch('engine.gui.gui_world.QWidget', autospec=True), \
         patch('engine.gui.gui_world.QVBoxLayout', autospec=True), \
         patch('engine.gui.globe.gui__globe_top.TGuiGlobeTopPanel', autospec=True) as MockTopPanel:
        instance = gui_world.TGuiGlobe(mock_parent)
        # Simulate signals for coverage
        instance.top_panel = MockTopPanel()
        instance.top_panel.screen_changed = MagicMock()
        return instance

def test_init_layout_and_widgets(tgui_globe):
    """Test TGuiGlobe initializes layout, top_panel, and screen_container."""
    assert hasattr(tgui_globe, 'layout')
    assert hasattr(tgui_globe, 'top_panel')
    assert hasattr(tgui_globe, 'screen_container')
    assert hasattr(tgui_globe, 'screen_layout')
    assert hasattr(tgui_globe, 'screens')
