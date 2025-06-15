"""
XCOM GUI Module: gui_transfer.py

Transfer Screen GUI for inter-base transfers.

Classes:
    TGuiTransfer: Main transfer GUI screen for inter-base transfer interface.

Last updated: 2025-06-11
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
