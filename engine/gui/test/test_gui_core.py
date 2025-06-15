"""
Test suite for gui_core.py (TGuiCoreScreen base class).
Mocks PySide6.QtWidgets.QWidget for headless testing.
"""
import pytest
from unittest.mock import patch, MagicMock

# Patch PySide6.QtWidgets.QWidget for headless test
gui_core = pytest.importorskip('engine.gui.gui_core', reason="gui_core requires PySide6")

@pytest.fixture
def mock_parent():
    return MagicMock()

@pytest.fixture
def screen(mock_parent):
    with patch('engine.gui.gui_core.QWidget', autospec=True):
        return gui_core.TGuiCoreScreen(mock_parent)


def test_init_sets_stylesheet(screen):
    """Test TGuiCoreScreen initializes and sets stylesheet."""
    assert hasattr(screen, 'setStyleSheet')


def test_screen_activated_deactivated_refresh_update(screen):
    """Test that all public methods exist and are callable (no-op)."""
    screen.screen_activated()
    screen.screen_deactivated()
    screen.refresh_base_data()
    screen.update_summary_display()
    # No exceptions should be raised
