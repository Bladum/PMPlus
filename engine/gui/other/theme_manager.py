"""
XCOM Theme Manager

A centralized system for managing application-wide theming, styling, and visual consistency.
Builds upon the existing theme_styles foundation to provide dynamic theme management,
theme switching capabilities, and centralized styling application.

Key Features:
- Theme switching (default XCOM theme and potential custom themes)
- Global styling application for the entire application
- Consistent styling for all widget types
- Fluid scaling across different display resolutions
- Centralized access to all theme constants and styling methods

Usage:
    # Initialize the theme manager
    theme_manager = ThemeManager()

    # Apply the theme to your application
    app = QApplication(sys.argv)
    theme_manager.apply_theme(app)

    # Get stylesheets for specific widgets
    my_button.setStyleSheet(theme_manager.get_style("pushbutton"))
    my_combo.setStyleSheet(theme_manager.get_style("combobox"))

Dependencies:
- PySide6.QtCore: Core Qt functionality
- PySide6.QtGui: GUI components and font management
"""

import sys
import json
import os.path
from enum import Enum, auto
from typing import Dict, Any, Optional, List, Tuple, Union

from PySide6.QtCore import Qt, QObject, Signal
from PySide6.QtGui import QFont, QPalette, QColor
from PySide6.QtWidgets import QApplication, QWidget

# Import base theme classes
from theme_styles import XcomTheme, XcomStyle, px, SCALE, GRID, WIDGET_MARGIN, WIDGET_PADDING

class ThemeType(Enum):
    """Available theme types in the application"""
    XCOM_DARK = auto()    # Default XCOM dark military theme
    XCOM_LIGHT = auto()   # Light variant of the XCOM theme
    CUSTOM = auto()       # User-defined custom theme

class TThemeManager(QObject):
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

        # Properties (use the theme class directly for now)
        self.colors = XcomTheme()
        self._user_scale_factor = SCALE

    def set_scale_factor(self, scale_factor: float) -> None:
        """
        Set a custom scaling factor for the UI.

        Args:
            scale_factor: The scaling factor to apply to UI elements
        """
        # Store the scale factor (implementation would update SCALE and px function)
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

        # Apply appropriate style based on widget type
        if widget_type == "qpushbutton":
            widget.setStyleSheet(self.get_style("pushbutton"))
        elif widget_type == "qcombobox":
            widget.setStyleSheet(self.get_style("combobox"))
        elif widget_type == "qlistwidget":
            widget.setStyleSheet(self.get_style("listwidget"))
        elif widget_type == "qgroupbox":
            widget.setStyleSheet(self.get_style("groupbox"))
        elif widget_type == "qlabel":
            widget.setStyleSheet(self.get_style("label"))
        else:
            # Apply a generic style for other widget types
            widget.setStyleSheet(self.get_style("widget"))

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
        cache_key = f"{style_name}_{str(kwargs)}"

        # Return cached style if available
        if cache_key in self._style_cache:
            return self._style_cache[cache_key]

        # Generate style based on current theme and requested style name
        if style_name == "pushbutton":
            style = self._get_pushbutton_style(**kwargs)
        elif style_name == "pushbutton_screen_active":
            style = self._get_pushbutton_screen_active_style(**kwargs)
        elif style_name == "pushbutton_base_active":
            style = self._get_pushbutton_base_active_style(**kwargs)
        elif style_name == "pushbutton_base_available":
            style = self._get_pushbutton_base_available_style(**kwargs)
        elif style_name == "pushbutton_base_disabled":
            style = self._get_pushbutton_base_disabled_style(**kwargs)
        elif style_name == "combobox":
            style = self._get_combobox_style(**kwargs)
        elif style_name == "listwidget":
            style = self._get_listwidget_style(**kwargs)
        elif style_name == "groupbox":
            style = self._get_groupbox_style(**kwargs)
        elif style_name == "label":
            style = self._get_label_style(**kwargs)
        elif style_name == "widget":
            style = self._get_widget_style(**kwargs)
        else:
            # Default empty style if style name not recognized
            style = ""

        # Cache the generated style
        self._style_cache[cache_key] = style

        return style

    def get_global_stylesheet(self) -> str:
        """
        Get a complete application-wide stylesheet for the current theme.

        Returns:
            A complete CSS stylesheet for styling the entire application
        """
        # Use cached global stylesheet if available
        if "global_stylesheet" in self._style_cache:
            return self._style_cache["global_stylesheet"]

        # For now, use the existing XcomStyle implementation
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

    # Style generator methods - these delegate to XcomStyle methods for now
    # but could be updated to use custom theme properties in the future

    def _get_pushbutton_style(self, **kwargs) -> str:
        """Generate a pushbutton style with the given parameters."""
        return XcomStyle.pushbutton(**kwargs)

    def _get_pushbutton_screen_active_style(self, **kwargs) -> str:
        """Generate an active screen button style with the given parameters."""
        return XcomStyle.pushbutton_screen_active()

    def _get_pushbutton_base_active_style(self, **kwargs) -> str:
        """Generate an active base button style with the given parameters."""
        return XcomStyle.pushbutton_base_active()

    def _get_pushbutton_base_available_style(self, **kwargs) -> str:
        """Generate an available base button style with the given parameters."""
        if hasattr(XcomStyle, 'pushbutton_base_available'):
            return XcomStyle.pushbutton_base_available()
        return ""

    def _get_pushbutton_base_disabled_style(self, **kwargs) -> str:
        """Generate a disabled base button style with the given parameters."""
        if hasattr(XcomStyle, 'pushbutton_base_disabled'):
            return XcomStyle.pushbutton_base_disabled()
        return ""

    def _get_combobox_style(self, **kwargs) -> str:
        """Generate a combobox style with the given parameters."""
        return XcomStyle.combobox()

    def _get_listwidget_style(self, **kwargs) -> str:
        """Generate a listwidget style with the given parameters."""
        return XcomStyle.listwidget()

    def _get_groupbox_style(self, **kwargs) -> str:
        """Generate a groupbox style with the given parameters."""
        return XcomStyle.groupbox(**kwargs)

    def _get_label_style(self, **kwargs) -> str:
        """Generate a label style with the given parameters."""
        if hasattr(XcomStyle, 'label'):
            return XcomStyle.label()
        return f"color: {XcomTheme.TEXT_BRIGHT}; background: transparent; font-family: {XcomTheme.FONT_FAMILY};"

    def _get_widget_style(self, **kwargs) -> str:
        """Generate a generic widget style with the given parameters."""
        return f"background: {XcomTheme.BG_MID}; color: {XcomTheme.TEXT_BRIGHT}; font-family: {XcomTheme.FONT_FAMILY};"


# Module-level singleton instance for easy import and use
theme_manager = TThemeManager()


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
