# GUI Module

This document is the authoritative design and architecture reference for the XCOM/AlienFall GUI systems. It is intended for validation by AI agents and developers to ensure all planned features and classes are implemented as designed. All subsystem documentation is consolidated here.

## Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Class Purposes and Details](#class-purposes-and-details)
4. [Integration Guide](#integration-guide)
5. [API Reference](#api-reference)

---

## Overview

The GUI module implements the core graphical user interface systems for the XCOM/AlienFall game, including theming, screen management, inventory widgets, and navigation panels. It provides the logic for all user interactions, visual consistency, and modular screen transitions.

## System Architecture

```
GUI Module
├── theme_manager.py (theming, scaling, style management)
├── gui_base.py (main base GUI container)
├── gui_world.py (main globe GUI container)
├── gui_core.py (base class for all screens)
├── globe/ (globe-specific screens)
├── other/
│   ├── slots/ (inventory and unit slot widgets)
│   └── widget/ (inventory, unit, and craft list widgets)
```

---

## Class Purposes and Details

### theme_manager.py
- **XcomTheme**: Centralized color palette and visual constants for the XCOM-style UI. Ensures consistent look and feel across all widgets.
- **XcomStyle**: Provides stylesheet and widget style management for all GUI components.
- **px**: Utility function for scaling pixel values for high-DPI support.
- **SCALE, GRID, etc.**: Constants for display scaling and layout.

### gui_base.py
- **TGuiBase**: Main base GUI class managing screens and navigation for the XCOM game.
  - Coordinates between specialized screen interfaces.
  - Handles top panel and screen container setup.
  - Integrates with `TGuiBaseTopPanel` and `TGuiCoreScreen`.
  - Manages screen transitions and base changes.

### gui_world.py
- **TGuiGlobe**: Main globe GUI container for the XCOM globe view.
  - Manages screen transitions and navigation for globe-specific screens.
  - Integrates with `TGuiGlobeTopPanel` and `TGuiCoreScreen`.
  - Handles top panel and screen container setup.

### gui_core.py
- **TGuiCoreScreen**: Base class for all screen widgets in the GUI.
  - Provides activation, deactivation, and data refresh hooks.
  - Ensures consistent background and style.

### globe/
- **TGuiGlobeTopPanel**: Top navigation panel for the globe interface.
  - Manages screen switching, world selection, and displays critical game info.
  - Emits signals for screen/world changes and end turn.
- **TGuiGlobeResearch**: Globe research management screen.
- **TGuiGlobeReports**: Globe reports/summary screen.
- **TGuiGlobeProduction**: Globe production management screen.

### other/slots/
- **TInventorySlot**: Interactive slot for equipment items with drag-and-drop, type restrictions, and visual customization.
- **TUnitInventorySlot**: Specialized slot for unit equipment, emits stat change signals.
- **TCraftInventorySlot**: Specialized slot for craft components, emits stat/system change signals.
- **TUnitSlot**: Slot for unit assignments to craft crew positions, emits crew change signals.

### other/widget/
- **TBaseInventoryWidget**: Widget for displaying and managing a base's complete inventory. Advanced filtering for unit and craft items.
- **TCraftListWidget**: Widget for managing and displaying a list of crafts with filtering and search.
- **TUnitItemListWidget**: Specialized inventory widget for unit equipment, with category filtering and drag-and-drop.
- **TUnitListWidget**: Widget for managing and displaying a list of units with filtering and search.

---

## Integration Guide

- All widgets and screens use centralized theming and style management from `theme_manager.py`.
- Screen containers (`TGuiBase`, `TGuiGlobe`) manage navigation and transitions between specialized screens.
- Inventory and slot widgets are reusable and can be integrated into any screen requiring item or unit management.

---

## API Reference

See individual class docstrings for detailed method signatures and usage examples. All classes follow standardized documentation and are designed for extensibility and maintainability.
