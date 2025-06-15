"""
XCOM GUI Module: gui_archive.py

Archive Screen GUI for research and records management.

Classes:
    TGuiArchive: Main archive GUI screen for research/records interface.

Last updated: 2025-06-11
"""

from gui.gui_core import TGuiCoreScreen


class TGuiArchive(TGuiCoreScreen):
    """
    Archive screen for research and records.
    Inherits from TGuiCoreScreen.
    """

    def __init__(self, parent=None):
        """
        Initialize the Archive GUI screen.

        Args:
            parent (QWidget, optional): Parent widget for the screen.
        """
        super().__init__(parent)
