"""
Test suite for theme_manager.py (XCOM GUI theming system).
Covers: px utility, XcomTheme constants, and module-level attributes.
Uses pytest and unittest.mock for Qt dependencies.
"""
import pytest
from unittest.mock import patch

import sys
import types

# Patch PySide6 imports for headless testing
theme_manager = pytest.importorskip('engine.gui.theme_manager', reason="theme_manager requires PySide6")


def test_px_scaling():
    """Test px() utility scales pixel values by SCALE."""
    assert theme_manager.px(1) == 2  # Default SCALE=2
    assert theme_manager.px(16) == 32
    with patch.object(theme_manager, 'SCALE', 3):
        assert theme_manager.px(10) == 30


def test_theme_constants():
    """Test that XcomTheme class has expected color attributes."""
    theme = theme_manager.XcomTheme
    assert hasattr(theme, '__doc__')
    # Example: check for a common color constant (BG_MID)
    assert hasattr(theme, 'BG_MID')


def test_module_level_constants():
    """Test module-level constants for correct types and values."""
    assert isinstance(theme_manager.SCALE, int)
    assert theme_manager.SCALE > 0
    assert theme_manager.BASE_WIDTH == 640
    assert theme_manager.BASE_HEIGHT == 400
    assert theme_manager.SCALED_WIDTH == theme_manager.BASE_WIDTH * theme_manager.SCALE
    assert theme_manager.SCALED_HEIGHT == theme_manager.BASE_HEIGHT * theme_manager.SCALE
    assert theme_manager.GRID == 16
    assert theme_manager.WIDGET_MARGIN == 1
    assert theme_manager.WIDGET_PADDING == 1

# XcomStyle and theme_manager singleton are not tested here due to GUI/Qt dependencies.
# For full coverage, use integration/UI tests with a Qt test runner.
