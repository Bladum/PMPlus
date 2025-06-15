# Task 2: Module-Level README Generation

**Purpose:**
Aggregate high-level summaries of all Python files in a module into a single, well-structured `readme.md` within the same folder.

> **Important:**
> - You must analyze **every** Python file in the module (excluding files in `test` subfolders and those starting with `test_`).
> - Do **not** skip any files, regardless of the number of files in the module.
> - The README must reflect the current state of all code files in the module.

## Steps & Examples

1. **Scan All Python Files in the Module**  
   - Exclude files in `test` subfolders and those starting with `test_`.
   - **Scan all files in the folder, regardless of count.** Do not skip modules with more than 20 files.

2. **Purge Existing `readme.md`**  
   Before writing, clear any previous content.

3. **Document Each File and Class**  
   For each `.py` file, extract class names, docstrings, and method signatures.
   - **For each class, collect a more detailed description:**
     - Summarize the class’s purpose in 2–4 bullet points.
     - Include responsibilities, integration points, and any unique behaviors or design notes.

4. **README Structure**  
   *Example from `engine/economy/readme.md`:*
   ```markdown
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

   The economy module implements the core economic systems for the XCOM/AlienFall game,
   including manufacturing, purchasing, research, black market, and transfer management.
   It provides the logic for all resource flows, project management, and economic interactions
   between bases, suppliers, and the world.

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
   - **TManufacture**: High-level interface for all manufacturing operations. Loads project templates,
     validates requirements, and manages project lifecycle via ManufacturingManager. Provides methods for
     loading, filtering, and checking availability of manufacturing projects, as well as starting, pausing,
     resuming, and cancelling projects.
   - **TManufactureEntry**: Data template for a single manufacturing project, including requirements,
     costs, outputs, and metadata. Stores all data and requirements for a manufacturing project.
   - **ManufacturingManager**: Orchestrates all active manufacturing projects across bases, manages workshop
     capacity, and project state (pause, resume, cancel). Handles starting projects, daily progress, and resource
     management. Tracks active projects and workshop capacity per base.
   - **ManufacturingProject**: Represents a single manufacturing project in progress, tracking progress,
   ```

5. **Keep README, Code, and API Documentation in Sync**  
   Ensure the local `readme.md` describes what the file and its main class are doing.
   Update whenever code or documentation changes.
