"""
TGuiFacility: Facility screen GUI for manufacturing and base facilities.
Purpose: Represents the facility management interface in the base GUI system.
Last update: 2025-06-11
"""

from gui.gui_core import TGuiCoreScreen


class TGuiFacility(TGuiCoreScreen):
    """
    Facility screen for manufacturing and base facilities.
    Inherits from TGuiCoreScreen.
    """

    def __init__(self, parent=None):
        """
        Initialize the Facility GUI screen.
        Args:
            parent (QWidget, optional): Parent widget for the screen.
        """
        super().__init__(parent)
