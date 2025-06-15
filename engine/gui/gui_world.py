"""
XCOM GUI Module: gui_world.py

Main globe GUI class that manages screens and navigation for the XCOM globe view.

Classes:
    TGuiGlobe: Container for the globe interface, managing screen transitions and navigation.

Last updated: 2025-06-14
"""

from typing import Dict, Type, Optional
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout
import sys
import os
from gui.globe.gui__globe_top import TGuiGlobeTopPanel
from gui.gui_core import TGuiCoreScreen
from gui.theme_manager import XcomTheme

# Add parent directory to path for imports to work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

class TGuiGlobe(QWidget):
    """
    Main globe GUI container that manages screens and navigation.
    Inherits from QWidget.
    """

    def __init__(self, parent=None):
        """
        Initialize the globe GUI with top panel and screen container.

        Args:
            parent: Parent widget.
        """
        super().__init__(parent)

        # Set up the layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Create top panel
        self.top_panel = TGuiGlobeTopPanel()
        self.top_panel.screen_changed.connect(self._handle_screen_change)

        # Create screen container
        self.screen_container = QWidget()
        self.screen_container.setStyleSheet(f"background: {XcomTheme.BG_MID};")
        self.screen_layout = QVBoxLayout(self.screen_container)
        self.screen_layout.setContentsMargins(0, 0, 0, 0)
        self.screen_layout.setSpacing(0)

        # Add widgets to layout
        self.layout.addWidget(self.top_panel)
        self.layout.addWidget(self.screen_container)

        # Screen management
        self.screens: Dict[str, TGuiCoreScreen] = {}
        self.current_screen: Optional[TGuiCoreScreen] = None
        self.current_screen_name: str = ""

    def register_screen(self, screen_name: str, screen_widget: TGuiCoreScreen):
        """
        Register a screen widget with a name.

        Args:
            screen_name: The name of the screen (must match one from TopPanelWidget screens)
            screen_widget: The widget to show for this screen
        """
        self.screens[screen_name] = screen_widget
        screen_widget.setParent(self.screen_container)
        screen_widget.hide()  # Initially hidden

    def _handle_screen_change(self, screen_name: str):
        """
        Handle screen change when user clicks on a screen button.

        Args:
            screen_name: The name of the new screen to display
        """
        if screen_name not in self.screens:
            print(f"Screen '{screen_name}' not registered")
            return

        # Deactivate current screen
        if self.current_screen:
            self.current_screen.screen_deactivated()
            self.current_screen.hide()

        # Activate new screen
        self.current_screen = self.screens[screen_name]
        self.current_screen_name = screen_name
        self.current_screen.screen_activated()
        self.current_screen.show()

        # Make sure it fills the container
        self.screen_layout.addWidget(self.current_screen)

        print(f"Switched to globe screen: {screen_name}")

    def set_initial_screen(self, screen_name: str):
        """
        Set the initial screen to display.

        Args:
            screen_name: The name of the screen to display initially
        """
        if screen_name in self.screens:
            self._handle_screen_change(screen_name)
            self.top_panel.set_screen(screen_name)
        else:
            print(f"Cannot set initial screen: '{screen_name}' not registered")


def create_globe_gui() -> TGuiGlobe:
    """
    Create and initialize the globe GUI.

    Returns:
        TGuiGlobe: The initialized globe GUI instance
    """
    globe_gui = TGuiGlobe()
    return globe_gui
