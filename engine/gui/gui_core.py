from PySide6.QtWidgets import QWidget


class TGuiCoreScreen(QWidget):
    """Base class for all screen widgets that can be displayed in the BaseGUI."""

    def __init__(self, parent=None):
        """Initialize the base screen widget."""
        super().__init__(parent)
        self.setStyleSheet(f"background: {XcomTheme.BG_MID};")

    def screen_activated(self):
        """Called when this screen becomes active."""
        pass

    def screen_deactivated(self):
        """Called when another screen becomes active."""
        pass

    def refresh_base_data(self):
        """Refresh data when base changes."""
        pass

    def update_summary_display(self):
        """Update summary data displays."""
        pass
