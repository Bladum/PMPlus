"""
XCOM Inventory System - Main Application Entry Point

This module serves as the primary entry point for the XCOM Inventory Management System.
It initializes the PySide6 application, applies the global XCOM theme, creates the main
window, and launches the complete inventory management interface.

Key Features:
- Application initialization and configuration
- Global theme application using XcomStyle
- Main window setup with proper dimensions
- Integration of all system components
- Cross-platform compatibility handling
- Error handling for application lifecycle

Components Initialized:
- QApplication: Main application object with event loop
- QMainWindow: Primary application window container
- Main Interface: Complete inventory management UI
- Global Styling: XCOM-themed visual appearance

The application provides a complete XCOM-style inventory management system including:
- Unit management and equipment assignment
- Item categorization and filtering
- Equipment slot management
- Template saving and loading
- Multi-base inventory tracking
- Drag-and-drop equipment assignment

Dependencies:
- PySide6: Qt framework for Python GUI development
- theme_styles: Application theming and styling system
- main_interface: Core UI components and functionality
- Supporting modules: game_data, inventory_system, custom_widgets

Usage:
    Run this file directly to start the application:
    $ python xcom_inventory_main.py

Author: XCOM Inventory System
Version: 1.0
License: MIT
"""

import sys
import os
from typing import NoReturn
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt

# Add current directory to path so imports work properly across different environments
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import application-specific modules
from theme_styles import XcomStyle, SCALED_WIDTH, SCALED_HEIGHT
from main_interface import create_main_interface


def main() -> NoReturn:
    """
    Main application entry point and initialization.
    
    This function initializes the PySide6 application, applies the global XCOM theme,
    creates and configures the main window, sets up the complete inventory interface,
    and starts the application event loop.
    
    The function performs the following initialization steps:
    1. Creates QApplication instance with command line arguments
    2. Applies global XCOM stylesheet for consistent theming
    3. Creates and configures main window with proper dimensions
    4. Initializes the complete inventory management interface
    5. Displays the window and starts the event loop
    
    Window Configuration:
    - Title: "XCOM UI Enhanced - Complete Inventory System"
    - Size: Fixed dimensions based on SCALED_WIDTH x SCALED_HEIGHT
    - Theme: Complete XCOM military/tactical styling
    
    Raises:
        SystemExit: When the application is closed (normal behavior)
        
    Note:
        This function does not return as it calls sys.exit() to terminate
        the application when the window is closed.
    """
    # Initialize PySide6 application with command line arguments
    app = QApplication(sys.argv)
    
    # Configure application properties
    app.setApplicationName("XCOM Inventory System")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("XCOM Project")

    # Apply the global XCOM stylesheet to ensure consistent theming across all widgets
    app.setStyleSheet(XcomStyle.get_global_stylesheet())

    # Create and configure the main application window
    main_window = QMainWindow()
    main_window.setWindowTitle("XCOM UI Enhanced - Complete Inventory System")
    main_window.setFixedSize(SCALED_WIDTH, SCALED_HEIGHT)
    
    # Disable window resizing to maintain consistent layout
    main_window.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
    
    # Create the complete inventory management interface
    try:
        main_interface = create_main_interface()
        main_window.setCentralWidget(main_interface)
    except Exception as e:
        print(f"Error creating main interface: {e}")
        sys.exit(1)
    
    # Display the main window
    main_window.show()
    
    # Start the application event loop (this blocks until application is closed)
    sys.exit(app.exec())


if __name__ == "__main__":
    """
    Application entry point when run as a script.
    
    This ensures the main() function is only called when this file is run directly,
    not when imported as a module.
    """
    main()
