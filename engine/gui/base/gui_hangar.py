"""
TGuiHangar: Hangar screen GUI for crafts.
Purpose: Represents the craft management interface in the base GUI system.
Last update: 2025-06-11
"""

from gui.gui_core import TGuiCoreScreen


class TGuiHangar(TGuiCoreScreen):
    """
    Hangar screen for craft management.
    Inherits from TGuiCoreScreen.
    """
    def __init__(self, parent=None):
        """
        Initialize the Hangar GUI screen.
        Args:
            parent (QWidget, optional): Parent widget for the screen.
        """
        super().__init__(parent)
