"""
TGuiBaseInfo: Base info summary screen GUI.
Purpose: Represents the summary of base activities in the base GUI system.
Last update: 2025-06-11
"""

from gui.gui_core import TGuiCoreScreen


class TGuiBaseInfo(TGuiCoreScreen):
    """
    Base info summary screen for base activities.
    Inherits from TGuiCoreScreen.
    """

    def __init__(self, parent=None):
        """
        Initialize the Base Info GUI screen.
        Args:
            parent (QWidget, optional): Parent widget for the screen.
        """
        super().__init__(parent)
