"""
Top Panel Widget for XCOM Inventory System

This module contains the TopPanelWidget class which handles the creation and management
of the top navigation panel, including screen selection buttons, base selection,
and information displays.
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
                              QButtonGroup, QGridLayout, QLabel)

from gui.other.theme_manager import px, XcomTheme, GRID, XcomStyle


class TGuiBaseTopPanel(QWidget):
    """
    Widget for managing the top navigation panel of the XCOM inventory interface.

    Handles screen selection, base switching, and information displays.
    Emits signals when screen or base selection changes.
    """
    # Define signals
    screen_changed = Signal(str)
    base_changed = Signal(int)

    def __init__(self, parent=None):
        """Initialize the top panel widget with all components."""
        super().__init__(parent)

        # Set fixed height and styling
        self.setFixedHeight(px(GRID * 2))
        self.setStyleSheet(f"background: {XcomTheme.BG_DARK};")

        # Initialize state variables
        self.current_screen = "BARRACKS"  # Default screen

        # Available screens - only BARRACKS is functional initially
        self.available_screens = [
            "GEO", "BUILD", "BARRACKS", "HANGAR", "STORAGE", "TRANSFER",
            "PRISON", "ACADEMY", "WORKSHOP", "LAB", "MARKET", "ARCHIVE", "INFO"
        ]

        # Set up the UI components
        self._setup_ui()

    def _setup_ui(self):
        """Create all UI components for the top panel."""
        # Main horizontal layout to combine all sections
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create the three main components
        screen_layout = self._create_screen_buttons()
        base_layout = self._create_base_buttons()
        info_layout = self._create_info_labels()

        # Add layouts to main layout with proportional spacing
        main_layout.addLayout(screen_layout, 26)
        main_layout.addLayout(base_layout, 6)
        main_layout.addLayout(info_layout, 12)

        self.setLayout(main_layout)

    def _create_screen_buttons(self):
        """Create screen selection button panel."""
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.screen_button_group = QButtonGroup(self)
        self.screen_button_group.setExclusive(True)
        self.screen_buttons = {}

        for label in self.available_screens:
            btn = QPushButton(label)
            btn.setFixedSize(px(GRID * 2 - 2), px(GRID * 2 - 2))
            btn.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_NORMAL))
            btn.setCheckable(True)

            # Set initial state
            if label == self.current_screen:
                btn.setChecked(True)
                btn.setProperty("class", "screen_active")
                btn.setStyleSheet(XcomStyle.pushbutton_screen_active())
            else:
                btn.setStyleSheet(XcomStyle.pushbutton(rounded=True, border_width=2))

            # Connect button click
            btn.clicked.connect(lambda checked, name=label: self._handle_screen_button_click(name))

            self.screen_button_group.addButton(btn)
            self.screen_buttons[label] = btn
            layout.addWidget(btn)

        return layout

    def _create_base_buttons(self):
        """Create base selection button grid."""
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.base_buttons = []

        for idx in range(12):  # 12 bases total
            btn = QPushButton(str(idx + 1))  # Display 1-12
            btn.setFixedSize(px(GRID), px(GRID))
            btn.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_NORMAL))

            # Set button style based on base status
            status = GameData.get_base_status(idx)
            if status == 'active':
                btn.setProperty("class", "base_active")
                btn.setStyleSheet(XcomStyle.pushbutton_base_active())
            elif status == 'available':
                btn.setProperty("class", "base_available")
                btn.setStyleSheet(XcomStyle.pushbutton_base_available())
            else:  # disabled
                btn.setProperty("class", "base_disabled")
                btn.setStyleSheet(XcomStyle.pushbutton_base_disabled())
                btn.setEnabled(False)

            # Connect button click
            if status != 'disabled':
                btn.clicked.connect(lambda checked, i=idx: self._handle_base_button_click(i))

            row = 0 if idx < 6 else 1  # 2 rows of 6
            col = idx if idx < 6 else idx - 6
            layout.addWidget(btn, row, col)
            self.base_buttons.append(btn)

        return layout

    def _create_info_labels(self):
        """Create information labels section."""
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        active_base = GameData.get_active_base()
        current_date = "MAY 30, 2025"
        current_money = "$3,500,000"

        self.base_info_label = QLabel(active_base.name)
        self.base_info_label.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_LARGE))
        self.base_info_label.setStyleSheet(f"color: {XcomTheme.ACCENT_YELLOW}; background: transparent; padding: 0px; margin: 0px;")
        self.base_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)

        date_label = QLabel(current_date)
        date_label.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_NORMAL))
        date_label.setStyleSheet(f"color: {XcomTheme.TEXT_BRIGHT}; background: transparent; padding: 0px; margin: 0px;")
        date_label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)

        money_label = QLabel(current_money)
        money_label.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_NORMAL))
        money_label.setStyleSheet(f"color: {XcomTheme.ACCENT_GREEN}; background: transparent; padding: 0px; margin: 0px;")
        money_label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)

        layout.addWidget(self.base_info_label, 0, 0, 1, 4)
        layout.addWidget(date_label, 1, 0, 1, 2)
        layout.addWidget(money_label, 1, 2, 1, 2)

        return layout

    def _handle_screen_button_click(self, screen_name: str) -> None:
        """
        Handle screen button clicks with visual feedback.

        Args:
            screen_name: Name of the selected screen
        """
        # Update internal state
        self.current_screen = screen_name

        # Update button styles
        for name, button in self.screen_buttons.items():
            if name == screen_name:
                button.setProperty("class", "screen_active")
                button.setStyleSheet(XcomStyle.pushbutton_screen_active())
            else:
                button.setProperty("class", "")
                button.setStyleSheet(XcomStyle.pushbutton(rounded=True, border_width=2))

        # Emit signal for screen change
        self.screen_changed.emit(screen_name)
        print(f"Switched to screen: {screen_name}")

    def _handle_base_button_click(self, base_index: int) -> None:
        """
        Handle base button clicks with visual feedback.

        Args:
            base_index: Zero-based index of the selected base
        """
        if self._switch_base(base_index):
            # Update all button styles
            for i, button in enumerate(self.base_buttons):
                status = GameData.get_base_status(i)
                if status == 'active':
                    button.setProperty("class", "base_active")
                    button.setStyleSheet(XcomStyle.pushbutton_base_active())
                elif status == 'available':
                    button.setProperty("class", "base_available")
                    button.setStyleSheet(XcomStyle.pushbutton_base_available())

    def _switch_base(self, base_index: int) -> bool:
        """
        Handle base switching with data refresh.

        Args:
            base_index: Zero-based index of the base to switch to

        Returns:
            True if base switch was successful, False otherwise
        """
        if GameData.set_active_base(base_index):
            self._update_base_display()
            # Emit signal for base change
            self.base_changed.emit(base_index)
            print(f"Switched to base: {GameData.BASES[base_index].name}")
            return True
        return False

    def _update_base_display(self) -> None:
        """Update base name label for the current active base."""
        active_base = GameData.get_active_base()
        self.base_info_label.setText(active_base.name)

    # Public methods for external use
    def get_current_screen(self) -> str:
        """Get the currently selected screen name."""
        return self.current_screen

    def set_screen(self, screen_name: str) -> bool:
        """
        Programmatically set the current screen.

        Args:
            screen_name: Name of the screen to select

        Returns:
            True if successful, False if screen name is invalid
        """
        if screen_name in self.available_screens:
            self._handle_screen_button_click(screen_name)
            return True
        return False

    def update_date_display(self, date_str: str) -> None:
        """Update the date display with the provided string."""
        if hasattr(self, 'date_label') and self.date_label:
            self.date_label.setText(date_str)

    def update_money_display(self, money_str: str) -> None:
        """Update the money display with the provided string."""
        if hasattr(self, 'money_label') and self.money_label:
            self.money_label.setText(money_str)
