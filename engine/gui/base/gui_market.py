"""
XCOM GUI Module: gui_market.py

Market Screen GUI for purchases.

Classes:
    TGuiMarket: Main market GUI screen for purchase interface.

Last updated: 2025-06-11
"""

from gui.gui_core import TGuiCoreScreen


class TGuiMarket(TGuiCoreScreen):
    """
    Market screen for purchases.
    Inherits from TGuiCoreScreen.
    """

    def __init__(self, parent=None):
        """
        Initialize the Market GUI screen.
        Args:
            parent (QWidget, optional): Parent widget for the screen.
        """
        super().__init__(parent)
