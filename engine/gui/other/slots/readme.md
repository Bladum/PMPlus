# Slots Submodule

This document provides a high-level summary and API reference for all Python files in the `engine/gui/other/slots` folder. It is intended for developers and AI agents to understand the responsibilities and integration points of each slot widget class.

## Table of Contents
1. [Overview](#overview)
2. [Class Purposes and Details](#class-purposes-and-details)
3. [API Reference](#api-reference)

---

## Overview

The `slots` submodule implements all slot widgets for the XCOM GUI inventory and crew assignment systems. These slots are used for unit equipment, craft components, and crew positions, providing drag-and-drop, type restrictions, and visual feedback.

---

## Class Purposes and Details

### TInventorySlot
- **Purpose:**
  - Interactive slot for equipment items with drag-and-drop, type restrictions, and visual customization.
  - Used as the base class for all specialized slot widgets.
- **Integration:**
  - Used by unit and craft inventory UIs.
  - Emits signals for item changes, drops, and right-clicks.

### TUnitInventorySlot
- **Purpose:**
  - Specialized slot for unit equipment with unit-specific functionality.
  - Emits signals when unit stats change due to equipment.
- **Integration:**
  - Used in unit inventory management screens.

### TCraftInventorySlot
- **Purpose:**
  - Specialized slot for craft components with craft-specific functionality.
  - Emits signals when craft stats or systems change.
- **Integration:**
  - Used in craft inventory management screens.

### TUnitSlot
- **Purpose:**
  - Slot for unit assignments to craft crew positions.
  - Always contains a single TUnit or None.
  - Emits signals when crew assignments change.
- **Integration:**
  - Used in craft crew assignment UIs.

---

## API Reference

See class docstrings in each file for detailed method signatures and usage examples. All classes follow the standardized documentation style and are designed for extensibility and maintainability.
