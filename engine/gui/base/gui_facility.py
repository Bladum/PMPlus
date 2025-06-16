"""
engine/gui/base/gui_facility.py

Facility Screen GUI for manufacturing and base facility management.

Classes:
    TGuiFacility: Main facility GUI screen for facility management interface.

Last standardized: 2025-06-15
"""

from gui.gui_core import TGuiCoreScreen


class TGuiFacility(TGuiCoreScreen):
    """
    Facility screen for manufacturing and base facilities.
    Inherits from TGuiCoreScreen.

    Attributes:
        None specific (inherits from TGuiCoreScreen)

    Methods:
        __init__(parent=None): Initialize the Facility GUI screen.
    """

    def __init__(self, parent=None):
        """
        Initialize the Facility GUI screen.

        Args:
            parent (QWidget, optional): Parent widget for the screen.
        """
        super().__init__(parent)
