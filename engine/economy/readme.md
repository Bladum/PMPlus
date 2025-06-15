# Economy Module

This document is the authoritative design and architecture reference for the XCOM/AlienFall economy systems. It is intended for validation by AI agents and developers to ensure all planned features and classes are implemented as designed. All subsystem documentation is consolidated here.

## Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Class Purposes and Details](#class-purposes-and-details)
4. [Integration Guide](#integration-guide)
5. [API Reference](#api-reference)

---

## Overview

The economy module implements the core economic systems for the XCOM/AlienFall game, including manufacturing, purchasing, research, black market, and transfer management. It provides the logic for all resource flows, project management, and economic interactions between bases, suppliers, and the world.

## System Architecture

```
Economy Module
├── Manufacturing System
│   ├── TManufacture (main interface)
│   ├── TManufactureEntry (project templates)
│   ├── ManufacturingManager (active projects)
│   └── ManufacturingProject (project progress)
├── Purchase System
│   ├── TPurchase (main interface)
│   ├── TPurchaseEntry (purchase templates)
│   ├── PurchaseManager (order management)
│   ├── PurchaseOrder (order tracking)
│   └── BlackMarket (special suppliers)
├── Research System
│   ├── TResearchManager (main interface)
│   ├── TResearchEntry (research templates)
│   ├── ResearchProject (active research)
│   └── TResearchTree (dependency management)
└── Transfer System
    ├── TTransfer (single delivery)
    └── TransferManager (all deliveries)
```

---

## Class Purposes and Details

### Manufacturing System
- **TManufacture**: High-level interface for all manufacturing operations. Loads project templates, validates requirements, and manages project lifecycle via ManufacturingManager. Provides methods for loading, filtering, and checking availability of manufacturing projects, as well as starting, pausing, resuming, and cancelling projects.
- **TManufactureEntry**: Data template for a single manufacturing project, including requirements, costs, outputs, and metadata. Stores all data and requirements for a manufacturing project.
- **ManufacturingManager**: Orchestrates all active manufacturing projects across bases, manages workshop capacity, and project state (pause, resume, cancel). Handles starting projects, daily progress, and resource management. Tracks active projects and workshop capacity per base.
- **ManufacturingProject**: Represents a single manufacturing project in progress, tracking progress, resources, and completion. Handles project status, progress calculation, and delivery.

### Purchase System
- **TPurchase**: Main purchasing system interface. Manages purchase entries, validation, order processing, and black market integration. Integrates with PurchaseManager and BlackMarket for order and supplier management.
- **TPurchaseEntry**: Template for a purchasable entry (item/unit/craft). Stores requirements, outputs, and metadata for a purchase.
- **PurchaseManager**: Manages active purchase orders across all bases. Handles order processing, delivery scheduling, and transfer integration. Tracks monthly purchases and order history.
- **PurchaseOrder**: Represents a purchase order made by the player. Tracks items, units, and crafts to be purchased, their quantities, delivery tracking, and order status. Integrates with transfer system for delivery.
- **BlackMarket**: Manages all black market suppliers, discovery, and global reputation. Handles special suppliers with limited availability, rotating stock, price variance, and discovery mechanics.
- **BlackMarketSupplier**: Represents a single black market supplier with unique rules, stock, and discovery requirements.

### Research System
- **TResearchManager**: Orchestrates all research operations, including entry management, project lifecycle, daily progress, and completion logic. Manages available, ongoing, and completed research.
- **TResearchEntry**: Template for a research project, storing all data and requirements for a research project.
- **ResearchProject**: Represents an active research project in a base, tracking progress, assigned capacity, and status. Handles progress advancement, completion, and status management.
- **TResearchTree**: Manages the research tree structure, dependencies, progress, and visualization. Handles randomization of costs, dependency unlocking, and research status tracking.

### Transfer System
- **TTransfer**: Represents a single delivery in transit (item, craft, or unit). Tracks delivery status, days remaining, and delivery completion.
- **TransferManager**: Manages all active deliveries and their progress. Handles daily updates, delivery completion, and cancellation.

---

## Integration Guide

- Manufacturing, purchasing, and research systems are tightly integrated. Manufacturing and purchasing both use transfer management for deliveries. Research unlocks new manufacturing and purchasing options.
- Black market suppliers are managed by the BlackMarket class and can provide unique purchase entries with special rules.
- All systems are designed for extensibility and integration with base, item, and event systems.

---

## API Reference

- See individual class docstrings and method signatures in the respective Python files for detailed API documentation.
- All classes are designed for use by both AI agents and human developers, with clear separation of data templates, managers, and active project/order objects.

---

*This README is automatically generated and should be kept in sync with code and documentation changes.*

