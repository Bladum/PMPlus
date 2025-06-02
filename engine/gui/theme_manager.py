"""
XCOM Theme Manager

A centralized system for managing application-wide theming, styling, and visual consistency.
Provides dynamic theme management, theme switching capabilities, and centralized styling application.

Key Features:
- Theme switching (default XCOM dark theme and potential custom themes)
- Global styling application for the entire application
- Consistent styling for all widget types
- Fluid scaling across different display resolutions
- Centralized access to all theme constants and styling methods

Usage:
    # Get the singleton theme manager instance
    from engine.gui.theme_manager import theme_manager

    # Apply the theme to your application
    app = QApplication(sys.argv)
    theme_manager.apply_theme(app)

    # Get stylesheets for specific widgets
    my_button.setStyleSheet(theme_manager.get_style("pushbutton"))
    my_combo.setStyleSheet(theme_manager.get_style("combobox"))

    # Or use the automatic widget styling
    theme_manager.apply_widget_theme(my_button)

Dependencies:
- PySide6.QtCore: Core Qt functionality
- PySide6.QtGui: GUI components and font management
"""

import sys
import json
import os.path
from enum import Enum, auto
from functools import lru_cache
from typing import Dict, Any, Optional, List, Tuple, Union, Callable

from PySide6.QtCore import Qt, QObject, Signal
from PySide6.QtGui import QFont, QPalette, QColor
from PySide6.QtWidgets import QApplication, QWidget

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
            f"QListWidget, QListView, QTreeView, QTableView {{ background: {XcomTheme.BG_DARK}; color: {XcomTheme.TEXT_BRIGHT}; font-size: {XcomTheme.FONT_SIZE_LARGE}px; font-family: {XcomTheme.FONT_FAMILY}; "
            f"border: 1px solid {XcomTheme.BORDER_COLOR}; border-radius: 0px; outline: 0; padding: 2px; }} "
            f"QListWidget::item, QListView::item, QTreeView::item, QTableView::item {{ padding: {px(0.5)}px; border: none; }} "
            f"QListWidget::item:hover, QListView::item:hover, QTreeView::item:hover, QTableView::item:hover {{ background: {XcomTheme.BG_MID}; color: {XcomTheme.TEXT_BRIGHT}; }} "
            f"QListWidget::item:selected, QListView::item:selected, QTreeView::item:selected, QTableView::item:selected {{ background: {XcomTheme.BG_MID}; color: {XcomTheme.ACCENT_BLUE}; }}"
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
    def lineedit() -> str:
        """
        Generate stylesheet for QLineEdit input fields.

        Creates styled text input fields with focus states and consistent typography.

        Returns:
            str: CSS stylesheet for QLineEdit styling
        """
        return (
            f"QLineEdit {{ "
            f"background: {XcomTheme.BG_DARK}; "
            f"color: {XcomTheme.TEXT_BRIGHT}; "
            f"border: 1px solid {XcomTheme.BORDER_COLOR}; "
            f"border-radius: 0px; "
            f"padding: {px(0.5)}px; "
            f"selection-background-color: {XcomTheme.ACCENT_BLUE}; "
            f"selection-color: {XcomTheme.BG_DARK}; "
            f"font-family: {XcomTheme.FONT_FAMILY}; "
            f"}} "
            f"QLineEdit:focus {{ "
            f"border: 1px solid {XcomTheme.ACCENT_BLUE}; "
            f"}}"
        )

    @staticmethod
    def get_global_stylesheet() -> str:
        """
        Generate a complete application-wide stylesheet.

        Returns a comprehensive CSS stylesheet that styles all major widget types
        used in the application. This provides consistent theming across the entire
        interface and can be applied at the application level.

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
        
        /* LineEdit Styling */
        {XcomStyle.lineedit()}

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


class ThemeType(Enum):
    """Available theme types in the application"""
    XCOM_DARK = auto()    # Default XCOM dark military theme
    XCOM_LIGHT = auto()   # Light variant of the XCOM theme
    CUSTOM = auto()       # User-defined custom theme


class ThemeManager(QObject):
    """
    Centralized manager for application theming and styling.

    This class provides the foundation for consistent visual styling across the
    entire XCOM game interface. It manages theme switching, centralized styling
    application, and customizable appearance options through a standardized API.

    Interactions:
    - Used by all UI components to get consistent styling
    - Provides scale-aware styling for different display resolutions
    - Offers theme switching capability (dark vs light themes)
    - Emits signals when theme changes that UI can respond to
    - Maintains a centralized cache of styles for performance

    Key Features:
    - Complete application-wide styling through unified API
    - Theme switching between dark and light variants
    - Custom theme creation and saving
    - Dynamic scaling for different display resolutions
    - Style caching for performance optimization
    - Widget-specific styling through specialized methods
    """

    # Signal emitted when theme changes
    theme_changed = Signal(ThemeType)

    def __init__(self, initial_theme: ThemeType = ThemeType.XCOM_DARK):
        """
        Initialize the theme manager with a specified theme.

        Args:
            initial_theme: The theme to use on initialization (default: XCOM_DARK)
        """
        super().__init__()

        # Current active theme
        self._current_theme = initial_theme

        # Theme-specific color palettes
        self._theme_palettes = {
            ThemeType.XCOM_DARK: self._create_dark_palette(),
            ThemeType.XCOM_LIGHT: self._create_light_palette(),
            ThemeType.CUSTOM: self._load_custom_palette()
        }

        # Style cache to avoid regenerating styles
        self._style_cache = {}

        # Widget type registry for automatic styling
        self._widget_styles = {
            "qpushbutton": "pushbutton",
            "qcombobox": "combobox",
            "qlistwidget": "listwidget",
            "qlistview": "listwidget",
            "qtreeview": "listwidget",
            "qtableview": "listwidget",
            "qgroupbox": "groupbox",
            "qlabel": "label",
            "qlineedit": "lineedit",
            "qtextedit": "widget",
            "qplaintextedit": "widget",
            "qcheckbox": "widget",
            "qradiobutton": "widget",
            "qspinbox": "widget",
            "qdoublespinbox": "widget",
            "qprogressbar": "widget",
            "qslider": "widget",
            "qtabwidget": "widget",
            "qtabbar": "widget",
            "qstatusbar": "widget",
            "qmenu": "widget",
            "qmenubar": "widget",
            "qtoolbar": "widget",
            "qheaderview": "widget",
            "qscrollbar": "widget",
        }

        # Properties
        self.colors = XcomTheme()
        self._user_scale_factor = SCALE

    def set_scale_factor(self, scale_factor: float) -> None:
        """
        Set a custom scaling factor for the UI.

        Args:
            scale_factor: The scaling factor to apply to UI elements
        """
        # Store the scale factor
        self._user_scale_factor = scale_factor
        # Clear style cache as sizes need to be recalculated
        self._style_cache.clear()

    def get_scale_factor(self) -> float:
        """Get the current UI scaling factor."""
        return self._user_scale_factor

    def switch_theme(self, theme_type: ThemeType) -> None:
        """
        Switch to a different theme.

        Args:
            theme_type: The theme to switch to

        Emits the theme_changed signal if the theme changes.
        """
        if theme_type != self._current_theme:
            self._current_theme = theme_type
            # Clear style cache when changing themes
            self._style_cache.clear()
            # Emit signal
            self.theme_changed.emit(theme_type)

    def apply_theme(self, app: QApplication) -> None:
        """
        Apply the current theme to the entire application.

        Args:
            app: The QApplication instance
        """
        # Apply the global stylesheet
        app.setStyleSheet(self.get_global_stylesheet())

        # Set application palette
        app.setPalette(self._theme_palettes[self._current_theme])

        # Set default font
        app.setFont(self.get_default_font())

    def register_widget_style(self, widget_class_name: str, style_name: str) -> None:
        """
        Register a widget type to use a specific style.

        This allows adding support for custom widgets or changing which style
        is applied to specific widget types.

        Args:
            widget_class_name: Lowercase name of the widget class (e.g., "qpushbutton")
            style_name: Name of the style to apply (e.g., "pushbutton")
        """
        self._widget_styles[widget_class_name.lower()] = style_name

    def get_widget_style_name(self, widget_class_name: str) -> str:
        """
        Get the style name to use for a given widget class.

        Args:
            widget_class_name: Lowercase name of the widget class

        Returns:
            Name of the style to apply or "widget" as fallback
        """
        return self._widget_styles.get(widget_class_name.lower(), "widget")

    def apply_widget_theme(self, widget: QWidget) -> None:
        """
        Apply appropriate styling to a specific widget.

        This method automatically detects the widget type and applies
        the appropriate styling based on the current theme.

        Args:
            widget: The widget to style
        """
        # Get the widget's class name
        widget_type = widget.__class__.__name__.lower()

        # Get the style name for this widget type
        style_name = self.get_widget_style_name(widget_type)

        # Apply the appropriate style
        widget.setStyleSheet(self.get_style(style_name))

    def get_style(self, style_name: str, **kwargs) -> str:
        """
        Get a stylesheet for a specific widget type with optional parameters.

        Args:
            style_name: Name of the style to retrieve (e.g., "pushbutton", "combobox")
            **kwargs: Optional styling parameters specific to the widget type

        Returns:
            A stylesheet string for the specified widget type

        Example:
            style = theme_manager.get_style("pushbutton", rounded=False, border_width=2)
        """
        # Generate a cache key based on the style name and parameters
        cache_key = f"{style_name}_{hash(frozenset(kwargs.items()))}"

        # Return cached style if available
        if cache_key in self._style_cache:
            return self._style_cache[cache_key]

        # Generate style based on current theme and requested style name
        style_generator = self._get_style_generator(style_name)
        if style_generator:
            style = style_generator(**kwargs)
        else:
            # Default empty style if style name not recognized
            style = ""

        # Cache the generated style
        self._style_cache[cache_key] = style

        return style

    def _get_style_generator(self, style_name: str) -> Optional[Callable]:
        """
        Get the appropriate style generator function for the given style name.

        Args:
            style_name: Name of the style to retrieve

        Returns:
            A style generator function or None if not found
        """
        style_generators = {
            "pushbutton": self._get_pushbutton_style,
            "pushbutton_screen_active": self._get_pushbutton_screen_active_style,
            "pushbutton_base_active": self._get_pushbutton_base_active_style,
            "pushbutton_base_available": self._get_pushbutton_base_available_style,
            "pushbutton_base_disabled": self._get_pushbutton_base_disabled_style,
            "combobox": self._get_combobox_style,
            "listwidget": self._get_listwidget_style,
            "groupbox": self._get_groupbox_style,
            "label": self._get_label_style,
            "lineedit": self._get_lineedit_style,
            "widget": self._get_widget_style,
        }

        return style_generators.get(style_name)

    def get_global_stylesheet(self) -> str:
        """
        Get a complete application-wide stylesheet for the current theme.

        This method builds and caches a complete application-wide stylesheet
        for styling all components consistently based on the current theme.

        Returns:
            A complete CSS stylesheet for styling the entire application
        """
        # Use cached global stylesheet if available
        if "global_stylesheet" in self._style_cache:
            return self._style_cache["global_stylesheet"]

        # Get the stylesheet from XcomStyle
        stylesheet = XcomStyle.get_global_stylesheet()

        # Cache the stylesheet
        self._style_cache["global_stylesheet"] = stylesheet

        return stylesheet

    def get_default_font(self) -> QFont:
        """
        Get the default font for the current theme.

        Returns:
            A QFont object configured for the current theme
        """
        font = QFont(XcomTheme.FONT_FAMILY, XcomTheme.FONT_SIZE_NORMAL)
        return font

    def get_color(self, color_name: str) -> str:
        """
        Get a color value by name from the current theme.

        Args:
            color_name: Name of the color to retrieve (e.g., "bg_dark", "accent_blue")

        Returns:
            The color value as a hex string
        """
        # Convert color_name to uppercase for attribute lookup
        color_attr = color_name.upper()

        # Try to get the color from theme constants
        if hasattr(XcomTheme, color_attr):
            return getattr(XcomTheme, color_attr)

        # Return default color if not found
        return "#000000"

    def get_dimension(self, dimension_name: str) -> int:
        """
        Get a dimension value by name from the current theme.

        Args:
            dimension_name: Name of the dimension to retrieve (e.g., "grid", "border_width")

        Returns:
            The dimension value in pixels
        """
        # Special case for grid
        if dimension_name.lower() == "grid":
            return GRID

        # Convert dimension_name to uppercase for attribute lookup
        dimension_attr = dimension_name.upper()

        # Try to get the dimension from theme constants
        if hasattr(XcomTheme, dimension_attr):
            return getattr(XcomTheme, dimension_attr)

        # Return default value if not found
        return 1

    def save_custom_theme(self, theme_data: Dict[str, Any]) -> bool:
        """
        Save a custom theme configuration to file.

        Args:
            theme_data: Dictionary containing custom theme settings

        Returns:
            True if the theme was successfully saved
        """
        try:
            # Determine the file path for the custom theme
            theme_path = self._get_custom_theme_path()

            # Write the theme data as JSON
            with open(theme_path, 'w') as f:
                json.dump(theme_data, f, indent=2)

            # Reload the custom theme
            self._theme_palettes[ThemeType.CUSTOM] = self._load_custom_palette()

            # Clear style cache
            self._style_cache.clear()

            return True
        except Exception as e:
            print(f"Error saving custom theme: {e}")
            return False

    def _create_dark_palette(self) -> QPalette:
        """Create a dark palette based on the XCOM dark theme colors."""
        palette = QPalette()

        # Set window background colors
        palette.setColor(QPalette.Window, QColor(XcomTheme.BG_MID))
        palette.setColor(QPalette.WindowText, QColor(XcomTheme.TEXT_BRIGHT))

        # Set widget background colors
        palette.setColor(QPalette.Base, QColor(XcomTheme.BG_DARK))
        palette.setColor(QPalette.AlternateBase, QColor(XcomTheme.BG_LIGHT))

        # Set text colors
        palette.setColor(QPalette.Text, QColor(XcomTheme.TEXT_BRIGHT))
        palette.setColor(QPalette.BrightText, QColor(XcomTheme.TEXT_BRIGHT))
        palette.setColor(QPalette.ButtonText, QColor(XcomTheme.TEXT_BRIGHT))

        # Set button colors
        palette.setColor(QPalette.Button, QColor(XcomTheme.BG_LIGHT))

        # Set highlight colors
        palette.setColor(QPalette.Highlight, QColor(XcomTheme.ACCENT_BLUE))
        palette.setColor(QPalette.HighlightedText, QColor(XcomTheme.BG_DARK))

        # Set disabled state colors
        palette.setColor(QPalette.Disabled, QPalette.Text, QColor(XcomTheme.TEXT_DIM))
        palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(XcomTheme.TEXT_DIM))
        palette.setColor(QPalette.Disabled, QPalette.Highlight, QColor(XcomTheme.BG_LIGHT))
        palette.setColor(QPalette.Disabled, QPalette.Base, QColor(XcomTheme.BG_MID))
        palette.setColor(QPalette.Disabled, QPalette.Button, QColor(XcomTheme.BG_MID))
        palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(XcomTheme.TEXT_DIM))

        return palette

    def _create_light_palette(self) -> QPalette:
        """Create a light palette based on inverted XCOM theme colors."""
        palette = QPalette()

        # Invert main colors for light theme
        bg_light = "#e6e9ef"  # Light gray with blue tint
        bg_mid = "#c0c5d0"    # Medium gray with blue tint
        bg_dark = "#a0a8b8"   # Darker gray with blue tint

        text_dark = "#202428"    # Very dark gray
        text_mid = "#505868"     # Medium dark gray
        text_light = "#8090a8"   # Light gray for disabled text

        # Modified accent colors for better visibility on light background
        accent_blue = "#0066cc"   # Darker blue
        accent_green = "#008855"  # Darker green
        accent_red = "#cc1111"    # Darker red
        accent_yellow = "#cc9900" # Darker amber

        # Set window background colors
        palette.setColor(QPalette.Window, QColor(bg_mid))
        palette.setColor(QPalette.WindowText, QColor(text_dark))

        # Set widget background colors
        palette.setColor(QPalette.Base, QColor(bg_light))
        palette.setColor(QPalette.AlternateBase, QColor(bg_dark))

        # Set text colors
        palette.setColor(QPalette.Text, QColor(text_dark))
        palette.setColor(QPalette.BrightText, QColor(text_dark))
        palette.setColor(QPalette.ButtonText, QColor(text_dark))

        # Set button colors
        palette.setColor(QPalette.Button, QColor(bg_dark))

        # Set highlight colors
        palette.setColor(QPalette.Highlight, QColor(accent_blue))
        palette.setColor(QPalette.HighlightedText, QColor(bg_light))

        # Set disabled state colors
        palette.setColor(QPalette.Disabled, QPalette.Text, QColor(text_light))
        palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(text_light))
        palette.setColor(QPalette.Disabled, QPalette.Highlight, QColor(bg_dark))
        palette.setColor(QPalette.Disabled, QPalette.Base, QColor(bg_mid))
        palette.setColor(QPalette.Disabled, QPalette.Button, QColor(bg_mid))
        palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(text_light))

        return palette

    def _load_custom_palette(self) -> QPalette:
        """Load a custom palette from saved theme file or use fallback."""
        try:
            theme_path = self._get_custom_theme_path()

            # Check if custom theme file exists
            if not os.path.exists(theme_path):
                # Return dark palette as fallback
                return self._create_dark_palette()

            # Load theme data from file
            with open(theme_path, 'r') as f:
                theme_data = json.load(f)

            # Create a new palette
            palette = QPalette()

            # Set colors from theme data
            palette.setColor(QPalette.Window, QColor(theme_data.get('window_bg', XcomTheme.BG_MID)))
            palette.setColor(QPalette.WindowText, QColor(theme_data.get('window_text', XcomTheme.TEXT_BRIGHT)))
            palette.setColor(QPalette.Base, QColor(theme_data.get('base_bg', XcomTheme.BG_DARK)))
            palette.setColor(QPalette.AlternateBase, QColor(theme_data.get('alt_base_bg', XcomTheme.BG_LIGHT)))
            palette.setColor(QPalette.Text, QColor(theme_data.get('text', XcomTheme.TEXT_BRIGHT)))
            palette.setColor(QPalette.BrightText, QColor(theme_data.get('bright_text', XcomTheme.TEXT_BRIGHT)))
            palette.setColor(QPalette.ButtonText, QColor(theme_data.get('button_text', XcomTheme.TEXT_BRIGHT)))
            palette.setColor(QPalette.Button, QColor(theme_data.get('button_bg', XcomTheme.BG_LIGHT)))
            palette.setColor(QPalette.Highlight, QColor(theme_data.get('highlight', XcomTheme.ACCENT_BLUE)))
            palette.setColor(QPalette.HighlightedText, QColor(theme_data.get('highlight_text', XcomTheme.BG_DARK)))

            # Set disabled state colors
            palette.setColor(QPalette.Disabled, QPalette.Text, QColor(theme_data.get('disabled_text', XcomTheme.TEXT_DIM)))
            palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(theme_data.get('disabled_button_text', XcomTheme.TEXT_DIM)))
            palette.setColor(QPalette.Disabled, QPalette.Highlight, QColor(theme_data.get('disabled_highlight', XcomTheme.BG_LIGHT)))
            palette.setColor(QPalette.Disabled, QPalette.Base, QColor(theme_data.get('disabled_base_bg', XcomTheme.BG_MID)))
            palette.setColor(QPalette.Disabled, QPalette.Button, QColor(theme_data.get('disabled_button_bg', XcomTheme.BG_MID)))
            palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(theme_data.get('disabled_window_text', XcomTheme.TEXT_DIM)))

            return palette

        except Exception as e:
            print(f"Error loading custom theme: {e}")
            # Return dark palette as fallback
            return self._create_dark_palette()

    def _get_custom_theme_path(self) -> str:
        """Get the file path for the custom theme file."""
        # Get application directory
        app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Create themes directory if it doesn't exist
        themes_dir = os.path.join(app_dir, 'themes')
        os.makedirs(themes_dir, exist_ok=True)
        # Return path to custom theme file
        return os.path.join(themes_dir, 'custom_theme.json')

    # Style generator methods with caching for better performance

    @lru_cache(maxsize=32)
    def _get_pushbutton_style(self, rounded=True, border_width=1) -> str:
        """
        Generate a pushbutton style with the given parameters.

        Args:
            rounded: Whether to use rounded corners
            border_width: Border thickness in pixels

        Returns:
            Stylesheet string for pushbuttons
        """
        return XcomStyle.pushbutton(rounded=rounded, border_width=border_width)

    @lru_cache(maxsize=8)
    def _get_pushbutton_screen_active_style(self, **kwargs) -> str:
        """Generate an active screen button style with the given parameters."""
        return XcomStyle.pushbutton_screen_active()

    @lru_cache(maxsize=8)
    def _get_pushbutton_base_active_style(self, **kwargs) -> str:
        """Generate an active base button style with the given parameters."""
        return XcomStyle.pushbutton_base_active()

    @lru_cache(maxsize=8)
    def _get_pushbutton_base_available_style(self, **kwargs) -> str:
        """Generate an available base button style with the given parameters."""
        return XcomStyle.pushbutton_base_available()

    @lru_cache(maxsize=8)
    def _get_pushbutton_base_disabled_style(self, **kwargs) -> str:
        """Generate a disabled base button style with the given parameters."""
        return XcomStyle.pushbutton_base_disabled()

    @lru_cache(maxsize=8)
    def _get_combobox_style(self, **kwargs) -> str:
        """Generate a combobox style with the given parameters."""
        return XcomStyle.combobox()

    @lru_cache(maxsize=8)
    def _get_listwidget_style(self, **kwargs) -> str:
        """Generate a listwidget style with the given parameters."""
        return XcomStyle.listwidget()

    @lru_cache(maxsize=16)
    def _get_groupbox_style(self, bg=None, border_col=None, border_width=2,
                           font_size=None, margin_top=3.5, label_font_size=None,
                           rounded=True) -> str:
        """
        Generate a groupbox style with the given parameters.

        Args:
            bg: Background color
            border_col: Border color
            border_width: Border thickness in pixels
            font_size: Content font size
            margin_top: Top margin for title positioning
            label_font_size: Title font size
            rounded: Whether to use rounded corners

        Returns:
            Stylesheet string for groupboxes
        """
        return XcomStyle.groupbox(bg=bg, border_col=border_col, border_width=border_width,
                                 font_size=font_size, margin_top=margin_top,
                                 label_font_size=label_font_size, rounded=rounded)

    @lru_cache(maxsize=8)
    def _get_label_style(self, **kwargs) -> str:
        """Generate a label style with the given parameters."""
        return XcomStyle.label()

    @lru_cache(maxsize=8)
    def _get_lineedit_style(self, **kwargs) -> str:
        """Generate a lineedit style with the given parameters."""
        return XcomStyle.lineedit()

    @lru_cache(maxsize=8)
    def _get_widget_style(self, **kwargs) -> str:
        """Generate a generic widget style with the given parameters."""
        return f"background: {XcomTheme.BG_MID}; color: {XcomTheme.TEXT_BRIGHT}; font-family: {XcomTheme.FONT_FAMILY};"


# Module-level singleton instance for easy import and use
theme_manager = ThemeManager()


def apply_theme_to_application(app: QApplication) -> None:
    """
    Convenience function to apply theme to application.

    Args:
        app: The QApplication instance to apply the theme to
    """
    theme_manager.apply_theme(app)


def get_style(style_name: str, **kwargs) -> str:
    """
    Convenience function to get a style by name.

    Args:
        style_name: Name of the style to retrieve
        **kwargs: Optional styling parameters

    Returns:
        A stylesheet string for the specified style
    """
    return theme_manager.get_style(style_name, **kwargs)
