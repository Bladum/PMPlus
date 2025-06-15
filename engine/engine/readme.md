# Engine Module

This document is the authoritative design and architecture reference for the XCOM/AlienFall core engine systems. It is intended for validation by AI agents and developers to ensure all planned features and classes are implemented as designed. All subsystem documentation is consolidated here.

## Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Class Purposes and Details](#class-purposes-and-details)
4. [Integration Guide](#integration-guide)
5. [API Reference](#api-reference)

---

## Overview

The engine module implements the core game engine systems, including mod loading, game state, animation, sound, and statistics.

## System Architecture

```
Engine Module
├── TMod, TItemCategory, TUnitCategory (mod.py)
├── TModLoader (modloader.py)
├── TGame (game.py)
├── TSoundManager (sounds.py)
├── TSaveGame (savegame.py)
├── TDifficulty (difficulty.py)
├── TStatistics (stats.py)
├── TAnimation (animation.py)
```

---

## Class Purposes and Details

- **TMod:** Main mod management class and core enumerations for the game engine.
- **TModLoader:** Loads and manages mods and game data.
- **TGame:** Represents the main game state and logic.
- **TSoundManager:** Handles sound playback and management.
- **TSaveGame:** Manages game save and load operations.
- **TDifficulty:** Represents game difficulty settings.
- **TStatistics:** Tracks and manages game statistics.
- **TAnimation:** Handles animation playback and updates.

---

## Integration Guide

- Use `TGame` for main game loop and state.
- Use `TModLoader` and `TMod` for mod and data management.

---

## API Reference

(See individual files for detailed method signatures.)
