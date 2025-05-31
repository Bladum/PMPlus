"""
XCOM Base Management Demo

This demo shows how to use the BaseGUI class with various screens.
"""

import sys
import os

from gui.gui_base import TGuiBaseScreen, TGuiBase

# Add parent directory to path for imports to work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PySide6.QtWidgets import QApplication, QMainWindow
from syf.theme_styles import XcomStyle, SCALED_WIDTH, SCALED_HEIGHT

class PlaceholderScreen(TGuiBaseScreen):
    """A placeholder screen for screens not yet implemented."""

    def __init__(self, name, parent=None):
        super().__init__(parent)
        from PySide6.QtWidgets import QLabel, QVBoxLayout
        from PySide6.QtCore import Qt

        self.name = name

        layout = QVBoxLayout(self)
        label = QLabel(f"{name} screen not implemented yet")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

def main():
    """Run the XCOM base management demo application."""
    app = QApplication(sys.argv)

    # Apply the global stylesheet to the entire application
    app.setStyleSheet(XcomStyle.get_global_stylesheet())

    # Create main window
    win = QMainWindow()
    win.setWindowTitle("XCOM Base Management v1.0")
    win.setFixedSize(SCALED_WIDTH, SCALED_HEIGHT)

    # Create base GUI
    base_gui = TGuiBase()

    # Register screens
    base_gui.register_screen("BARRACKS", TGuiBaseScreen())

    # Register placeholder screens for other screens
    for screen_name in ["GEO", "BUILD", "HANGAR", "STORAGE", "TRANSFER",
                        "PRISON", "ACADEMY", "WORKSHOP", "LAB", "MARKET",
                        "ARCHIVE", "INFO"]:
        base_gui.register_screen(screen_name, PlaceholderScreen(screen_name))

    # Set initial screen
    base_gui.set_initial_screen("BARRACKS")

    # Set as central widget
    win.setCentralWidget(base_gui)
    win.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
