"""
engine/gui/base/gui_base_info.py

Base Info Summary Screen GUI for base activities overview.

Classes:
    TGuiBaseInfo: Main base info summary GUI screen.

Last standardized: 2025-06-15
"""

from gui.gui_core import TGuiCoreScreen


class TGuiBaseInfo(TGuiCoreScreen):
    """
    Base info summary screen for base activities.
    Inherits from TGuiCoreScreen.

    Attributes:
        None specific (inherits from TGuiCoreScreen)

    Methods:
        __init__(parent=None): Initialize the Base Info GUI screen.
    """

    def __init__(self, parent=None):
        """
        Initialize the Base Info GUI screen.

        Args:
            parent (QWidget, optional): Parent widget for the screen.
        """
        super().__init__(parent)
