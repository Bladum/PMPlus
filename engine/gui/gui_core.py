"""
XCOM GUI Module: gui_core.py

Base class for all screen widgets that can be displayed in the BaseGUI.

Classes:
    TGuiCoreScreen: Base class for all screen widgets.

Last updated: 2025-06-14
"""

from PySide6.QtWidgets import QWidget
from gui.theme_manager import XcomTheme


class TGuiCoreScreen(QWidget):
    """
    Base class for all screen widgets that can be displayed in the BaseGUI.
    Inherits from QWidget.
    """

    def __init__(self, parent=None):
        """
        Initialize the base screen widget.
        Args:
            parent: Parent widget.
        """
        super().__init__(parent)
        self.setStyleSheet(f"background: {XcomTheme.BG_MID};")

    def screen_activated(self):
        """
        Called when this screen becomes active.
        """
        pass

    def screen_deactivated(self):
        """
        Called when another screen becomes active.
        """
        pass

    def refresh_base_data(self):
        """
        Refresh data when base changes.
        """
        pass

    def update_summary_display(self):
        """
        Update summary data displays.
        """
        pass
