"""
engine/gui/base/gui_hangar.py

Hangar Screen GUI for craft management.

Classes:
    TGuiHangar: Main hangar GUI screen for craft management interface.

Last standardized: 2025-06-15
"""

from gui.gui_core import TGuiCoreScreen


class TGuiHangar(TGuiCoreScreen):
    """
    Hangar screen for craft management.
    Inherits from TGuiCoreScreen.

    Attributes:
        None specific (inherits from TGuiCoreScreen)

    Methods:
        __init__(parent=None): Initialize the Hangar GUI screen.
    """
    def __init__(self, parent=None):
        """
        Initialize the Hangar GUI screen.

        Args:
            parent (QWidget, optional): Parent widget for the screen.
        """
        super().__init__(parent)
