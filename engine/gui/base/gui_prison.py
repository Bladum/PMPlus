"""
XCOM GUI Module: gui_prison.py

Prison Screen GUI for containment management.

Classes:
    TGuiPrison: Main prison GUI screen for containment interface.

Last updated: 2025-06-11
"""

from gui.gui_core import TGuiCoreScreen


class TGuiPrison(TGuiCoreScreen):
    """
    Prison screen for containment.
    Inherits from TGuiCoreScreen.
    """

    def __init__(self, parent=None):
        """
        Initialize the Prison GUI screen.
        Args:
            parent (QWidget, optional): Parent widget for the screen.
        """
        super().__init__(parent)
