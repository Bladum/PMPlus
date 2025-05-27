from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QStackedWidget, QSizePolicy
from PySide6.QtCore import Qt

class DashboardScreen(QWidget):
    def __init__(self, switch_screen, date="2023-12-11", money=1234):
        super().__init__()
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(8)

        # Top bar
        top_bar = QHBoxLayout()
        top_bar.setSpacing(8)
        date_label = QLabel(f"DATE: {date}")
        date_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        date_label.setStyleSheet("font-size: 8px; font-weight: bold;")
        money_label = QLabel(f"MONEY: {money}$")
        money_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        money_label.setStyleSheet("font-size: 8px; font-weight: bold;")
        top_bar.addWidget(date_label)
        top_bar.addStretch()
        top_bar.addWidget(money_label)
        main_layout.addLayout(top_bar)

        # Main content area
        content_layout = QHBoxLayout()
        content_layout.setSpacing(8)

        # Left menu/list
        left_menu = QListWidget()
        left_menu.addItems(["BASES", "CRAFT", "RESEARCH", "MANUFACTURE", "TRANSFER", "UFOPAEDIA", "OPTIONS"])
        left_menu.setFixedWidth(120)
        left_menu.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        content_layout.addWidget(left_menu)

        # Central stacked area (placeholder for now)
        self.central_stack = QStackedWidget()
        placeholder = QLabel("Main Content Area\n(Select from left menu)")
        placeholder.setAlignment(Qt.AlignCenter)
        self.central_stack.addWidget(placeholder)
        content_layout.addWidget(self.central_stack, 1)

        main_layout.addLayout(content_layout, 1)

        # Optionally connect left_menu to switch screens in the stack
        # left_menu.currentRowChanged.connect(self.central_stack.setCurrentIndex)

