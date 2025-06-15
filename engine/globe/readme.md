# Globe Module

This document is the authoritative design and architecture reference for the XCOM/AlienFall globe/world map systems. It is intended for validation by AI agents and developers to ensure all planned features and classes are implemented as designed. All subsystem documentation is consolidated here.

## Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Class Purposes and Details](#class-purposes-and-details)
4. [Integration Guide](#integration-guide)
5. [API Reference](#api-reference)

---

## Overview

The globe module implements the core world map systems for the XCOM/AlienFall game, including biomes, countries, diplomacy, funding, locations, radar, and world map analytics. It provides the logic for all world-level interactions, analytics, and strategic gameplay.

## System Architecture

```
Globe Module
├── TBiome (biome type for world map tiles)
├── TCountry (country entity and funding)
├── TDiplomacy (diplomacy manager)
├── TFunding (funding and monthly report manager)
├── TLocation (world map location entity)
├── TGlobalRadar (global radar detection manager)
```

---

## Class Purposes and Details

### TBiome
- Represents a biome type assigned to each tile on the world map (e.g., forest, desert, ocean).
- Used to generate battles with specific terrain types and for world map analytics.
- Supports random terrain selection based on biome weights.

### TCountry
- Represents a country on the world map.
- Manages funding, relations with XCOM, and country-specific properties for world map analytics and gameplay.
- Tracks owned tiles, funding, services, and diplomatic status.

### TDiplomacy
- Manages diplomacy between XCOM (player) and other factions.
- Provides methods to get, set, and list diplomatic states (ALLY, NEUTRAL, WAR).
- Tracks history of state changes for each faction.

### TFunding
- Manages XCOM's funding based on country scores and generates monthly reports.
- Operates from the country perspective and updates funding and relations.
- Tracks monthly scores and provides summary reports.

### TLocation
- Represents a single location on the world map (base, city, crash site, etc.).
- Handles radar detection, visibility, and cover mechanics for world map locations.
- Supports cover replenishment and visibility updates.

### TGlobalRadar
- Manages radar detection of UFOs and locations on the world map.
- Handles radar scanning from bases and crafts, updating cover and visibility for all locations.
- Integrates with TWorld and TLocation for detection logic.

---

## Integration Guide

- TBiome, TCountry, and TLocation are used for world map analytics, battle generation, and funding.
- TDiplomacy and TFunding manage strategic relations and monthly funding updates.
- TGlobalRadar is used for detection and visibility of all world map locations.
- All classes are designed for extensibility and integration with other game systems.

---

## API Reference

- See individual class docstrings and method signatures in the respective Python files for detailed API documentation.
- All classes are designed for use by both AI agents and human developers, with clear separation of entities, managers, and analytics.

---

*This README is automatically generated and should be kept in sync with code and documentation changes.*

