"""
Widget for managing the top navigation panel of the XCOM inventory interface.

This class implements the top navigation bar for the game interface,
providing screen switching between different game views (Barracks, Hangar, etc.)
and world selection functionality. It displays critical game information
like current world, date, and available funds.

Interactions:
- Used by TGuiBase as the main navigation system
- Emits signals when users change screens or worlds
- Connects to GameData to retrieve world and financial information
- Provides visual feedback for current screen and world selection
- Updates when game state changes (funds, etc.)

Key Features:
- Screen selection buttons with visual active state
- World selection grid for different planets/locations
- End turn button to progress game time
- Information display for current world, date, and funds
- Consistent theming via TThemeManager styling system
- Signal-based communication with parent interfaces
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
                              QButtonGroup, QGridLayout, QLabel)

from gui.other.theme_manager import px, XcomTheme, GRID, XcomStyle


class TGuiGlobeTopPanel(QWidget):


    # Define signals
    screen_changed = Signal(str)
    world_changed = Signal(str)
    end_turn_clicked = Signal()

    def __init__(self, parent=None):
        """Initialize the top panel widget with all components."""
        super().__init__(parent)

        # Set fixed height and styling
        self.setFixedHeight(px(GRID * 2))
        self.setStyleSheet(f"background: {XcomTheme.BG_DARK};")

        # Initialize state variables
        self.current_screen = "MAP"  # Default screen
        self.current_world = "EARTH"  # Default world

        # Available screens
        self.available_screens = [
            "BASE", "MAP", "INTERCEPT", "RESEARCH", "PRODUCTION", "BUDGET",
            "POLICIES", "FACTIONS", "FUDNING", "REPORTS", "PEDIA", "MENU",
        ]

        # Available worlds
        self.available_worlds = ["EARTH", "MOON", "CYBER", "MARS", "3X", "DARK"]

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
        world_layout = self._create_world_controls()
        info_layout = self._create_info_labels()

        # Add layouts to main layout with proportional spacing
        main_layout.addLayout(screen_layout, 26)
        main_layout.addLayout(world_layout, 6)
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

    def _create_world_controls(self):
        """Create world selection buttons and end turn button."""
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create world selection buttons
        self.world_buttons = {}
        self.world_button_group = QButtonGroup(self)
        self.world_button_group.setExclusive(True)

        # Add world buttons (2 rows, 3 columns)
        for i, world_name in enumerate(self.available_worlds):
            btn = QPushButton(world_name)
            row = 0 if i < 3 else 1
            col = i if i < 3 else i - 3

            # Button size is 2x1 grid (larger than base buttons)
            btn.setFixedSize(px(GRID * 2), px(GRID))
            btn.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_NORMAL))
            btn.setCheckable(True)

            # Set initial state
            if world_name == self.current_world:
                btn.setChecked(True)
                btn.setProperty("class", "world_active")
                btn.setStyleSheet(XcomStyle.pushbutton_screen_active())
            else:
                btn.setStyleSheet(XcomStyle.pushbutton(rounded=True, border_width=2))

            # Connect button click
            btn.clicked.connect(lambda checked, name=world_name: self._handle_world_button_click(name))

            self.world_button_group.addButton(btn)
            self.world_buttons[world_name] = btn

            # Add button to layout
            layout.addWidget(btn, row, col)

        # Create END TURN button
        self.end_turn_button = QPushButton("END TURN")
        self.end_turn_button.setFixedSize(px(GRID * 2), px(GRID * 2))
        self.end_turn_button.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_NORMAL))
        self.end_turn_button.setStyleSheet(XcomStyle.pushbutton(bg_color=XcomTheme.ACCENT_RED,
                                                               rounded=True,
                                                               border_width=2))
        self.end_turn_button.clicked.connect(self._handle_end_turn_click)

        # Add END TURN button to layout, spanning both rows
        layout.addWidget(self.end_turn_button, 0, 3, 2, 1)

        return layout

    def _create_info_labels(self):
        """Create information labels section."""
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Current data
        current_date = "JUNE 1, 2025"
        current_money = "$3,500,000"

        # Create world info label (large, prominent text)
        self.world_info_label = QLabel(self.current_world)
        self.world_info_label.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_LARGE))
        self.world_info_label.setStyleSheet(f"color: {XcomTheme.ACCENT_YELLOW}; background: transparent; padding: 0px; margin: 0px;")
        self.world_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)

        # Create date label
        self.date_label = QLabel(current_date)
        self.date_label.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_NORMAL))
        self.date_label.setStyleSheet(f"color: {XcomTheme.TEXT_BRIGHT}; background: transparent; padding: 0px; margin: 0px;")
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)

        # Create money label
        self.money_label = QLabel(current_money)
        self.money_label.setFont(QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_NORMAL))
        self.money_label.setStyleSheet(f"color: {XcomTheme.ACCENT_GREEN}; background: transparent; padding: 0px; margin: 0px;")
        self.money_label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)

        layout.addWidget(self.world_info_label, 0, 0, 1, 4)
        layout.addWidget(self.date_label, 1, 0, 1, 2)
        layout.addWidget(self.money_label, 1, 2, 1, 2)

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

    def _handle_world_button_click(self, world_name: str) -> None:
        """
        Handle world button clicks with visual feedback.

        Args:
            world_name: Name of the selected world
        """
        # Update internal state
        self.current_world = world_name

        # Update button styles
        for name, button in self.world_buttons.items():
            if name == world_name:
                button.setProperty("class", "world_active")
                button.setStyleSheet(XcomStyle.pushbutton_screen_active())
            else:
                button.setProperty("class", "")
                button.setStyleSheet(XcomStyle.pushbutton(rounded=True, border_width=2))

        # Update the world display
        self._update_world_display()

        # Emit signal for world change
        self.world_changed.emit(world_name)
        print(f"Switched to world: {world_name}")

    def _update_world_display(self) -> None:
        """Update world name label for the current world."""
        self.world_info_label.setText(self.current_world)

    def _handle_end_turn_click(self) -> None:
        """Handle the end turn button click."""
        self.end_turn_clicked.emit()
        print("End turn button clicked")

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

    def get_current_world(self) -> str:
        """Get the currently selected world name."""
        return self.current_world

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

    def set_world(self, world_name: str) -> bool:
        """
        Programmatically set the current world.

        Args:
            world_name: Name of the world to select

        Returns:
            True if successful, False if world name is invalid
        """
        if world_name in self.available_worlds:
            self._handle_world_button_click(world_name)
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
