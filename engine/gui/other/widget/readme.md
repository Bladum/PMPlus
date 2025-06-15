# Widget Submodule

This document provides a high-level summary and API reference for all Python files in the `engine/gui/other/widget` folder. It is intended for developers and AI agents to understand the responsibilities and integration points of each widget class.

## Table of Contents
1. [Overview](#overview)
2. [Class Purposes and Details](#class-purposes-and-details)
3. [API Reference](#api-reference)

---

## Overview

The `widget` submodule implements all inventory, list, and management widgets for the XCOM GUI. These widgets are used for displaying and managing units, crafts, and base inventories, providing advanced filtering, drag-and-drop, and search capabilities.

---

## Class Purposes and Details

### TBaseInventoryWidget
- **Purpose:**
  - Widget for displaying and managing a base's complete inventory.
  - Advanced filtering for both unit equipment and craft components.
- **Integration:**
  - Used in base inventory management screens.
  - Emits signals for item drag/drop and inventory changes.

### TCraftListWidget
- **Purpose:**
  - Widget for displaying and managing a list of crafts.
  - Provides filtering and search capabilities.
- **Integration:**
  - Used in craft management screens.
  - Emits signals for craft selection and changes.

### TUnitItemListWidget
- **Purpose:**
  - Specialized inventory widget for displaying and managing unit equipment.
  - Combines generic inventory features with unit-specific categories.
- **Integration:**
  - Used in unit inventory management screens.

### TUnitListWidget
- **Purpose:**
  - Widget for displaying and managing a list of units.
  - Provides filtering and search capabilities.
- **Integration:**
  - Used in unit management screens.
  - Emits signals for unit selection and changes.

---

## API Reference

See class docstrings in each file for detailed method signatures and usage examples. All classes follow the standardized documentation style and are designed for extensibility and maintainability.
