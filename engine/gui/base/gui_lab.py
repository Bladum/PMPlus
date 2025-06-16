"""
engine/gui/base/gui_lab.py

Laboratory Screen GUI for science and research management.

Classes:
    TGuiLab: Main laboratory GUI screen for science/research interface.

Last standardized: 2025-06-15
"""

from gui.gui_core import TGuiCoreScreen


class TGuiLab(TGuiCoreScreen):
    """
    Laboratory screen for science and research.
    Inherits from TGuiCoreScreen.

    Attributes:
        None specific (inherits from TGuiCoreScreen)

    Methods:
        __init__(parent=None): Initialize the Laboratory GUI screen.
    """

    def __init__(self, parent=None):
        """
        Initialize the Laboratory GUI screen.

        Args:
            parent (QWidget, optional): Parent widget for the screen.
        """
        super().__init__(parent)
