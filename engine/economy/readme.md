# Economy Module

This module implements the core economic systems for the XCOM/AlienFall game, including manufacturing, purchasing, research, black market, and transfer management. It provides the logic for all resource flows, project management, and economic interactions between bases, suppliers, and the world.

## Architecture Overview

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

## Subsystems

### Manufacturing System
- **Purpose:** Manage manufacturing projects, validate requirements, allocate workshop capacity, and track progress.
- **Key Classes:**
  - `TManufacture`: Main interface for manufacturing operations.
  - `TManufactureEntry`: Defines what can be manufactured.
  - `ManufacturingManager`: Manages active projects and workshop allocation.
  - `ManufacturingProject`: Tracks individual project progress.

### Purchase System
- **Purpose:** Handle purchasing of items, units, and crafts, including black market transactions, monthly limits, and delivery tracking.
- **Key Classes:**
  - `TPurchase`: Main interface for purchasing operations.
  - `TPurchaseEntry`: Defines what can be purchased.
  - `PurchaseManager`: Manages orders and deliveries.
  - `PurchaseOrder`: Tracks order status and delivery.
  - `BlackMarket`: Manages special suppliers and rotating stock.

### Research System
- **Purpose:** Manage research projects, scientist allocation, dependencies, and progress tracking.
- **Key Classes:**
  - `TResearchManager`: Main interface for research operations.
  - `TResearchEntry`: Defines researchable projects.
  - `ResearchProject`: Tracks research progress.
  - `TResearchTree`: Manages dependencies and unlocks.

### Transfer System
- **Purpose:** Handle all item, unit, and craft deliveries between bases and from suppliers.
- **Key Classes:**
  - `TTransfer`: Represents a single delivery.
  - `TransferManager`: Manages all active deliveries.

## Integration
- All subsystems are integrated with the main game loop for daily/monthly processing.
- Manufacturing and purchasing interact with the transfer system for deliveries.
- Research unlocks new manufacturing and purchasing options.
- Black market provides special purchase opportunities with unique mechanics.

## Testing & Documentation
- Each subsystem includes unit tests in the `test/` subfolder, covering core logic and edge cases where available. **Note:** Not all classes have full test coverage yet; test coverage is a work in progress. Check the `test/` subfolder for the latest status, and contributions to test coverage are welcome.
- All classes and methods are documented with docstrings following project standards.
- Comprehensive markdown documentation is provided for each subsystem, synchronized with the codebase.

---

For detailed API and class documentation, see the code docstrings and the subsystem markdown files:
- `MANUFACTURING_SYSTEM_DOCUMENTATION.md`
- `PURCHASE_SYSTEM_DOCUMENTATION.md`
- `RESEARCH_SYSTEM_DOCUMENTATION.md`

