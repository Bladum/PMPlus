import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton
)
from PySide6.QtCore import Qt

SCALE = 4
BASE_WIDTH = 320
BASE_HEIGHT = 240
SCALED_WIDTH = BASE_WIDTH * SCALE
SCALED_HEIGHT = BASE_HEIGHT * SCALE

# Helper to scale pixel values
px = lambda x: x * SCALE

class TopPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(0, 0, px(BASE_WIDTH), px(24))
        self.setStyleSheet("background: #333;")
        # 14 buttons, each 20x20, spaced evenly with minimum spacing
        btn_w, btn_h = 16, 8
        btn_count = 14
        total_btn_width = btn_count * btn_w
        free_space = BASE_WIDTH - total_btn_width
        spacing = free_space // (btn_count + 1)
        y = 2  # vertical margin
        self.buttons = []
        for i in range(btn_count):
            x = spacing + i * (btn_w + spacing)
            btn = QPushButton(f"{i+1}", self)
            btn.setGeometry(px(x), px(y), px(btn_w), px(btn_h))
            btn.setStyleSheet("background: #555; color: #fff; font-size: 12px; border-radius: 2px;")
            self.buttons.append(btn)

class CraftsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Crafts UI")
        self.setFixedSize(SCALED_WIDTH, SCALED_HEIGHT)
        central = QWidget(self)
        central.setStyleSheet("background: #222;")
        self.setCentralWidget(central)
        # Top panel
        self.top_panel = TopPanel(central)
        # The rest of the panel is free for now


def main():
    app = QApplication(sys.argv)
    win = CraftsWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

