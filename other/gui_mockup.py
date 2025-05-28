import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QStackedWidget, QSizePolicy
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import os

SCALE = 4
BASE_WIDTH = 320
BASE_HEIGHT = 200
SCALED_WIDTH = BASE_WIDTH * SCALE
SCALED_HEIGHT = BASE_HEIGHT * SCALE

# Map section names to image filenames
SECTIONS = [
    ("Battlescape", "battle.png"),
    ("Units", "units.png"),
    ("Crafts", "crafts.png"),
    ("Prison", "prison.png"),
    ("Training", "training.png"),
    ("Hospital", "hospital.png"),
    ("Archive", "archive.png"),
    ("Research", "research.png"),
    ("Manufacturing", "manufacturing.png"),
    ("Market", "market.png"),
    ("Facilities", "facility.png"),
    ("Storage", "storage.png"),
    ("Transfers", "transfer.png"),
    ("Base info", "base_info.png"),
]

class ImagePanel(QWidget):
    def __init__(self, image_path):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel(self)
        label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(SCALED_WIDTH, SCALED_HEIGHT, Qt.KeepAspectRatio, Qt.FastTransformation)
            label.setPixmap(pixmap)
        else:
            label.setText(f"Image not found: {image_path}")
        layout.addWidget(label)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("XCOM GUI Mockup")
        self.setFixedSize(SCALED_WIDTH, SCALED_HEIGHT)
        central = QWidget()
        main_layout = QHBoxLayout(central)
        # Sidebar for navigation
        sidebar = QVBoxLayout()
        self.stack = QStackedWidget()
        self.panels = []
        for i, (name, img) in enumerate(SECTIONS):
            btn = QPushButton(name)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.clicked.connect(lambda checked, idx=i: self.stack.setCurrentIndex(idx))
            sidebar.addWidget(btn)
            img_path = os.path.join(os.path.dirname(__file__), "wiki", "gui", img)
            panel = ImagePanel(img_path)
            self.stack.addWidget(panel)
            self.panels.append(panel)
        sidebar.addStretch(1)
        main_layout.addLayout(sidebar, 1)
        main_layout.addWidget(self.stack, 4)
        self.setCentralWidget(central)
        self.stack.setCurrentIndex(0)

def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

