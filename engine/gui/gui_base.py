from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QSizePolicy
)
from PySide6.QtCore import Qt

class BaseScreen(QWidget):
    def __init__(self, switch_screen_callback):
        super().__init__()
        self.switch_screen_callback = switch_screen_callback
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)

        # Left: Base grid (6x6 for demo, adjust as needed)
        grid_widget = QWidget()
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setSpacing(2)
        for row in range(6):
            for col in range(6):
                cell = QLabel()
                cell.setFixedSize(64, 64)
                cell.setStyleSheet("background-color: #7a6a3a; border: 1px solid #c2b97b;")
                grid_layout.addWidget(cell, row, col)
        main_layout.addWidget(grid_widget, stretch=3)

        # Right: Info and buttons
        right_panel = QVBoxLayout()
        # Title
        title = QLabel("Bundy Base")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignLeft)
        right_panel.addWidget(title)
        # Subtitle/info
        subtitle = QLabel("North America\nFUNDS $2574039")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignLeft)
        right_panel.addWidget(subtitle)
        # Small icon row (3 icons, rest empty)
        icon_row = QHBoxLayout()
        for i in range(3):
            icon = QLabel()
            icon.setFixedSize(32, 32)
            icon.setStyleSheet("background-color: #c2b97b; border: 1px solid #7a6a3a;")
            icon_row.addWidget(icon)
        for i in range(5):
            spacer = QLabel()
            spacer.setFixedSize(32, 32)
            icon_row.addWidget(spacer)
        right_panel.addLayout(icon_row)
        # Action buttons
        actions = [
            "BUILD NEW BASE", "BASE INFORMATION", "SOLDIERS", "EQUIP CRAFT",
            "BUILD FACILITIES", "RESEARCH", "MANUFACTURE", "TRANSFER",
            "PURCHASE/RECRUIT", "SELL/SACK", "GEOSCAPE"
        ]
        for action in actions:
            btn = QPushButton(action)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            right_panel.addWidget(btn)
        right_panel.addStretch()
        main_layout.addLayout(right_panel, stretch=1)