# Base Module

This document is the authoritative design and architecture reference for the XCOM/AlienFall base management systems. It is intended for validation by AI agents and developers to ensure all planned features and classes are implemented as designed. All subsystem documentation is consolidated here.

## Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Class Purposes and Details](#class-purposes-and-details)
4. [Integration Guide](#integration-guide)
5. [API Reference](#api-reference)

---

## Overview

The base module implements the core systems for XCOM and alien base management, including facility construction, inventory, tactical battle map generation, and base serialization. It provides the logic for all base-related operations, from facility management to inventory and tactical defense.

## System Architecture

```
Base Module
├── TBaseAlien (alien base logic)
├── TBaseXCom (XCOM base logic)
├── TBaseInventory (inventory management)
├── TFacility (facility instance)
├── TFacilityType (facility blueprint)
├── TBaseXComBattleGenerator (battle map generator)
```

---

## Class Purposes and Details

### TBaseAlien
- Represents an alien base on the world map as a location.
- Handles base growth, mission generation, and scoring logic for alien bases.
- Integrates with the world map and mission systems.

### TBaseXCom
- Represents an XCOM base on the world map, with facilities, inventory, and management methods.
- Handles facility management, inventory, and base serialization for XCOM bases.
- Provides methods for adding/removing facilities and updating inventory capacities.

### TBaseInventory
- Inventory management system for XCOM bases.
- Handles items, units, and crafts with categorized storage, addition, removal, and sorting operations.
- Validates storage and craft capacity, and integrates with facility upgrades.

### TFacility
- Represents a facility instance in an XCOM base.
- Tracks position, build progress, health, and links to the facility type blueprint.
- Handles construction progress and activation logic.

### TFacilityType
- Represents a facility type blueprint for XCOM bases.
- Holds all stats, requirements, and properties for a facility, loaded from TOML or YAML.
- Used for facility construction, requirements validation, and UI display.

### TBaseXComBattleGenerator
- Generates a tactical battle map layout for an XCOM base using its facilities and their positions.
- Converts the base's facility layout into a 2D map block array for tactical battles.

---

## Integration Guide

- TBaseXCom and TBaseAlien are used for player and alien base management, respectively.
- TBaseInventory is used by TBaseXCom for managing all items, units, and crafts.
- TFacility and TFacilityType are used for facility construction and management.
- TBaseXComBattleGenerator is used to generate tactical battle maps for base defense missions.
- All classes are imported in the base module's `__init__.py` for unified access.

---

## API Reference

- See individual class docstrings and method signatures in the respective Python files for detailed API documentation.
- All classes are designed for use by both AI agents and human developers, with clear separation of data templates, managers, and active objects.

---

*This README is automatically generated and should be kept in sync with code and documentation changes.*

