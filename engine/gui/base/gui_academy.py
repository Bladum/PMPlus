"""
TGuiAcademy: Academy screen GUI for manufacturing and training.
Purpose: Represents the manufacturing/training interface in the base GUI system.
Last update: 2025-06-11
"""

from gui.gui_core import TGuiCoreScreen


class TGuiAcademy(TGuiCoreScreen):
    """
    Academy screen for manufacturing and training.
    Inherits from TGuiCoreScreen.
    """

    def __init__(self, parent=None):
        """
        Initialize the Academy GUI screen.
        Args:
            parent (QWidget, optional): Parent widget for the screen.
        """
        super().__init__(parent)
