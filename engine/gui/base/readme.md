# Base Submodule

This document provides a high-level summary and API reference for all Python files in the `engine/gui/base` folder. It is intended for developers and AI agents to understand the responsibilities and integration points of each base GUI class.

## Table of Contents
1. [Overview](#overview)
2. [Class Purposes and Details](#class-purposes-and-details)
3. [API Reference](#api-reference)

---

## Overview

The `base` submodule implements all GUI components for the XCOM base management system, including navigation panels, barracks, storage, workshop, transfers, purchasing, and more. These classes provide the visual and interactive layer for base operations and management.

---

## Class Purposes and Details

### TGuiBaseTopPanel
- **Purpose:**
  - Implements the top navigation bar for the base interface.
  - Provides screen switching, base selection, and displays critical game information.
- **Integration:**
  - Used by the main base container to manage navigation and state.

### TGuiWorkshop
- **Purpose:**
  - Main workshop GUI screen for manufacturing management.
- **Integration:**
  - Used to manage and display manufacturing projects and progress.

### TGuiTransfer
- **Purpose:**
  - Main transfer GUI screen for inter-base transfers.
- **Integration:**
  - Used to manage and display transfer operations between bases.

### TGuiStorage
- **Purpose:**
  - Main storage GUI screen for base storage management.
- **Integration:**
  - Used to manage and display base storage inventory.

### TPurchaseGui
- **Purpose:**
  - Main GUI screen for purchasing items, units, and crafts.
- **Integration:**
  - Used to manage and display purchase operations and orders.

### TGuiBarracks
- **Purpose:**
  - Main barracks GUI screen for unit and inventory management.
  - Handles unit management, equipment assignment, loadout templates, and item inventory interfaces.
- **Integration:**
  - Used to manage base personnel and equipment.

---

## API Reference

See class docstrings in each file for detailed method signatures and usage examples. All classes follow the standardized documentation style and are designed for extensibility and maintainability.
