"""
engine/gui/base/gui_transfer.py

Transfer Screen GUI for inter-base transfers.

Classes:
    TGuiTransfer: Main transfer GUI screen for inter-base transfer interface.

Last standardized: 2025-06-15
"""

from gui.gui_core import TGuiCoreScreen


class TGuiTransfer(TGuiCoreScreen):
    """
    Transfer screen for inter-base transfers.
    Inherits from TGuiCoreScreen.

    Attributes:
        None specific (inherits from TGuiCoreScreen)

    Methods:
        __init__(parent=None): Initialize the Transfer GUI screen.
    """

    def __init__(self, parent=None):
        """
        Initialize the Transfer GUI screen.

        Args:
            parent (QWidget, optional): Parent widget for the screen.
        """
        super().__init__(parent)
