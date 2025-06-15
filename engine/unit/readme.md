# Unit Module

This document is the authoritative design and architecture reference for the XCOM/AlienFall unit systems. It is intended for validation by AI agents and developers to ensure all planned features and classes are implemented as designed. All subsystem documentation is consolidated here.

## Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Class Purposes and Details](#class-purposes-and-details)
4. [Integration Guide](#integration-guide)
5. [API Reference](#api-reference)

---

## Overview

The unit module implements the core systems for XCOM/AlienFall units, including unit templates, stats, traits, inventory, and side/faction logic. It provides the logic for all unit-related operations, from stat management to equipment and combat integration.

## System Architecture

```
Unit Module
├── TRace (race template for unit creation)
├── TSide (faction/side definition)
├── TTrait (base class for unit traits)
├── TUnit (individual unit entity)
├── TUnitInventoryManager (unit inventory management)
├── TUnitStats (unit stats and management)
├── InventoryTemplate (saved equipment configurations)
```

---

## Class Purposes and Details

### TRace
- Represents a race/type of unit and its basic stats, abilities, and AI behavior.
- Used as a template for unit creation and stat calculation.
- Defines immunities, abilities, and combat roles for each race.

### TSide
- Represents a faction or side in the game (e.g., player, alien, civilian).
- Used to define unit ownership, allegiance, and combat relationships.
- Provides constants for all major sides in the game.

### TTrait
- Represents a trait of a unit, modifying stats and abilities.
- Base class for all specific trait types (promotions, wounds, effects, etc.).
- Supports stat modifications, requirements, and battle effects.

### TUnit
- Represents an individual unit in the game with all its attributes and capabilities.
- Handles stats, equipment, traits, and status for gameplay.
- Integrates with race, side, trait, and inventory systems.

### TUnitInventoryManager
- Unified inventory manager for a single unit.
- Handles slot logic, stat modification, template save/load, dynamic slot availability, and auto-equip.
- Supports equipment templates for quick loadouts.

### TUnitStats
- Handles health, energy, morale, action points, and other core stats for units.
- Provides methods to manage and update stats during the game.
- Used by all unit, race, and trait classes for stat management.

### InventoryTemplate
- Container for saved equipment configurations for units.
- Allows players to save and quickly restore equipment setups for different scenarios or unit types.

---

## Integration Guide

- TRace, TSide, and TTrait are used for unit creation, faction logic, and trait assignment.
- TUnit is the main entity for all units in the game, integrating with stats, inventory, and traits.
- TUnitInventoryManager and InventoryTemplate are used for managing and saving unit equipment.
- TUnitStats is used throughout the module for stat management and updates.
- All classes are designed for extensibility and integration with other game systems.

---

## API Reference

- See individual class docstrings and method signatures in the respective Python files for detailed API documentation.
- All classes are designed for use by both AI agents and human developers, with clear separation of templates, entities, and managers.

---

*This README is automatically generated and should be kept in sync with code and documentation changes.*
