"""
engine/gui/base/gui_academy.py

Academy Screen GUI for manufacturing and training management.

Classes:
    TGuiAcademy: Main academy GUI screen for manufacturing/training interface.

Last standardized: 2025-06-15
"""

from gui.gui_core import TGuiCoreScreen


class TGuiAcademy(TGuiCoreScreen):
    """
    Academy screen for manufacturing and training.
    Inherits from TGuiCoreScreen.

    Attributes:
        None specific (inherits from TGuiCoreScreen)

    Methods:
        __init__(parent=None): Initialize the Academy GUI screen.
    """

    def __init__(self, parent=None):
        """
        Initialize the Academy GUI screen.

        Args:
            parent (QWidget, optional): Parent widget for the screen.
        """
        super().__init__(parent)
