"""
engine/gui/base/gui_prison.py

Prison Screen GUI for containment management.

Classes:
    TGuiPrison: Main prison GUI screen for containment interface.

Last standardized: 2025-06-15
"""

from gui.gui_core import TGuiCoreScreen


class TGuiPrison(TGuiCoreScreen):
    """
    Prison screen for containment.
    Inherits from TGuiCoreScreen.

    Attributes:
        None specific (inherits from TGuiCoreScreen)

    Methods:
        __init__(parent=None): Initialize the Prison GUI screen.
    """

    def __init__(self, parent=None):
        """
        Initialize the Prison GUI screen.

        Args:
            parent (QWidget, optional): Parent widget for the screen.
        """
        super().__init__(parent)
