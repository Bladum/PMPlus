"""
engine/gui/base/gui_storage.py

Storage Screen GUI for base storage management.

Classes:
    TGuiStorage: Main storage GUI screen for storage management interface.

Last standardized: 2025-06-15
"""

from gui.gui_core import TGuiCoreScreen


class TGuiStorage(TGuiCoreScreen):
    """
    Storage screen for base storage management.
    Inherits from TGuiCoreScreen.

    Attributes:
        None specific (inherits from TGuiCoreScreen)

    Methods:
        __init__(parent=None): Initialize the Storage GUI screen.
    """

    def __init__(self, parent=None):
        """
        Initialize the Storage GUI screen.

        Args:
            parent (QWidget, optional): Parent widget for the screen.
        """
        super().__init__(parent)
