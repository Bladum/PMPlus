from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel

class MainMenuScreen(QWidget):
    def __init__(self, switch_screen):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        label = QLabel("XCOM Main Menu")
        label.setStyleSheet("font-size: 12px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(label)
        btn_start = QPushButton("Start Game")
        btn_load = QPushButton("Load Game")
        btn_options = QPushButton("Options")
        btn_exit = QPushButton("Exit")
        layout.addWidget(btn_start)
        layout.addWidget(btn_load)
        layout.addWidget(btn_options)
        layout.addWidget(btn_exit)
        btn_start.clicked.connect(lambda: switch_screen('base'))
        btn_load.clicked.connect(lambda: switch_screen('base'))  # Placeholder for load screen
        btn_options.clicked.connect(lambda: switch_screen('dashboard'))  # Placeholder for options screen
        btn_exit.clicked.connect(lambda: exit())

