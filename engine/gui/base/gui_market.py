"""
engine/gui/base/gui_market.py

Market Screen GUI for purchases.

Classes:
    TGuiMarket: Main market GUI screen for purchase interface.

Last standardized: 2025-06-15
"""

from gui.gui_core import TGuiCoreScreen


class TGuiMarket(TGuiCoreScreen):
    """
    Market screen for purchases.
    Inherits from TGuiCoreScreen.

    Attributes:
        None specific (inherits from TGuiCoreScreen)

    Methods:
        __init__(parent=None): Initialize the Market GUI screen.
    """

    def __init__(self, parent=None):
        """
        Initialize the Market GUI screen.

        Args:
            parent (QWidget, optional): Parent widget for the screen.
        """
        super().__init__(parent)
