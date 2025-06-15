# Craft Module

This document is the authoritative design and architecture reference for the XCOM/AlienFall craft systems. It is intended for validation by AI agents and developers to ensure all planned features and classes are implemented as designed. All subsystem documentation is consolidated here.

## Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Class Purposes and Details](#class-purposes-and-details)
4. [Integration Guide](#integration-guide)
5. [API Reference](#api-reference)

---

## Overview

The craft module implements the core systems for XCOM craft management, including craft entities, inventory, type blueprints, and interception combat. It provides the logic for all craft-related operations, from world map movement to dogfighting and inventory management.

## System Architecture

```
Craft Module
├── TCraft (craft entity)
├── TCraftInventoryManager (craft inventory management)
├── CraftInventoryTemplate (saved loadout templates)
├── TCraftType (craft type blueprint)
├── TInterception (interception combat system)
```

---

## Class Purposes and Details

### TCraft
- Represents a craft (aircraft, submarine, spaceship, etc.) on the world map.
- Handles movement, crew, inventory, mission assignment, and automation routines.
- Integrates with craft type blueprints and world map systems.

### TCraftInventoryManager
- Unified inventory manager for a single craft.
- Supports hardpoint management, dynamic availability, performance modification, equipment templates, cargo calculation, validation, and synchronization.
- Integrates with item and craft systems for inventory operations.

### CraftInventoryTemplate
- Container for saved craft loadout configurations.
- Allows players to save and quickly restore component/cargo setups for different scenarios or craft types.

### TCraftType
- Represents the blueprint for all craft types in the game.
- Encapsulates all static data and configuration for a craft, including stats, capabilities, costs, and special features.
- Used for construction, upgrades, and UI display.

### TInterception
- Implements the interception combat mechanics for XCOM crafts and UFOs.
- Manages dogfighting, action points, hit/damage/evasion calculations, and turn-based combat flow.
- Integrates with craft and UFO entities for real-time combat resolution.

---

## Integration Guide

- TCraft is used for all craft entities on the world map, integrating with inventory, mission, and automation systems.
- TCraftInventoryManager and CraftInventoryTemplate are used for managing and saving craft loadouts.
- TCraftType is used for defining craft blueprints and capabilities.
- TInterception is used for resolving air/space/sea combat between XCOM crafts and UFOs.
- All classes are imported in the craft module's `__init__.py` for unified access.

---

## API Reference

- See individual class docstrings and method signatures in the respective Python files for detailed API documentation.
- All classes are designed for use by both AI agents and human developers, with clear separation of entities, managers, and templates.

---

*This README is automatically generated and should be kept in sync with code and documentation changes.*
