# AI Module

This document is the authoritative design and architecture reference for the XCOM/AlienFall AI systems. It is intended for validation by AI agents and developers to ensure all planned features and classes are implemented as designed. All subsystem documentation is consolidated here.

## Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Class Purposes and Details](#class-purposes-and-details)
4. [Integration Guide](#integration-guide)
5. [API Reference](#api-reference)

---

## Overview

The AI module implements the core artificial intelligence systems for the XCOM/AlienFall game, including tactical battle AI and grand strategy AI for alien forces. It provides the logic for enemy unit decision-making, target selection, movement, and high-level alien strategy.

## System Architecture

```
AI Module
├── TBattleAI (tactical battle AI)
└── TAlienStrategy (grand strategy controller)
```

---

## Class Purposes and Details

### TBattleAI
- Handles artificial intelligence for enemy units during tactical battles.
- Controls unit movement, target selection, and tactical decisions for each AI-controlled unit.
- Integrates with the battle state, including units, map, and objectives.
- Designed for extensibility to support advanced tactics and behaviors.

### TAlienStrategy
- Controls the grand strategy of alien forces.
- Decides which regions to target for terror missions and base establishment.
- Adapts alien tactics based on player actions and game progression.
- Provides a high-level interface for strategic decision-making by the AI.

---

## Integration Guide

- TBattleAI is used during tactical battles to control enemy unit actions each turn.
- TAlienStrategy is used on the strategic layer to determine alien objectives and adapt to player progress.
- Both classes are imported in the AI module's `__init__.py` for unified access.

---

## API Reference

- See individual class docstrings and method signatures in the respective Python files for detailed API documentation.
- All classes are designed for use by both AI agents and human developers, with clear separation of tactical and strategic AI logic.

---

*This README is automatically generated and should be kept in sync with code and documentation changes.*

