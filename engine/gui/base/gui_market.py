"""
TGuiMarket: Market screen GUI for purchases.
Purpose: Represents the purchase interface in the base GUI system.
Last update: 2025-06-11
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
