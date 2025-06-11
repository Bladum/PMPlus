"""
TGuiPrison: Prison screen GUI for containment.
Purpose: Represents the containment/prison interface in the base GUI system.
Last update: 2025-06-11
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
