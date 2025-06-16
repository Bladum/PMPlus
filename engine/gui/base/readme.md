# GUI Base Module

This document is the authoritative design and architecture reference for the XCOM/AlienFall base GUI systems. It is intended for validation by AI agents and developers to ensure all planned features and classes are implemented as designed. All subsystem documentation is consolidated here.

## Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Class Purposes and Details](#class-purposes-and-details)
4. [Integration Guide](#integration-guide)
5. [API Reference](#api-reference)

---

## Overview

The base GUI module implements the core user interface screens for base management in XCOM/AlienFall, including barracks, hangar, storage, purchasing, manufacturing, research, and more. It provides the logic and widgets for all major base activities and navigation.

## System Architecture

```
Base GUI Module
├── TGuiBaseTopPanel (top navigation panel)
├── TGuiBarracks (unit and inventory management)
├── TGuiHangar (craft management)
├── TGuiStorage (base storage management)
├── TGuiPurchaseGui (purchasing interface)
├── TGuiWorkshop (manufacturing interface)
├── TGuiLab (science/research interface)
├── TGuiMarket (market/purchase interface)
├── TGuiPrison (containment interface)
├── TGuiFacility (facility management)
├── TGuiBaseInfo (base summary)
├── TGuiTransfer (inter-base transfer)
├── TGuiAcademy (manufacturing/training)
├── TGuiArchive (research/records)
```

## Class Purposes and Details

### TGuiBaseTopPanel
- Implements the top navigation bar for the game interface.
- Provides screen switching and base selection.
- Displays current base, date, and funds.
- Integrates with GameData and emits signals for navigation.

### TGuiBarracks
- Main barracks GUI for unit and inventory management.
- Allows viewing, equipping, and managing units.
- Supports loadout templates and unit stats display.
- Integrates with unit inventory and item systems.

### TGuiHangar
- Main hangar GUI for craft management.
- Allows viewing and managing crafts in the base.

### TGuiStorage
- Main storage GUI for base storage management.
- Allows viewing and managing stored items.

### TGuiPurchaseGui
- Main purchasing interface for items, units, and crafts.
- Supports standard and black market purchases.
- Displays active orders and integrates with purchase system.

### TGuiWorkshop
- Main workshop GUI for manufacturing management.
- Allows managing manufacturing projects and progress.

### TGuiLab
- Main laboratory GUI for science and research management.
- Allows managing research projects and scientists.

### TGuiMarket
- Main market GUI for purchases.
- Allows browsing and buying from the market.

### TGuiPrison
- Main prison GUI for containment management.
- Allows viewing and managing prisoners/aliens.

### TGuiFacility
- Main facility GUI for base facility management.
- Allows building and managing base facilities.

### TGuiBaseInfo
- Main base info summary GUI screen.
- Displays overview of base activities and status.

### TGuiTransfer
- Main transfer GUI for inter-base transfers.
- Allows managing and tracking transfers between bases.

### TGuiAcademy
- Main academy GUI for manufacturing/training.
- Allows managing training and manufacturing in the academy.

### TGuiArchive
- Main archive GUI for research/records.
- Allows viewing research progress and records.

## Integration Guide
- All screens inherit from TGuiCoreScreen for consistent interface and integration.
- Navigation is managed via TGuiBaseTopPanel.
- Each screen connects to relevant game systems (unit, item, purchase, etc.).

## API Reference
- See individual class docstrings for method and attribute details.
