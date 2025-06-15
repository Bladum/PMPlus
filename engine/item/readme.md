# Item Module

This document is the authoritative design and architecture reference for the XCOM/AlienFall item systems. It is intended for validation by AI agents and developers to ensure all planned features and classes are implemented as designed. All subsystem documentation is consolidated here.

## Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Class Purposes and Details](#class-purposes-and-details)
4. [Integration Guide](#integration-guide)
5. [API Reference](#api-reference)

---

## Overview

The item module implements the core item systems for the XCOM/AlienFall game, including base items, armours, craft equipment, weapon modes, and inventory transfer management. It provides the logic for all item-related operations, from inventory management to equipment and combat integration.

## System Architecture

```
Item Module
├── TItem (base class for all items)
├── TItemArmour (armour item for units)
├── TCraftItem (craft-specific equipment)
├── TWeaponMode (weapon firing/usage modes)
├── TItemTransferManager (inventory item transfer management)
```

---

## Class Purposes and Details

### TItem
- Base class for all game items.
- Provides common properties and behaviors for all items, including serialization, inventory compatibility, and UI display.
- Used as the foundation for all item types in the game.

### TItemArmour
- Represents an armour item assigned to a unit (soldier, alien, etc).
- Manages shield points, regeneration, and resistance to damage types.
- Provides stat modifiers and interacts with unit systems for damage reduction.

### TCraftItem
- Represents a craft-specific item for vehicles/craft.
- Manages craft equipment state, maintenance, and provides methods for craft system integration.
- Handles ammo, rearming, and hardpoint assignment for craft equipment.

### TWeaponMode
- Represents a specific firing/usage mode for weapons (snap, aimed, auto, etc.).
- Defines operational modes with modifiers for accuracy, damage, AP cost, and shot count.
- Used by weapons to provide multiple attack options.

### TItemTransferManager
- Manages the transfer of items between inventory slots.
- Handles drag-and-drop, compatibility checks, swap logic, and undo/redo history for inventory systems.
- Integrates with GUI and inventory systems for user interaction.

---

## Integration Guide

- TItem and its subclasses are used throughout the game for inventory, equipment, and combat.
- TItemArmour and TCraftItem are used for unit and craft equipment, respectively.
- TWeaponMode is used by weapons to define multiple attack options.
- TItemTransferManager is used by the GUI and inventory systems for item movement and management.
- All classes are designed for extensibility and integration with other game systems.

---

## API Reference

- See individual class docstrings and method signatures in the respective Python files for detailed API documentation.
- All classes are designed for use by both AI agents and human developers, with clear separation of base items, equipment, and transfer logic.

---

*This README is automatically generated and should be kept in sync with code and documentation changes.*
