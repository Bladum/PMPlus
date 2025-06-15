"""
XCOM GUI Module: gui_base.py

Main base GUI class that manages screens and navigation for the XCOM game.

Classes:
    TGuiBase: Foundational container for the game's interface, managing screen transitions and navigation.

Last updated: 2025-06-14
"""

from typing import Dict, Type, Optional
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout
import sys
import os
from gui.base.gui__base_top import TGuiBaseTopPanel
from gui.gui_core import TGuiCoreScreen
from gui.theme_manager import XcomTheme

# Add parent directory to path for imports to work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

class TGuiBase(QWidget):
    """
    Main base GUI class that manages screens and navigation for the XCOM game.
    Acts as a coordinator between different specialized screen interfaces.
    Inherits from QWidget.
    """

    def __init__(self, parent=None):
        """
        Initialize the base GUI with top panel and screen container.

        Args:
            parent: Parent widget.
        """
        super().__init__(parent)

        # Set up the layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Create top panel
        self.top_panel = TGuiBaseTopPanel()
        self.top_panel.screen_changed.connect(self._handle_screen_change)
        self.top_panel.base_changed.connect(self._handle_base_change)

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

        print(f"Switched to screen: {screen_name}")

    def _handle_base_change(self, base_index: int):
        """
        Handle base change when user switches to a different base.

        Args:
            base_index: The index of the new base
        """
        # Refresh data in all screens
        for screen in self.screens.values():
            screen.refresh_base_data()

        # Update summary display in current screen
        if self.current_screen:
            self.current_screen.update_summary_display()

        print(f"Base changed to index: {base_index}")

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


def create_base_gui() -> TGuiBase:
    """
    Create and initialize the base GUI.

    Returns:
        TGuiBase: The initialized base GUI instance
    """
    base_gui = TGuiBase()
    # Register available screens here (will be done by specific implementation)
    return base_gui
