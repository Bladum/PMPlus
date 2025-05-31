"""
XCOM UI Theme and Styling System

This module provides a comprehensive theming and styling system for the XCOM Inventory Management application.
It implements a military/tactical theme with dark color schemes, sharp corners, and monospace fonts
to create an authentic XCOM-style user interface.

Key Features:
- XcomTheme: Color palette and typography definitions following XCOM design language
- XcomStyle: Static methods for generating CSS-like stylesheets for Qt widgets
- Scaling system: Pixel-perfect scaling for different display resolutions
- Grid-based layout: Consistent 16px grid alignment for professional appearance
- Specialized button styles: Different visual states for various UI elements
- Global stylesheet: Complete application-wide styling solution

Classes:
- XcomTheme: Color constants, fonts, and dimension definitions
- XcomStyle: Widget styling methods for consistent UI appearance

Constants:
- SCALE: Display scaling multiplier for high-DPI support
- GRID: Base grid unit (16px) for layout alignment
- WIDGET_MARGIN/PADDING: Standard spacing values

Dependencies:
- PySide6.QtCore: Core Qt functionality
- PySide6.QtGui: GUI components and font management

Author: XCOM Inventory System
Version: 1.0
"""

from typing import Optional
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

# Scaling constants for display resolution independence
SCALE: int = 2  # Display scaling multiplier for high-DPI support
BASE_WIDTH: int = 640  # Base interface width in pixels
BASE_HEIGHT: int = 400  # Base interface height in pixels
SCALED_WIDTH: int = BASE_WIDTH * SCALE  # Calculated scaled width
SCALED_HEIGHT: int = BASE_HEIGHT * SCALE  # Calculated scaled height

# Interface grid step and widget margin/padding for consistent layout
GRID: int = 16  # All widgets aligned to 16px grid for professional appearance
WIDGET_MARGIN: int = 1  # 1px margin for all widgets
WIDGET_PADDING: int = 1  # 1px padding for all widgets


def px(x: int) -> int:
    """
    Scale pixel values according to the current display scaling factor.
    
    This function ensures consistent sizing across different display resolutions
    by multiplying the input value by the global SCALE constant.
    
    Args:
        x (int): The base pixel value to scale
        
    Returns:
        int: The scaled pixel value
        
    Example:
        >>> px(16)  # With SCALE = 2
        32
    """
    return x * SCALE

class XcomTheme:
    """
    Color palette and visual constants for the XCOM-style user interface.
    
    This class defines the complete visual language for the application, including:
    - Dark color scheme inspired by military/tactical interfaces
    - High contrast colors for readability in dark environments
    - Accent colors for different UI states (success, danger, info, warning)
    - Typography settings optimized for technical/military appearance
    - Consistent spacing and border definitions
    
    All colors use hexadecimal notation and follow accessibility guidelines
    for sufficient contrast ratios.
    """
    
    # Background Colors - Progressive darkness levels for layered UI
    BG_DARK: str = "#0a0e14"  # Darkest background - almost black with blue tint
    BG_MID: str = "#121a24"  # Mid-level background - dark navy blue
    BG_LIGHT: str = "#1e2836"  # Lighter background elements - steel blue

    # Accent Colors - High visibility colors for different UI states
    ACCENT_GREEN: str = "#00cc66"  # Green accent (success, confirm) - neon green
    ACCENT_RED: str = "#ff3333"  # Red accent (danger, cancel) - bright red
    ACCENT_BLUE: str = "#3399ff"  # Blue accent (info, selection) - bright blue
    ACCENT_YELLOW: str = "#ffcc00"  # Yellow accent (warning, attention) - gold/amber

    # Text Colors - Hierarchy of text visibility levels
    TEXT_BRIGHT: str = "#ffffff"  # Bright text - white for primary content
    TEXT_MID: str = "#99ccff"  # Secondary text - light blue for labels
    TEXT_DIM: str = "#607080"  # Disabled text - slate gray for inactive elements

    # Border and Structure Colors
    BORDER_COLOR: str = "#30465d"  # Border color for panels - dark slate blue

    # Visual Properties - Consistent styling dimensions
    BORDER_RADIUS: int = 0  # Border radius for elements (sharp corners for military look)
    BORDER_WIDTH: int = 1  # Standard border width in pixels

    # Typography - Monospace font family for technical/military appearance
    FONT_FAMILY: str = "Consolas"  # Monospace font for tech/military look
    FONT_SIZE_SMALL: int = 9  # Small text size for details
    FONT_SIZE_NORMAL: int = 11  # Normal text size for general content
    FONT_SIZE_LARGE: int = 14  # Large text size for headers and emphasis

class XcomStyle:
    """
    Widget styling methods for consistent XCOM-themed UI appearance.
    
    This class provides static methods that generate CSS-like stylesheets for various
    Qt widgets, ensuring consistent visual appearance throughout the application.
    All methods return properly formatted stylesheet strings that can be applied
    directly to Qt widgets using setStyleSheet().
    
    Key Features:
    - Consistent color application from XcomTheme
    - Scalable dimensions using the px() helper function
    - Hover and interaction states for all interactive elements
    - Specialized styles for different button types and states
    - Complete application-wide stylesheet generation
    
    Methods generate stylesheets for:
    - GroupBox containers with customizable borders and backgrounds
    - ComboBox dropdown menus with custom arrow styling
    - ListWidget components with selection highlighting
    - PushButton variants for different UI contexts
    - Label text styling
    - Global application stylesheet
    """
    
    @staticmethod
    def groupbox(
        bg: Optional[str] = None,
        border_col: Optional[str] = None,
        border_width: int = 2,
        font_size: Optional[int] = None,
        margin_top: float = 3.5,
        label_font_size: Optional[int] = None,
        rounded: bool = True
    ) -> str:
        """
        Generate stylesheet for QGroupBox containers.
        
        Creates styled group boxes with customizable appearance including background,
        borders, and title styling. Supports both rounded and sharp corner styles.
        
        Args:
            bg (Optional[str]): Background color (defaults to XcomTheme.BG_LIGHT)
            border_col (Optional[str]): Border color (defaults to XcomTheme.BORDER_COLOR)
            border_width (int): Border thickness in pixels (default: 2)
            font_size (Optional[int]): Content font size (defaults to FONT_SIZE_LARGE + 2)
            margin_top (float): Top margin for title positioning (default: 3.5)
            label_font_size (Optional[int]): Title font size (defaults to font_size)
            rounded (bool): Whether to use rounded corners (default: True)
            
        Returns:
            str: Complete CSS stylesheet for QGroupBox styling
        """
        bg = bg or XcomTheme.BG_LIGHT
        border_col = border_col or XcomTheme.BORDER_COLOR
        font_size = font_size or (XcomTheme.FONT_SIZE_LARGE + 2)
        label_font_size = label_font_size or font_size
        border_radius = 4 if rounded else 0
        label_bg = bg  # Use the same as groupbox background for a subtle look
        return (
            f"QGroupBox {{ background: {bg}; border: {border_width}px solid {border_col}; border-radius: {border_radius}px; margin-top: {px(margin_top)}px; "
            f"color: {XcomTheme.TEXT_MID}; font-size: {font_size}px; padding-left: {px(0.5)}px; }} "
            f"QGroupBox:title {{ subcontrol-origin: margin; subcontrol-position: top center; left: 0px; top: 0px; "
            f"padding: 0 {px(3)}px; background: {label_bg}; font-size: {label_font_size}px; border-radius: {border_radius}px; }}"
        )

    @staticmethod
    def combobox() -> str:
        """
        Generate stylesheet for QComboBox dropdown menus.
        
        Creates styled dropdown menus with custom arrow indicators and hover states.
        Includes styling for the dropdown list view with proper selection highlighting.
        
        Returns:
            str: Complete CSS stylesheet for QComboBox styling including dropdown list
        """
        return (
            f"QComboBox {{ background: {XcomTheme.BG_DARK}; color: {XcomTheme.TEXT_BRIGHT}; font-size: {XcomTheme.FONT_SIZE_LARGE}px; font-family: {XcomTheme.FONT_FAMILY}; "
            f"border: 1px solid {XcomTheme.BORDER_COLOR}; border-radius: 0px; padding: {px(0.5)}px; }} "
            f"QComboBox:hover {{ border: 1px solid {XcomTheme.ACCENT_BLUE}; }} "
            f"QComboBox::drop-down {{ border: 0px; background: {XcomTheme.BG_MID}; width: {px(GRID * 0.8)}px; }} "
            f"QComboBox::down-arrow {{ width: {px(GRID * 0.5)}px; height: {px(GRID * 0.5)}px; background: {XcomTheme.TEXT_MID}; }}"
            f"QComboBox QAbstractItemView {{ background: {XcomTheme.BG_LIGHT}; color: {XcomTheme.TEXT_BRIGHT}; "
            f"border: 2px solid {XcomTheme.BORDER_COLOR}; selection-background-color: {XcomTheme.BG_MID}; outline: 0; }}"
        )

    @staticmethod
    def listwidget() -> str:
        """
        Generate stylesheet for QListWidget components.
        
        Creates styled list widgets with proper item selection, hover effects,
        and consistent typography matching the XCOM theme.
        
        Returns:
            str: Complete CSS stylesheet for QListWidget styling including item states
        """
        return (
            f"QListWidget {{ background: {XcomTheme.BG_DARK}; color: {XcomTheme.TEXT_BRIGHT}; font-size: {XcomTheme.FONT_SIZE_LARGE}px; font-family: {XcomTheme.FONT_FAMILY}; "
            f"border: 1px solid {XcomTheme.BORDER_COLOR}; border-radius: 0px; outline: 0; padding: 2px; }} "
            f"QListWidget::item {{ padding: {px(0.5)}px; border: none; }} "
            f"QListWidget::item:hover {{ background: {XcomTheme.BG_MID}; color: {XcomTheme.TEXT_BRIGHT}; }} "
            f"QListWidget::item:selected {{ background: {XcomTheme.BG_MID}; color: {XcomTheme.ACCENT_BLUE}; }}"
        )

    @staticmethod
    def pushbutton(rounded: bool = True, border_width: int = 1) -> str:
        """
        Generate stylesheet for standard QPushButton components.
        
        Creates styled buttons with hover, pressed, and checked states.
        Supports both rounded and sharp corner styles for different UI contexts.
        
        Args:
            rounded (bool): Whether to use rounded corners (default: True)
            border_width (int): Border thickness in pixels (default: 1)
            
        Returns:
            str: Complete CSS stylesheet for QPushButton with all interaction states
        """
        border_radius = 4 if rounded else 0
        return (
            f"QPushButton {{ "
            f"background: {XcomTheme.BG_LIGHT}; "
            f"color: {XcomTheme.TEXT_BRIGHT}; "
            f"border: {border_width}px solid {XcomTheme.BORDER_COLOR if border_width else 'transparent'}; "
            f"border-radius: {border_radius}px; "
            f"margin: {px(WIDGET_MARGIN)}px; "
            f"padding: {px(WIDGET_PADDING)}px; "
            f"font-family: {XcomTheme.FONT_FAMILY}; "
            f"font-size: {XcomTheme.FONT_SIZE_NORMAL}px; "
            f"}} "
            f"QPushButton:hover {{ background: {XcomTheme.ACCENT_BLUE}; color: {XcomTheme.BG_DARK}; }} "
            f"QPushButton:pressed {{ background: {XcomTheme.BG_DARK}; color: {XcomTheme.ACCENT_BLUE}; }} "
            f"QPushButton:checked {{ background: {XcomTheme.ACCENT_GREEN}; color: {XcomTheme.BG_DARK}; }}"
        )

    @staticmethod
    def pushbutton_screen_active() -> str:
        """
        Generate stylesheet for active screen navigation buttons.
        
        Creates a distinct visual style for currently selected screen buttons,
        using green accent color to indicate active state with bold typography.
        
        Returns:
            str: CSS stylesheet for active screen button styling
        """
        return (
            f"QPushButton.screen_active {{ "
            f"background: {XcomTheme.ACCENT_GREEN}; "
            f"color: {XcomTheme.BG_DARK}; "
            f"border: 2px solid {XcomTheme.ACCENT_GREEN}; "
            f"border-radius: 4px; "
            f"margin: {px(WIDGET_MARGIN)}px; "
            f"padding: {px(WIDGET_PADDING)}px; "
            f"font-family: {XcomTheme.FONT_FAMILY}; "
            f"font-size: {XcomTheme.FONT_SIZE_NORMAL}px; "
            f"font-weight: bold; "
            f"}} "
            f"QPushButton.screen_active:hover {{ background: {XcomTheme.ACCENT_BLUE}; border-color: {XcomTheme.ACCENT_BLUE}; }}"
        )

    @staticmethod
    def pushbutton_base_active() -> str:
        """
        Generate stylesheet for active base selection buttons.
        
        Creates a green-colored style for the currently selected base button,
        indicating the active base in the base selection interface.
        
        Returns:
            str: CSS stylesheet for active base button styling
        """
        return (
            f"QPushButton.base_active {{ "
            f"background: {XcomTheme.ACCENT_GREEN}; "
            f"color: {XcomTheme.BG_DARK}; "
            f"border: none; "
            f"border-radius: 0px; "
            f"margin: 0px; "
            f"padding: 0px; "
            f"font-family: {XcomTheme.FONT_FAMILY}; "
            f"font-size: {XcomTheme.FONT_SIZE_NORMAL}px; "
            f"font-weight: bold; "
            f"}}"
        )

    @staticmethod
    def pushbutton_base_available() -> str:
        """
        Generate stylesheet for available (but not active) base selection buttons.
        
        Creates a red-colored style for bases that are available for selection
        but not currently active. Includes hover effect transitioning to yellow.
        
        Returns:
            str: CSS stylesheet for available base button styling with hover state
        """
        return (
            f"QPushButton.base_available {{ "
            f"background: {XcomTheme.ACCENT_RED}; "
            f"color: {XcomTheme.TEXT_BRIGHT}; "
            f"border: none; "
            f"border-radius: 0px; "
            f"margin: 0px; "
            f"padding: 0px; "
            f"font-family: {XcomTheme.FONT_FAMILY}; "
            f"font-size: {XcomTheme.FONT_SIZE_NORMAL}px; "
            f"}} "
            f"QPushButton.base_available:hover {{ background: {XcomTheme.ACCENT_YELLOW}; color: {XcomTheme.BG_DARK}; }}"
        )

    @staticmethod
    def pushbutton_base_disabled() -> str:
        """
        Generate stylesheet for disabled base selection buttons.
        
        Creates a gray-colored style for bases that are not available for selection,
        indicating disabled or locked base slots.
        
        Returns:
            str: CSS stylesheet for disabled base button styling
        """
        return (
            f"QPushButton.base_disabled {{ "
            f"background: {XcomTheme.TEXT_DIM}; "
            f"color: {XcomTheme.BG_DARK}; "
            f"border: none; "
            f"border-radius: 0px; "
            f"margin: 0px; "
            f"padding: 0px; "
            f"font-family: {XcomTheme.FONT_FAMILY}; "
            f"font-size: {XcomTheme.FONT_SIZE_NORMAL}px; "
            f"}}"
        )

    @staticmethod
    def label() -> str:
        """
        Generate stylesheet for QLabel text components.
        
        Creates consistent text styling for labels throughout the application
        with transparent background and proper typography.
        
        Returns:
            str: CSS stylesheet for QLabel styling
        """
        return (
            f"QLabel {{ "
            f"color: {XcomTheme.TEXT_BRIGHT}; "
            f"background: transparent; "
            f"font-family: {XcomTheme.FONT_FAMILY}; "
            f"padding: 0px; "
            f"margin: 0px; "
            f"}}"
        )

    @staticmethod
    def get_global_stylesheet() -> str:
        """
        Generate a complete application-wide stylesheet.
        
        Returns a comprehensive CSS stylesheet that styles all major widget types
        used in the application. This provides consistent theming across the entire
        interface and can be applied at the application level.
        
        Includes styling for:
        - Base widget appearance
        - All button variants and states
        - GroupBox containers
        - ComboBox dropdowns
        - ListWidget components
        - Label text
        - Special panel identifiers
        
        Returns:
            str: Complete CSS stylesheet for the entire application
        """
        border_radius = 4
        return f"""
        /* Base Widget Styling */
        QWidget {{
            background: {XcomTheme.BG_MID};
            color: {XcomTheme.TEXT_BRIGHT};
            font-family: {XcomTheme.FONT_FAMILY};
        }}

        /* Button Styling */
        {XcomStyle.pushbutton(rounded=True, border_width=2)}

        /* Screen Button Styling */
        {XcomStyle.pushbutton_screen_active()}

        /* Base Button Styling */
        {XcomStyle.pushbutton_base_active()}
        {XcomStyle.pushbutton_base_available()}
        {XcomStyle.pushbutton_base_disabled()}

        /* Label Styling */
        {XcomStyle.label()}

        /* GroupBox Styling */
        QGroupBox {{
            background: {XcomTheme.BG_LIGHT};
            border: 2px solid {XcomTheme.BORDER_COLOR};
            border-radius: {border_radius}px;
            margin-top: {px(3.5)}px;
            color: {XcomTheme.TEXT_MID};
            font-size: {XcomTheme.FONT_SIZE_LARGE + 2}px;
            padding-left: {px(0.5)}px;
        }}

        QGroupBox:title {{
            subcontrol-origin: margin;
            subcontrol-position: top center;
            left: 0px;
            top: 0px;
            padding: 0 {px(3)}px;
            background: {XcomTheme.BG_LIGHT};
            font-size: {XcomTheme.FONT_SIZE_LARGE}px;
            border-radius: {border_radius}px;
        }}

        /* ComboBox Styling */
        {XcomStyle.combobox()}

        /* ListWidget Styling */
        {XcomStyle.listwidget()}

        /* Special Panel Styling */
        #topPanel {{
            background: {XcomTheme.BG_DARK};
        }}

        #bottomPanel {{
            background: {XcomTheme.BG_MID};
        }}
        """