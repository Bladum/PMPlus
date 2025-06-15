"""
XCOM GUI Module: gui_facility.py

Facility Screen GUI for manufacturing and base facility management.

Classes:
    TGuiFacility: Main facility GUI screen for facility management interface.

Last updated: 2025-06-11
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
