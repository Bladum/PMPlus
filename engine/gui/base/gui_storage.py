"""
TGuiStorage: Storage screen GUI for base storage management.
Purpose: Represents the storage management interface in the base GUI system.
Last update: 2025-06-11
"""

from gui.gui_core import TGuiCoreScreen


class TGuiStorage(TGuiCoreScreen):
    """
    Storage screen for base storage management.
    Inherits from TGuiCoreScreen.
    """

    def __init__(self, parent=None):
        """
        Initialize the Storage GUI screen.
        Args:
            parent (QWidget, optional): Parent widget for the screen.
        """
        super().__init__(parent)
