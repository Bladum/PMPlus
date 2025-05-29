#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implementation of the Crafts interface based on the crafts.png mockup.
Resolution: 320x240 with x4 scale (1280x960)
"""

import sys
from PySide6.QtCore import Qt, QSize, QRect
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QFontDatabase, QPixmap
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                              QHBoxLayout, QPushButton, QLabel, QGridLayout,
                              QScrollArea, QFrame)

# Constants
ORIGINAL_WIDTH = 320
ORIGINAL_HEIGHT = 240
SCALE_FACTOR = 4
SCALED_WIDTH = ORIGINAL_WIDTH * SCALE_FACTOR
SCALED_HEIGHT = ORIGINAL_HEIGHT * SCALE_FACTOR

# Colors
BACKGROUND_COLOR = QColor(40, 44, 52)  # Dark background
PANEL_COLOR = QColor(60, 63, 65)       # Slightly lighter panel
BUTTON_COLOR = QColor(78, 82, 88)      # Button background
HIGHLIGHT_COLOR = QColor(86, 156, 214) # Highlight blue
TEXT_COLOR = QColor(220, 220, 220)     # Light gray text

# Spacing constants
MARGIN_SIZE = 1 * SCALE_FACTOR
SPACING_SIZE = 2 * SCALE_FACTOR
WIDGET_SPACING = 3 * SCALE_FACTOR

class CraftButton(QPushButton):
    """Custom button for the craft interface with specific styling."""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {BUTTON_COLOR.name()};
                color: {TEXT_COLOR.name()};
                border: 1px solid {HIGHLIGHT_COLOR.name()};
                padding: {4 * SCALE_FACTOR}px;
                font-size: {3 * SCALE_FACTOR}pt;
            }}
            QPushButton:hover {{
                background-color: {HIGHLIGHT_COLOR.darker(120).name()};
            }}
            QPushButton:pressed {{
                background-color: {HIGHLIGHT_COLOR.darker(150).name()};
            }}
        """)
        # Scale font size
        font = self.font()
        font.setPointSize(3 * SCALE_FACTOR)
        self.setFont(font)


class CraftStatusPanel(QFrame):
    """Panel showing craft status information."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet(f"background-color: {PANEL_COLOR.name()}; border: 1px solid {HIGHLIGHT_COLOR.name()};")

        layout = QVBoxLayout(self)
        layout.setSpacing(WIDGET_SPACING)
        layout.setContentsMargins(MARGIN_SIZE, MARGIN_SIZE, MARGIN_SIZE, MARGIN_SIZE)

        # Create status information labels
        self.craftName = QLabel("FIRESTORM-1")
        self.craftName.setStyleSheet(f"color: {TEXT_COLOR.name()}; font-size: {4 * SCALE_FACTOR}pt; font-weight: bold;")

        self.craftStatus = QLabel("Status: Ready")
        self.craftStatus.setStyleSheet(f"color: {TEXT_COLOR.name()}; font-size: {3 * SCALE_FACTOR}pt;")

        self.craftLocation = QLabel("Location: Hangar 1")
        self.craftLocation.setStyleSheet(f"color: {TEXT_COLOR.name()}; font-size: {3 * SCALE_FACTOR}pt;")

        self.fuelStatus = QLabel("Fuel: 100%")
        self.fuelStatus.setStyleSheet(f"color: {TEXT_COLOR.name()}; font-size: {3 * SCALE_FACTOR}pt;")

        self.damageStatus = QLabel("Damage: 0%")
        self.damageStatus.setStyleSheet(f"color: {TEXT_COLOR.name()}; font-size: {3 * SCALE_FACTOR}pt;")

        # Add to layout
        layout.addWidget(self.craftName)
        layout.addWidget(self.craftStatus)
        layout.addWidget(self.craftLocation)
        layout.addWidget(self.fuelStatus)
        layout.addWidget(self.damageStatus)
        layout.addStretch()


class CraftItemPanel(QFrame):
    """Panel showing craft weapon/equipment."""
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet(f"background-color: {PANEL_COLOR.name()}; border: 1px solid {HIGHLIGHT_COLOR.name()};")

        layout = QVBoxLayout(self)
        layout.setSpacing(WIDGET_SPACING)
        layout.setContentsMargins(MARGIN_SIZE, MARGIN_SIZE, MARGIN_SIZE, MARGIN_SIZE)

        # Title label
        titleLabel = QLabel(title)
        titleLabel.setStyleSheet(f"color: {HIGHLIGHT_COLOR.name()}; font-size: {3 * SCALE_FACTOR}pt; font-weight: bold;")

        # Item status (empty or equipped)
        self.itemStatus = QLabel("No item equipped")
        self.itemStatus.setStyleSheet(f"color: {TEXT_COLOR.name()}; font-size: {3 * SCALE_FACTOR}pt;")
        self.itemStatus.setAlignment(Qt.AlignCenter)

        # Add to layout
        layout.addWidget(titleLabel)
        layout.addWidget(self.itemStatus)
        layout.addStretch()


class CraftCrewPanel(QFrame):
    """Panel showing craft crew members."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet(f"background-color: {PANEL_COLOR.name()}; border: 1px solid {HIGHLIGHT_COLOR.name()};")

        layout = QVBoxLayout(self)
        layout.setSpacing(WIDGET_SPACING)
        layout.setContentsMargins(MARGIN_SIZE, MARGIN_SIZE, MARGIN_SIZE, MARGIN_SIZE)

        # Title label
        titleLabel = QLabel("CREW")
        titleLabel.setStyleSheet(f"color: {HIGHLIGHT_COLOR.name()}; font-size: {3 * SCALE_FACTOR}pt; font-weight: bold;")
        layout.addWidget(titleLabel)

        # Create some sample crew entries
        for i in range(4):
            crewMember = QLabel(f"[Empty]" if i > 1 else f"Agent {i+1}")
            crewMember.setStyleSheet(f"color: {TEXT_COLOR.name()}; font-size: {3 * SCALE_FACTOR}pt;")
            layout.addWidget(crewMember)

        layout.addStretch()


class CraftsInterface(QMainWindow):
    """Main window for the crafts interface."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("XCOM - Craft Management")
        self.setFixedSize(SCALED_WIDTH, SCALED_HEIGHT)

        # Central widget
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        mainLayout = QVBoxLayout(centralWidget)
        mainLayout.setSpacing(SPACING_SIZE)
        mainLayout.setContentsMargins(MARGIN_SIZE, MARGIN_SIZE, MARGIN_SIZE, MARGIN_SIZE)

        # Top panel with buttons
        topPanel = QWidget()
        topLayout = QHBoxLayout(topPanel)
        topLayout.setSpacing(SPACING_SIZE)
        topLayout.setContentsMargins(0, 0, 0, 0)

        # Create top buttons
        buttons = ["HANGAR", "EQUIP", "TRANSFER", "RENAME", "NEW", "DISMISS"]
        for text in buttons:
            button = CraftButton(text)
            topLayout.addWidget(button)

        mainLayout.addWidget(topPanel)

        # Main content area
        contentArea = QWidget()
        contentLayout = QHBoxLayout(contentArea)
        contentLayout.setSpacing(SPACING_SIZE)
        contentLayout.setContentsMargins(0, 0, 0, 0)

        # Left panel for craft list
        leftPanel = QFrame()
        leftPanel.setFrameShape(QFrame.StyledPanel)
        leftPanel.setStyleSheet(f"background-color: {PANEL_COLOR.name()}; border: 1px solid {HIGHLIGHT_COLOR.name()};")
        leftLayout = QVBoxLayout(leftPanel)
        leftLayout.setSpacing(WIDGET_SPACING)
        leftLayout.setContentsMargins(MARGIN_SIZE, MARGIN_SIZE, MARGIN_SIZE, MARGIN_SIZE)

        leftTitle = QLabel("AVAILABLE CRAFT")
        leftTitle.setStyleSheet(f"color: {HIGHLIGHT_COLOR.name()}; font-size: {3 * SCALE_FACTOR}pt; font-weight: bold;")
        leftLayout.addWidget(leftTitle)

        # Sample craft list
        craft_names = ["FIRESTORM-1", "SKYRANGER-1", "INTERCEPTOR-1", "AVENGER-1"]
        for craft in craft_names:
            craftButton = QPushButton(craft)
            craftButton.setStyleSheet(f"""
                QPushButton {{
                    text-align: left;
                    background-color: {PANEL_COLOR.name()};
                    color: {TEXT_COLOR.name()};
                    border: none;
                    padding: {2 * SCALE_FACTOR}px;
                    font-size: {3 * SCALE_FACTOR}pt;
                }}
                QPushButton:hover {{
                    background-color: {HIGHLIGHT_COLOR.darker(150).name()};
                }}
            """)
            leftLayout.addWidget(craftButton)

        leftLayout.addStretch()

        # Right panel for craft details
        rightPanel = QWidget()
        rightLayout = QVBoxLayout(rightPanel)
        rightLayout.setSpacing(SPACING_SIZE)
        rightLayout.setContentsMargins(MARGIN_SIZE, MARGIN_SIZE, MARGIN_SIZE, MARGIN_SIZE)

        # Craft status panel
        statusPanel = CraftStatusPanel()
        rightLayout.addWidget(statusPanel)

        # Weapon panels
        weaponsLayout = QHBoxLayout()
        weaponsLayout.setSpacing(SPACING_SIZE)
        weaponsLayout.setContentsMargins(0, 0, 0, 0)
        weaponPanel1 = CraftItemPanel("WEAPON 1")
        weaponPanel2 = CraftItemPanel("WEAPON 2")
        weaponsLayout.addWidget(weaponPanel1)
        weaponsLayout.addWidget(weaponPanel2)
        rightLayout.addLayout(weaponsLayout)

        # Equipment and crew panels
        bottomLayout = QHBoxLayout()
        bottomLayout.setSpacing(SPACING_SIZE)
        bottomLayout.setContentsMargins(0, 0, 0, 0)
        equipmentPanel = CraftItemPanel("EQUIPMENT")
        crewPanel = CraftCrewPanel()
        bottomLayout.addWidget(equipmentPanel)
        bottomLayout.addWidget(crewPanel)
        rightLayout.addLayout(bottomLayout)

        # Add panels to content layout
        contentLayout.addWidget(leftPanel, 1)
        contentLayout.addWidget(rightPanel, 2)

        mainLayout.addWidget(contentArea)

        # Bottom status bar
        self.statusBar = QLabel("Ready - Craft management system active")
        self.statusBar.setStyleSheet(f"background-color: {BUTTON_COLOR.name()}; color: {TEXT_COLOR.name()}; padding: {2 * SCALE_FACTOR}px; font-size: {2 * SCALE_FACTOR}pt;")
        mainLayout.addWidget(self.statusBar)

        # Set the background color for the whole window
        self.setStyleSheet(f"background-color: {BACKGROUND_COLOR.name()};")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Try to load a pixelated font for retro look
    QFontDatabase.addApplicationFont("pixelated.ttf")  # If available
    window = CraftsInterface()
    window.show()
    sys.exit(app.exec())
