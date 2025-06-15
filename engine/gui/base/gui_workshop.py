"""
XCOM GUI Module: gui_workshop.py

Workshop Screen GUI for manufacturing management.

Classes:
    TGuiWorkshop: Main workshop GUI screen for manufacturing interface.

Last updated: 2025-06-11
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
