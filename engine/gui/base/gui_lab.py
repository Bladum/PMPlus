"""
TGuiLab: Laboratory screen GUI for science/research.
Purpose: Represents the science/research interface in the base GUI system.
Last update: 2025-06-11
"""

from gui.gui_core import TGuiCoreScreen


class TGuiLab(TGuiCoreScreen):
    """
    Laboratory screen for science and research.
    Inherits from TGuiCoreScreen.
    """

    def __init__(self, parent=None):
        """
        Initialize the Laboratory GUI screen.
        Args:
            parent (QWidget, optional): Parent widget for the screen.
        """
        super().__init__(parent)
