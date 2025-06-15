# Battle Submodule

This document provides a high-level summary and API reference for all Python files in the `engine/gui/battle` folder. It is intended for developers and AI agents to understand the responsibilities and integration points of each battle GUI class.

## Table of Contents
1. [Overview](#overview)
2. [Class Purposes and Details](#class-purposes-and-details)
3. [API Reference](#api-reference)

---

## Overview

The `battle` submodule implements all GUI components for the XCOM battle system, including map visualization, unit graphics, mission screens, inventory, and user interaction controllers. These classes provide the visual and interactive layer for tactical combat.

---

## Class Purposes and Details

### UnitGraphicsItem
- **Purpose:**
  - Visual representation of a unit on the battle map.
  - Subclass of QGraphicsRectItem for unit display.
- **Integration:**
  - Used by `BattleMapView` to render units.

### BattleMapView
- **Purpose:**
  - Main view for rendering the battle map and units using QGraphicsView/QGraphicsScene.
  - Handles efficient drawing and updating of tiles and units.
- **Integration:**
  - Used as the main map display in battle screens.

### BattleInteractionController
- **Purpose:**
  - Handles user interaction (mouse, wheel, selection, path planning) for the battle map.
  - Connects to `BattleMapView` and `TBattle` logic.
- **Integration:**
  - Used to manage user input and selection in tactical combat.

### TGuiBattleBrief
- **Purpose:**
  - Main GUI screen for mission briefing.
- **Integration:**
  - Used at the start of a mission to display objectives and context.

### TGuiBattleEnd
- **Purpose:**
  - Main GUI screen for mission end/debriefing.
- **Integration:**
  - Used at the end of a mission to display results and statistics.

### TGuiBattleInventory
- **Purpose:**
  - Main GUI screen for battle inventory management.
- **Integration:**
  - Used for managing unit and craft equipment during battle.

---

## API Reference

See class docstrings in each file for detailed method signatures and usage examples. All classes follow the standardized documentation style and are designed for extensibility and maintainability.
