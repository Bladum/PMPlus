"""
TGuiWorkshop: Workshop screen GUI for manufacturing.
Purpose: Represents the manufacturing interface in the base GUI system.
Last update: 2025-06-11
"""

from gui.gui_core import TGuiCoreScreen


class TGuiWorkshop(TGuiCoreScreen):
    """
    Workshop screen for manufacturing.
    Inherits from TGuiCoreScreen.
    """

    def __init__(self, parent=None):
        """
        Initialize the Workshop GUI screen.
        Args:
            parent (QWidget, optional): Parent widget for the screen.
        """
        super().__init__(parent)
