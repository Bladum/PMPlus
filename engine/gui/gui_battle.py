from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class BattleScreen(QWidget):
    def __init__(self, switch_screen):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(QLabel("<h2>Land Battle</h2>"))
        btn_back = QPushButton("Back to Main Menu")
        layout.addWidget(btn_back)
        btn_back.clicked.connect(lambda: switch_screen('main_menu'))

