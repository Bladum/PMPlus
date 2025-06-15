"""
XCOM GUI Module: gui_hangar.py

Hangar Screen GUI for craft management.

Classes:
    TGuiHangar: Main hangar GUI screen for craft management interface.

Last updated: 2025-06-11
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
