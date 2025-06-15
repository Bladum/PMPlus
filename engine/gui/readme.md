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

The GUI module implements the core graphical user interface systems for the XCOM/AlienFall game, including the main base GUI, globe GUI, theming, and screen/widget management. It provides the logic for all user interactions, screen transitions, and visual consistency.

## System Architecture

```
GUI Module
├── TGuiBase (main base GUI container)
├── TGuiCoreScreen (base class for all screens)
├── TGuiGlobe (main globe GUI container)
├── XcomTheme (theme constants and color definitions)
```

---

## Class Purposes and Details

### TGuiBase
- Main base GUI class that manages screens and navigation for the XCOM game.
- Acts as a coordinator between different specialized screen interfaces.
- Inherits from QWidget and manages top panel and screen container.

### TGuiCoreScreen
- Base class for all screen widgets that can be displayed in the BaseGUI.
- Provides hooks for activation, deactivation, data refresh, and summary updates.
- Inherits from QWidget and integrates with theming.

### TGuiGlobe
- Main globe GUI container that manages screens and navigation for the XCOM globe view.
- Inherits from QWidget and manages top panel and screen container for the globe.
- Supports screen management and transitions for globe-related interfaces.

### XcomTheme
- Centralized system for managing application-wide theming, styling, and visual consistency.
- Provides color palette, scaling utilities, and style constants for the XCOM-style user interface.
- Used by all GUI components for consistent appearance.

---

## Integration Guide

- TGuiBase and TGuiGlobe are used as the main containers for base and globe interfaces, respectively.
- TGuiCoreScreen is used as the base class for all custom screens and widgets.
- XcomTheme is used throughout the GUI for consistent theming and scaling.
- All classes are designed for extensibility and integration with PySide6/Qt widgets.

---

## API Reference

- See individual class docstrings and method signatures in the respective Python files for detailed API documentation.
- All classes are designed for use by both AI agents and human developers, with clear separation of containers, screens, and theming.

---

*This README is automatically generated and should be kept in sync with code and documentation changes.*
