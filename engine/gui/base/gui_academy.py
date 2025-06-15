"""
XCOM GUI Module: gui_academy.py

Academy Screen GUI for manufacturing and training management.

Classes:
    TGuiAcademy: Main academy GUI screen for manufacturing/training interface.

Last updated: 2025-06-11
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
