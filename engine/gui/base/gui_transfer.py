"""
TGuiTransfer: Transfer screen GUI for inter-base transfers.
Purpose: Represents the transfer interface between bases in the base GUI system.
Last update: 2025-06-11
"""

from gui.gui_core import TGuiCoreScreen


class TGuiTransfer(TGuiCoreScreen):
    """
    Transfer screen for inter-base transfers.
    Inherits from TGuiCoreScreen.
    """

    def __init__(self, parent=None):
        """
        Initialize the Transfer GUI screen.

        Args:
            parent (QWidget, optional): Parent widget for the screen.
        """
        super().__init__(parent)
