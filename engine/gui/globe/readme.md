# Globe Submodule

This document provides a high-level summary and API reference for all Python files in the `engine/gui/globe` folder. It is intended for developers and AI agents to understand the responsibilities and integration points of each globe GUI class.

## Table of Contents
1. [Overview](#overview)
2. [Class Purposes and Details](#class-purposes-and-details)
3. [API Reference](#api-reference)

---

## Overview

The `globe` submodule implements all GUI components for the XCOM globe view, including navigation panels, research, production, reports, policies, and more. These classes provide the visual and interactive layer for the strategic world view.

---

## Class Purposes and Details

### TGuiGlobeTopPanel
- **Purpose:**
  - Implements the top navigation bar for the globe interface.
  - Provides screen switching, world selection, and displays critical game information.
- **Integration:**
  - Used by the main globe container to manage navigation and state.

### TGuiGlobeResearch
- **Purpose:**
  - Main GUI screen for research management.
- **Integration:**
  - Used to manage and display research projects and progress.

### TGuiGlobeReports
- **Purpose:**
  - Main GUI screen for reports/summary.
- **Integration:**
  - Used to display strategic reports and summaries.

### TGuiGlobeProduction
- **Purpose:**
  - Main GUI screen for production management.
- **Integration:**
  - Used to manage and display production projects and progress.

### TGuiGlobePolicies
- **Purpose:**
  - Main GUI screen for policies management.
- **Integration:**
  - Used to manage and display policy settings.

### TGuiGlobePedia
- **Purpose:**
  - Main GUI screen for globe encyclopedia (pedia).
- **Integration:**
  - Used to display in-game encyclopedia entries.

### TGuiGlobeMenu
- **Purpose:**
  - Main GUI screen for globe options/menu.
- **Integration:**
  - Used to display and manage game options.

### TGuiGlobeMap
- **Purpose:**
  - Main GUI screen for globe map display.
- **Integration:**
  - Used to display the strategic map and locations.

### TGuiGlobeIntercept
- **Purpose:**
  - Main GUI screen for interception management.
- **Integration:**
  - Used to manage and display interception missions.

### TGuiGlobeFunding
- **Purpose:**
  - Main GUI screen for funding overview.
- **Integration:**
  - Used to display and manage funding sources.

### TGuiGlobeFactions
- **Purpose:**
  - Main GUI screen for factions overview.
- **Integration:**
  - Used to display and manage faction relations.

### TGuiGlobeDodgefight
- **Purpose:**
  - Main GUI screen for dodgefight/air combat.
- **Integration:**
  - Used to manage and display air combat missions.

### TGuiGlobeBudget
- **Purpose:**
  - Main GUI screen for budget management.
- **Integration:**
  - Used to display and manage base/world budgets.

---

## API Reference

See class docstrings in each file for detailed method signatures and usage examples. All classes follow the standardized documentation style and are designed for extensibility and maintainability.
