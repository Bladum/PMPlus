import os
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PySide6.QtGui import QColor, QPalette
from PySide6.QtCore import Qt
import sys
from gui_main_menu import MainMenuScreen
from gui_base import BaseScreen
from gui_pedia import PediaScreen
from gui_globe import GlobeScreen
from gui_options import OptionsScreen
from gui_battle import BattleScreen
from gui_dashboard import DashboardScreen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("XCOM GUI")
        self.setFixedSize(320, 200)  # Set window to 320x200, classic retro resolution
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self.screens = {}
        self.set_xcom_theme()
        self.init_screens()
        self.switch_screen('main_menu')

    def set_xcom_theme(self):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(16, 24, 32))  # Deep blue/black
        palette.setColor(QPalette.WindowText, QColor(0, 255, 128))  # Greenish text
        palette.setColor(QPalette.Base, QColor(24, 32, 40))
        palette.setColor(QPalette.AlternateBase, QColor(32, 48, 64))
        palette.setColor(QPalette.ToolTipBase, QColor(0, 255, 128))
        palette.setColor(QPalette.ToolTipText, QColor(16, 24, 32))
        palette.setColor(QPalette.Text, QColor(0, 255, 128))
        palette.setColor(QPalette.Button, QColor(24, 32, 40))
        palette.setColor(QPalette.ButtonText, QColor(0, 255, 128))
        palette.setColor(QPalette.BrightText, QColor(255, 255, 0))
        palette.setColor(QPalette.Highlight, QColor(0, 255, 128))
        palette.setColor(QPalette.HighlightedText, QColor(16, 24, 32))
        self.setPalette(palette)
        self.setStyleSheet('''
            QWidget {
                background-color: #101820;
                color: #00ff80;
                font-family: "Consolas", "Courier New", monospace;
                font-size: 8px;
            }
            QPushButton {
                background-color: #182028;
                color: #00ff80;
                border: 1px solid #00ff80;
                border-radius: 2px;
                padding: 1px 4px;
                font-size: 9px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #223040;
                color: #ffff00;
                border: 1px solid #ffff00;
            }
            QLabel#title {
                color: #ffff00;
                font-size: 10px;
                font-weight: bold;
            }
            QLabel#subtitle {
                color: #00ff80;
                font-size: 8px;
            }
            QHeaderView::section {
                background-color: #223040;
                color: #00ff80;
                font-weight: bold;
                border: 1px solid #00ff80;
                font-size: 8px;
            }
            QTableWidget {
                background-color: #101820;
                color: #00ff80;
                gridline-color: #00ff80;
                font-size: 8px;
            }
            QListWidget {
                background-color: #101820;
                color: #00ff80;
                border: 1px solid #00ff80;
                font-size: 8px;
            }
            QLabel {
                color: #00ff80;
                font-size: 8px;
            }
        ''')

    def init_screens(self):
        self.screens['main_menu'] = MainMenuScreen(self.switch_screen)
        self.screens['base'] = BaseScreen(self.switch_screen)
        self.screens['pedia'] = PediaScreen(self.switch_screen)
        self.screens['globe'] = GlobeScreen(self.switch_screen)
        self.screens['options'] = OptionsScreen(self.switch_screen)
        self.screens['battle'] = BattleScreen(self.switch_screen)
        self.screens['dashboard'] = DashboardScreen(self.switch_screen, date="2025-05-26", money=1234)
        for screen in self.screens.values():
            self.stack.addWidget(screen)

    def switch_screen(self, name):
        widget = self.screens.get(name)
        if widget:
            self.stack.setCurrentWidget(widget)

def run_gui():
    os.environ["QT_SCALE_FACTOR"] = "4.0"  # Force scale of all widgets to 2.0
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run_gui()

