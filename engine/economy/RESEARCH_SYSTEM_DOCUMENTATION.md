# Research System Comprehensive Documentation

## Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Core Classes](#core-classes)
4. [Research Flow](#research-flow)
5. [Mathematical Model](#mathematical-model)
6. [Comparison to UFO: Enemy Unknown](#comparison-to-ufo-enemy-unknown)
7. [Features and Capabilities](#features-and-capabilities)
8. [Usage Examples](#usage-examples)
9. [Integration Guide](#integration-guide)
10. [API Reference](#api-reference)

## Overview

The Research System implements X-COM-style research mechanics, supporting project-based research, scientist allocation, dependency management, and real-time progress tracking. It is designed for extensibility and integration with other economic systems (manufacturing, purchasing).

### Key Features
- **Project-based Research**: Each research order is a separate project with its own lifecycle
- **Scientist/Capacity Allocation**: Assign research capacity per project, per base
- **Real-time Progress Tracking**: Daily progress simulation with completion estimates
- **Requirement Validation**: Checks technology, services, items, and facility requirements
- **Project Management**: Pause, resume, cancel, and modify project capacity
- **Dependency Management**: Research unlocks new projects as dependencies are met
- **Visualization**: Research tree and dependency visualization

## System Architecture

```
TResearchManager (Main Interface)
├── ResearchProject (Active Projects)
├── TResearchEntry (Project Templates)
└── TResearchTree (Dependency Management)

TGame (Integration Layer)
├── Daily Research Progress
└── Research Completion Effects
```

### Data Flow
1. **Loading**: Research entries loaded from configuration
2. **Validation**: Requirements checked (tech, services, items, facilities)
3. **Creation**: Projects instantiated and allocated research capacity
4. **Processing**: Daily progress advancement
5. **Completion**: Research completed, effects applied, and capacity freed

## Core Classes

### 1. TResearchEntry
**Purpose**: Defines what can be researched - serves as project templates.

```python
class TResearchEntry:
    """Research project template with requirements and effects."""
```

**Example Configuration**:
```toml
[research.alien_alloys]
name = "Alien Alloys"
cost = 30              # 30 man-days
tech_needed = ["alien_materials"]
items_needed = { alien_artifact = 1 }
services_needed = ["lab"]
```

### 2. ResearchProject
**Purpose**: Represents an active research project in a base.

```python
class ResearchProject:
    """Active research project tracking progress and capacity."""
```

**Key Methods**:
- `advance_progress(amount)`: Process one day of work
- `get_completion_percentage(entry_cost)`: Current completion rate
- `get_remaining_time(entry_cost)`: Estimated days until completion
- `change_capacity(new_capacity)`: Modify assigned capacity
- `pause()`, `resume()`, `cancel()`: Status management

### 3. TResearchManager
**Purpose**: Orchestrates all active projects and manages research entries and completion.

```python
class TResearchManager:
    """Manages active research projects and entries."""
    def get_available_research(base_id, technologies, items, services, facilities)
    def start_research_project(entry_id, base_id, assigned_capacity)
    def process_daily_research()
    def get_research_status(base_id)
    def complete_research_project(project_id)
```

### 4. TResearchTree
**Purpose**: Manages research dependencies, progress, and visualization.

```python
class TResearchTree:
    """Manages research tree, dependencies, and scientist assignment."""
    def add_entry(entry)
    def start_research(tech_id)
    def progress_research(tech_id, points)
    def complete_research(tech_id)
    def get_available_research()
    def assign_scientists(tech_id, scientists)
    def daily_progress()
    def visualize_dependencies()
```

## Research Flow

### 1. Project Initiation
```python
# 1. Check availability
available_research = research_manager.get_available_research(
    base_id='base_001',
    technologies=['alien_materials'],
    items={'alien_artifact': 2},
    services=['lab'],
    facilities=['advanced_lab']
)

# 2. Start project
success, project = research_manager.start_research_project(
    entry_id='alien_alloys',
    base_id='base_001',
    assigned_capacity=5
)
```

### 2. Daily Processing
```python
# Process daily research progress
completed_projects = research_manager.process_daily_research()
```

## Mathematical Model

### Core Calculations

#### 1. Time and Progress
- **Total Time Required**: `cost` (man-days)
- **Daily Progress**: `assigned_capacity` (man-days/day)
- **Completion Percentage**: `(progress / cost) × 100`

#### 2. Capacity Management
- **Capacity Assignment**: Each project can have a different assigned capacity
- **Capacity is freed when project completes or is paused/cancelled**

## Comparison to UFO: Enemy Unknown

### Similarities to Original X-COM
1. **Base-Specific Research**: Research is managed per base
2. **Scientist Assignment**: Capacity (scientists) is allocated per project
3. **Dependency Gating**: Research unlocks new projects
4. **Project Lifecycle**: Start, progress, complete, pause, resume, cancel

### Enhanced Features (Beyond Original)
1. **Multiple Concurrent Projects**: Multiple research projects per base
2. **Capacity Allocation**: Assign different capacity to each project
3. **Requirement Validation**: Checks for items, services, and facilities
4. **Visualization**: Research tree and dependency graph
5. **Project Management**: Change capacity, pause, resume, cancel

## Features and Capabilities

### 1. Project Lifecycle Management
- **Creation**: Start projects with full requirement validation
- **Monitoring**: Track progress, completion estimates, and resource usage
- **Modification**: Change capacity, pause, resume, or cancel
- **Completion**: Automatic research unlock and project cleanup

### 2. Capacity System
```python
# Assign capacity to a project
project.change_capacity(10)  # 10 man-days/day
```

### 3. Requirement Validation
```python
available = research_manager.get_available_research(
    base_id, technologies, items, services, facilities
)
```

### 4. Multi-Project Management
```python
# Start multiple projects
success1, proj1 = research_manager.start_research_project('alien_alloys', base_id, 5)
success2, proj2 = research_manager.start_research_project('plasma_rifle', base_id, 8)
```

### 5. Progress Tracking
```python
status = research_manager.get_research_status(base_id)
for proj in status:
    print(f"{proj['name']}: {proj['completion_pct']:.1f}% done")
```

## Usage Examples

```python
# Start a research project
success, project = research_manager.start_research_project('plasma_rifle', 'base_001', 6)

# Advance all projects by one day
completed = research_manager.process_daily_research()

# Pause a project
research_manager.pause_project(project.id)

# Resume a project
research_manager.resume_project(project.id)

# Cancel a project
research_manager.cancel_project(project.id)
```

## Integration Guide

- Integrate with base management to track available research capacity
- Call `process_daily_research()` on each game day
- Apply research completion effects (unlock tech, spawn items, trigger events) in game logic

## API Reference

### TResearchManager Class Methods
- `get_available_research(base_id, technologies, items, services, facilities) -> List[TResearchEntry]`
- `start_research_project(entry_id, base_id, assigned_capacity) -> Tuple[bool, ResearchProject]`
- `process_daily_research() -> List[ResearchProject]`
- `get_research_status(base_id=None) -> List[dict]`
- `complete_research_project(project_id) -> bool`
- `pause_project(project_id) -> None`
- `resume_project(project_id) -> None`
- `cancel_project(project_id) -> None`

### ResearchProject Methods
- `advance_progress(amount=None)`
- `get_completion_percentage(entry_cost)`
- `get_remaining_time(entry_cost)`
- `change_capacity(new_capacity)`
- `pause()`, `resume()`, `cancel()`, `complete()`

### TResearchTree Methods
- `add_entry(entry)`
- `start_research(tech_id)`
- `progress_research(tech_id, points)`
- `complete_research(tech_id)`
- `get_available_research()`
- `assign_scientists(tech_id, scientists)`
- `daily_progress()`
- `visualize_dependencies()`
- `export_dependencies_to_file(filepath)`
- `visualize_dependencies_tree()`
- `export_dependencies_tree_to_file(filepath)`

---

This comprehensive research system provides all the functionality needed for an XCOM-style research and technology progression system, with full integration into the existing game architecture.
