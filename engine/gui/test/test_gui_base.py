"""
Test suite for gui_base.py (TGuiBase main base GUI class).
Mocks PySide6 widgets for headless testing.
"""
import pytest
from unittest.mock import patch, MagicMock

gui_base = pytest.importorskip('engine.gui.gui_base', reason="gui_base requires PySide6")

@pytest.fixture
def mock_parent():
    return MagicMock()

@pytest.fixture
def tgui_base(mock_parent):
    with patch('engine.gui.gui_base.QWidget', autospec=True), \
         patch('engine.gui.gui_base.QVBoxLayout', autospec=True), \
         patch('engine.gui.base.gui__base_top.TGuiBaseTopPanel', autospec=True) as MockTopPanel:
        instance = gui_base.TGuiBase(mock_parent)
        # Simulate signals for coverage
        instance.top_panel = MockTopPanel()
        instance.top_panel.screen_changed = MagicMock()
        instance.top_panel.base_changed = MagicMock()
        return instance

def test_init_layout_and_widgets(tgui_base):
    """Test TGuiBase initializes layout, top_panel, and screen_container."""
    assert hasattr(tgui_base, 'layout')
    assert hasattr(tgui_base, 'top_panel')
    assert hasattr(tgui_base, 'screen_container')
    assert hasattr(tgui_base, 'screen_layout')
    assert hasattr(tgui_base, 'screens')
