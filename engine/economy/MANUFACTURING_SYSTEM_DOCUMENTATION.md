# Manufacturing System Comprehensive Documentation

## Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Core Classes](#core-classes)
4. [Manufacturing Flow](#manufacturing-flow)
5. [Mathematical Model](#mathematical-model)
6. [Comparison to UFO: Enemy Unknown](#comparison-to-ufo-enemy-unknown)
7. [Features and Capabilities](#features-and-capabilities)
8. [Usage Examples](#usage-examples)
9. [Integration Guide](#integration-guide)
10. [API Reference](#api-reference)

## Overview

The Manufacturing System is a comprehensive implementation inspired by the classic UFO: Enemy Unknown (X-COM: UFO Defense) manufacturing mechanics, enhanced with modern features like monthly invoicing, project management, and workshop capacity allocation.

### Key Features
- **Project-based Manufacturing**: Each manufacturing order is a separate project with its own lifecycle
- **Workshop Capacity Management**: Allocate man-days per day across multiple projects
- **Real-time Progress Tracking**: Daily progress simulation with completion estimates
- **Resource Validation**: Checks technology, services, items, and funding requirements
- **Monthly Invoicing**: Track manufacturing hours and generate cost reports
- **Project Management**: Pause, resume, cancel, and modify project quantities
- **Duplicate Prevention**: Ensures only one project per item type per base

## System Architecture

```
TManufacture (Main Interface)
├── ManufacturingManager (Project Orchestration)
│   ├── ManufacturingProject (Individual Projects)
│   └── Workshop Capacity Management
└── TManufactureEntry (Project Templates)

TGame (Hours Tracking & Invoicing)
├── Monthly Manufacturing Hours
└── Invoice Generation
```

### Data Flow
1. **Loading**: Manufacturing entries loaded from TOML configuration
2. **Validation**: Requirements checked (tech, services, items, money)
3. **Creation**: Projects instantiated and allocated workshop capacity
4. **Processing**: Daily progress advancement with hour tracking
5. **Completion**: Items produced and added to inventory
6. **Invoicing**: Monthly hour summaries and cost calculation

## Core Classes

### 1. TManufactureEntry
**Purpose**: Defines what can be manufactured - serves as project templates.

```python
class TManufactureEntry:
    """Manufacturing project template with requirements and outputs."""
    
    # Core Properties
    pid: str                    # Project ID
    name: str                   # Display name
    category: str               # Project category (weapons, supplies, etc.)
    
    # Production Data
    build_time: int             # Man-days required per item
    build_cost: int             # Money cost per item
    give_score: int             # Score awarded on completion
    
    # Requirements
    tech_start: list            # Required technologies
    items_needed: dict          # Required items with quantities
    services_needed: list       # Required base services
    region_needed: list         # Required regions (future use)
    country_needed: list        # Required countries (future use)
    
    # Outputs
    items_build: any            # Items produced
    units_build: any            # Units produced (future use)
    crafts_build: any           # Crafts produced (future use)
```

**Example Configuration**:
```toml
[manufacturing.pistol]
name = "Combat Pistol"
category = "weapons"
build_time = 5              # 5 man-days per pistol
build_cost = 1000           # $1000 per pistol
tech_start = ["basic_weapons"]
items_needed = { metal = 2, electronics = 1 }
services_needed = ["workshop"]
items_build = { pistol = 1 }
```

### 2. ManufacturingProject
**Purpose**: Represents an active manufacturing project in progress.

```python
class ManufacturingProject:
    """Active manufacturing project tracking progress and resources."""
    
    # Identification
    project_id: str             # Unique UUID
    entry_id: str               # Reference to TManufactureEntry
    base_id: str               # Base where manufacturing occurs
    
    # Project Parameters
    quantity: int               # Number of items to build
    workshop_capacity: int      # Allocated man-days per day
    
    # Progress Tracking
    progress: float             # Current progress in man-days
    total_time: float           # Total time required in man-days
    items_completed: int        # Items already finished
    
    # Timeline
    start_date: datetime        # Project start
    estimated_completion: datetime  # Projected finish
    
    # Status Management
    status: str                 # 'active', 'paused', 'completed', 'cancelled'
    cost_paid: bool            # Whether upfront cost was deducted
```

**Key Methods**:
- `advance_progress(daily_capacity)`: Process one day of work
- `get_completion_percentage()`: Current completion rate
- `get_remaining_time()`: Estimated days until completion
- `change_quantity(new_quantity)`: Modify item count
- `pause()`, `resume()`, `cancel()`: Status management

### 3. ManufacturingManager
**Purpose**: Orchestrates all active projects and manages workshop capacity.

```python
class ManufacturingManager:
    """Manages active projects across all bases."""
    
    # Data Storage
    active_projects: dict       # base_id -> [ManufacturingProject]
    workshop_capacity: dict     # base_id -> capacity in man-days/day
    
    # Core Operations
    def start_project(base_id, entry, quantity, capacity)
    def daily_progress(game=None)
    def get_project_summary(base_id)
    
    # Capacity Management
    def get_available_workshop_capacity(base_id)
    def can_start_project(base_id, entry, quantity, capacity)
    
    # Project Control
    def pause_project(project_id)
    def resume_project(project_id)
    def cancel_project(project_id)
    def change_project_quantity(project_id, new_quantity)
```

### 4. TManufacture
**Purpose**: Main interface providing high-level manufacturing operations.

```python
class TManufacture:
    """Primary manufacturing system interface."""
    
    # Data Management
    entries: dict               # project_id -> TManufactureEntry
    manufacturing_manager: ManufacturingManager
    
    # Core Operations
    def start_manufacturing_project(entry_id, base_id, quantity, ...)
    def process_daily_manufacturing(game=None)
    def get_available_projects(technologies, services, items)
    def validate_project_requirements(entry, base_id, quantity, ...)
    
    # Status & Control
    def get_manufacturing_status(base_id)
    def pause_project(project_id)
    def resume_project(project_id)
    def cancel_project(project_id)
    def change_project_quantity(project_id, new_quantity)
```

## Manufacturing Flow

### 1. Project Initiation
```python
# 1. Check availability
available_projects = manufacture.get_available_projects(
    available_technologies=['basic_weapons'],
    available_services=['workshop'],
    available_items={'metal': 10, 'electronics': 5}
)

# 2. Validate requirements
can_start, issues = manufacture.validate_project_requirements(
    entry, base_id, quantity, technologies, services, items, money
)

# 3. Start project
success, project = manufacture.start_manufacturing_project(
    'pistol', 'base_001', 100,  # 100 pistols
    technologies, services, items, money,
    workshop_capacity=10  # Allocate 10 man-days/day
)
```

### 2. Daily Processing
```python
# Process daily manufacturing progress
completed_items = manufacture.process_daily_manufacturing(game)

for base_id, completions in completed_items.items():
    for completion in completions:
        # Add completed items to inventory
        item_id = completion['entry_id']
        quantity = completion['items_completed']
        hours_worked = completion['hours_worked']
        
        # Track completion
        if completion['project_completed']:
            print(f"Project {completion['project_id']} finished!")
```

### 3. Monthly Invoicing
```python
# At month end
monthly_data = game.finalize_monthly_manufacturing("2025-06")
invoice = game.get_monthly_manufacturing_invoice("2025-06", hourly_rate=50)

print(f"Total manufacturing cost: ${invoice['total_cost']}")
for base_id, base_data in invoice['details'].items():
    print(f"Base {base_id}: ${base_data['total_cost']}")
    for project_id, project_data in base_data['projects'].items():
        print(f"  {project_id}: {project_data['hours']} hours = ${project_data['cost']}")
```

## Mathematical Model

### Core Calculations

#### 1. Time and Progress
- **Total Time Required**: `quantity × build_time_per_item`
- **Daily Progress**: `min(daily_capacity, allocated_capacity)`
- **Items Completed**: `floor(total_progress ÷ build_time_per_item)`
- **Completion Percentage**: `(current_progress ÷ total_time) × 100`

#### 2. Hour Conversion
- **Man-Hours per Day**: `man_days × 8 hours/day`
- **Monthly Hours**: Sum of daily hours worked

#### 3. Cost Calculation
- **Project Cost**: `quantity × build_cost_per_item`
- **Monthly Invoice**: `total_hours × hourly_rate`

### Example Calculations

#### Pistol Manufacturing
- **Item**: Combat Pistol
- **Build Time**: 5 man-days per pistol
- **Quantity**: 100 pistols
- **Workshop Capacity**: 10 man-days/day

**Calculations**:
- Total time: 100 × 5 = 500 man-days
- Duration: 500 ÷ 10 = 50 days
- Items per day: 10 ÷ 5 = 2 pistols/day
- Hours per day: 10 man-days × 8 = 80 hours/day
- Total hours: 50 days × 80 hours = 4,000 hours

#### Rifle Manufacturing (Complex Example)
- **Item**: Assault Rifle
- **Build Time**: 10 man-days per rifle
- **Quantity**: 20 rifles
- **Workshop Capacity**: 6 man-days/day

**Calculations**:
- Total time: 20 × 10 = 200 man-days
- Duration: 200 ÷ 6 = 33.33 days
- Items per day: 6 ÷ 10 = 0.6 rifles/day (1 rifle every ~1.67 days)
- Hours per day: 6 man-days × 8 = 48 hours/day

## Comparison to UFO: Enemy Unknown

### Similarities to Original X-COM
1. **Workshop-Based Production**: Manufacturing occurs in base workshops
2. **Resource Requirements**: Items need materials and money
3. **Time-Based Production**: Manufacturing takes time to complete
4. **Technology Gating**: Advanced items require research
5. **Base Management**: Each base has its own manufacturing capacity

### Enhanced Features (Beyond Original)
1. **Multiple Concurrent Projects**: Original allowed only one project per base
2. **Capacity Allocation**: Distribute workshop capacity across projects
3. **Project Management**: Pause, resume, cancel individual projects
4. **Progress Tracking**: Real-time completion percentages and estimates
5. **Monthly Invoicing**: Track manufacturing costs over time
6. **Quantity Modification**: Change project quantities after starting
7. **Requirement Validation**: Comprehensive pre-flight checks
8. **Hours Tracking**: Detailed time accounting for billing

### Original X-COM Manufacturing Process
```
1. Go to Manufacturing screen
2. Select item to manufacture
3. Set quantity
4. Confirm (deducts money immediately)
5. Wait for completion
6. Items appear in storage
```

### Enhanced System Process
```
1. Check available projects (filtered by requirements)
2. Validate all requirements (tech, services, items, money)
3. Start project with allocated capacity
4. Monitor progress daily
5. Adjust quantities or pause/resume as needed
6. Complete items incrementally
7. Generate monthly invoices
8. Track detailed manufacturing hours
```

### Technology Integration
**Original X-COM**: Simple research dependency
**Enhanced System**: Multi-layered requirements:
- Research technologies
- Base services (workshop, medical lab, etc.)
- Material availability
- Funding verification
- Workshop capacity allocation

## Features and Capabilities

### 1. Project Lifecycle Management
- **Creation**: Start projects with full requirement validation
- **Monitoring**: Track progress, completion estimates, and resource usage
- **Modification**: Change quantities, pause, resume, or cancel
- **Completion**: Automatic item generation and project cleanup

### 2. Workshop Capacity System
```python
# Set base capacity
manufacture.set_base_workshop_capacity("base_001", 20)  # 20 man-days/day

# Check capacity usage
status = manufacture.get_manufacturing_status("base_001")
print(f"Total: {status['total_capacity']}")
print(f"Used: {status['used_capacity']}")
print(f"Available: {status['available_capacity']}")
```

### 3. Resource Validation
```python
can_start, issues = manufacture.validate_project_requirements(
    entry, base_id, quantity,
    available_technologies=['basic_weapons', 'advanced_materials'],
    available_services=['workshop', 'precision_tools'],
    available_items={'metal': 100, 'electronics': 50},
    available_money=50000
)

if not can_start:
    for issue in issues:
        print(f"Requirement not met: {issue}")
```

### 4. Multi-Project Management
```python
# Start multiple projects
success1, pistol_project = manufacture.start_manufacturing_project(
    'pistol', base_id, 50, ..., workshop_capacity=10
)

success2, rifle_project = manufacture.start_manufacturing_project(
    'rifle', base_id, 20, ..., workshop_capacity=8
)

# Total capacity used: 10 + 8 = 18 man-days/day
```

### 5. Progress Tracking
```python
project = manufacture.get_project(project_id)
print(f"Progress: {project.get_completion_percentage():.1f}%")
print(f"Completed: {project.items_completed}/{project.quantity}")
print(f"Time remaining: {project.get_remaining_time():.1f} days")
print(f"Estimated completion: {project.estimated_completion}")
```

### 6. Monthly Invoicing
```python
# Track hours automatically during daily processing
completed = manufacture.process_daily_manufacturing(game)

# At month end
invoice = game.get_monthly_manufacturing_invoice("2025-06", hourly_rate=75)
print(f"Manufacturing bill: ${invoice['total_cost']}")

# Invoice structure:
{
    "total_cost": 15000,
    "details": {
        "base_001": {
            "total_cost": 10000,
            "projects": {
                "pistol": {"hours": 120, "cost": 9000},
                "medkit": {"hours": 13.33, "cost": 1000}
            }
        },
        "base_002": {
            "total_cost": 5000,
            "projects": {
                "rifle": {"hours": 66.67, "cost": 5000}
            }
        }
    }
}
```

## Usage Examples

### Basic Manufacturing Setup
```python
from engine.economy.manufacture import TManufacture
from engine.engine.game import TGame

# Load manufacturing data from TOML
manufacturing_data = {
    'manufacturing': {
        'pistol': {
            'name': 'Combat Pistol',
            'category': 'weapons',
            'build_time': 5,
            'build_cost': 1000,
            'tech_start': ['basic_weapons'],
            'items_needed': {'metal': 2, 'electronics': 1},
            'services_needed': ['workshop'],
            'items_build': {'pistol': 1}
        }
    }
}

# Initialize systems
game = TGame()
manufacture = TManufacture(manufacturing_data)

# Set up base workshop
base_id = "base_001"
manufacture.set_base_workshop_capacity(base_id, 15)  # 15 man-days/day
```

### Starting Manufacturing Projects
```python
# Define available resources
available_tech = ['basic_weapons', 'basic_medicine']
available_services = ['workshop', 'medical_lab']
available_items = {'metal': 100, 'electronics': 50, 'chemicals': 30}
available_money = 100000

# Check what can be built
available_projects = manufacture.get_available_projects(
    available_tech, available_services, available_items
)

print("Available manufacturing projects:")
for project in available_projects:
    print(f"- {project.name}: {project.build_time} man-days, ${project.build_cost}")

# Start a manufacturing project
success, project = manufacture.start_manufacturing_project(
    'pistol', base_id, 50,  # Build 50 pistols
    available_tech, available_services, available_items, available_money,
    workshop_capacity=10  # Allocate 10 man-days/day
)

if success:
    print(f"Started project {project.project_id}")
    print(f"Building {project.quantity} pistols")
    print(f"Total time: {project.total_time} man-days")
    print(f"Expected completion: {project.estimated_completion}")
else:
    print(f"Failed to start project: {project}")
```

### Daily Manufacturing Processing
```python
# Simulate daily operations
for day in range(1, 26):  # 25 days
    print(f"\n--- Day {day} ---")
    
    # Process manufacturing
    completed_items = manufacture.process_daily_manufacturing(game)
    
    if completed_items:
        for base_id, completions in completed_items.items():
            for completion in completions:
                print(f"Completed {completion['items_completed']} {completion['entry_id']}")
                print(f"Hours worked: {completion['hours_worked']}")
                
                if completion['project_completed']:
                    print(f"🎉 Project {completion['project_id']} finished!")
    
    # Check status
    status = manufacture.get_manufacturing_status(base_id)
    for project in status['projects']:
        if project.is_active():
            print(f"{project.entry_id}: {project.get_completion_percentage():.1f}% complete")
```

### Project Management
```python
# Pause a project
manufacture.pause_project(project_id)
print("Project paused")

# Resume later
manufacture.resume_project(project_id)
print("Project resumed")

# Change quantity
success, message = manufacture.change_project_quantity(project_id, 75)
if success:
    print(f"Quantity changed: {message}")
else:
    print(f"Cannot change quantity: {message}")

# Cancel project
manufacture.cancel_project(project_id)
print("Project cancelled")
```

### Monthly Financial Management
```python
# At month end
month_year = "2025-06"
monthly_data = game.finalize_monthly_manufacturing(month_year)

if monthly_data:
    print(f"Manufacturing activity for {month_year}:")
    for base_id, projects in monthly_data.items():
        print(f"Base {base_id}:")
        for entry_id, hours in projects.items():
            print(f"  {entry_id}: {hours} hours")

# Generate invoice
invoice = game.get_monthly_manufacturing_invoice(month_year, hourly_rate=60)
print(f"\nTotal manufacturing cost: ${invoice['total_cost']}")

# Detailed breakdown
for base_id, base_data in invoice['details'].items():
    print(f"\nBase {base_id}: ${base_data['total_cost']}")
    for project_id, project_data in base_data['projects'].items():
        print(f"  {project_id}: {project_data['hours']} hours @ $60/hour = ${project_data['cost']}")
```

## Integration Guide

### 1. Game Loop Integration
```python
class GameEngine:
    def __init__(self):
        self.game = TGame()
        self.manufacture = TManufacture(manufacturing_data)
    
    def daily_update(self):
        # Process manufacturing
        completed_items = self.manufacture.process_daily_manufacturing(self.game)
        
        # Add completed items to inventory
        for base_id, completions in completed_items.items():
            for completion in completions:
                self.add_items_to_base_inventory(
                    base_id, 
                    completion['entry_id'], 
                    completion['items_completed']
                )
    
    def monthly_billing(self, month_year):
        # Generate and process invoice
        invoice = self.game.get_monthly_manufacturing_invoice(month_year)
        self.deduct_funds(invoice['total_cost'])
        
        # Archive monthly data
        self.game.finalize_monthly_manufacturing(month_year)
```

### 2. UI Integration
```python
class ManufacturingUI:
    def show_available_projects(self):
        projects = self.manufacture.get_available_projects(
            self.get_available_technologies(),
            self.get_available_services(),
            self.get_available_items()
        )
        
        for project in projects:
            self.display_project_option(project)
    
    def show_active_projects(self, base_id):
        status = self.manufacture.get_manufacturing_status(base_id)
        
        for project in status['projects']:
            if project.is_active():
                self.display_project_progress(project)
    
    def handle_start_project(self, entry_id, quantity):
        success, result = self.manufacture.start_manufacturing_project(
            entry_id, self.current_base_id, quantity,
            self.get_available_technologies(),
            self.get_available_services(),
            self.get_available_items(),
            self.get_available_money(),
            self.get_allocated_capacity()
        )
        
        if success:
            self.show_success_message(f"Started manufacturing project: {result.project_id}")
        else:
            self.show_error_message(f"Cannot start project: {result}")
```

### 3. Save/Load Integration
```python
def save_manufacturing_state(self):
    return {
        'active_projects': self.manufacture.manufacturing_manager.active_projects,
        'workshop_capacity': self.manufacture.manufacturing_manager.workshop_capacity,
        'current_month_hours': self.game.current_month_manufacturing,
        'monthly_hours_archive': self.game.monthly_manufacturing_hours
    }

def load_manufacturing_state(self, data):
    self.manufacture.manufacturing_manager.active_projects = data['active_projects']
    self.manufacture.manufacturing_manager.workshop_capacity = data['workshop_capacity']
    self.game.current_month_manufacturing = data['current_month_hours']
    self.game.monthly_manufacturing_hours = data['monthly_hours_archive']
```

## API Reference

### TManufacture Class

#### Core Methods

##### `start_manufacturing_project(entry_id, base_id, quantity, available_technologies, available_services, available_items, available_money, workshop_capacity)`
Start a new manufacturing project.

**Parameters:**
- `entry_id` (str): Manufacturing entry ID
- `base_id` (str): Base where project will run
- `quantity` (int): Number of items to build
- `available_technologies` (list): Available technologies
- `available_services` (list): Available services
- `available_items` (dict): Available items in storage
- `available_money` (int): Available money
- `workshop_capacity` (int): Workshop capacity to allocate

**Returns:**
- `tuple`: (success: bool, project_or_error: ManufacturingProject or str)

##### `process_daily_manufacturing(game=None)`
Process daily manufacturing progress.

**Parameters:**
- `game` (TGame, optional): Game instance for tracking hours

**Returns:**
- `dict`: Completed items by base

##### `get_available_projects(available_technologies, available_services, available_items)`
Get list of manufacturing projects available based on requirements.

**Parameters:**
- `available_technologies` (list): List of researched technologies
- `available_services` (list): List of available base services
- `available_items` (dict): Dictionary of available items

**Returns:**
- `list`: List of available TManufactureEntry objects

##### `validate_project_requirements(entry, base_id, quantity, available_technologies, available_services, available_items, available_money)`
Validate all requirements for starting a manufacturing project.

**Returns:**
- `tuple`: (can_start: bool, issues: list)

##### `get_manufacturing_status(base_id)`
Get manufacturing status for a base.

**Returns:**
- `dict`: Status information including capacity usage and active projects

##### `change_project_quantity(project_id, new_quantity)`
Change the quantity of items in a project.

**Returns:**
- `tuple`: (success: bool, message: str)

##### `pause_project(project_id)`, `resume_project(project_id)`, `cancel_project(project_id)`
Control project lifecycle.

### ManufacturingProject Class

#### Key Properties
- `project_id`: Unique identifier
- `entry_id`: Reference to manufacturing entry
- `quantity`: Number of items to build
- `progress`: Current progress in man-days
- `total_time`: Total time required
- `items_completed`: Items already finished
- `status`: Current status ('active', 'paused', 'completed', 'cancelled')

#### Key Methods
- `advance_progress(daily_capacity)`: Process one day of work
- `get_completion_percentage()`: Get completion percentage
- `get_remaining_time()`: Get estimated remaining time
- `change_quantity(new_quantity)`: Modify quantity
- `pause()`, `resume()`, `cancel()`: Status control

### TGame Manufacturing Methods

#### `track_manufacturing_hours(base_id, entry_id, hours)`
Track manufacturing hours for monthly invoicing.

#### `finalize_monthly_manufacturing(month_year)`
Finalize and archive manufacturing hours for a month.

#### `get_monthly_manufacturing_invoice(month_year, hourly_rate=50)`
Generate invoice for a month's manufacturing activity.

---

## Conclusion

This manufacturing system provides a robust, feature-rich implementation that builds upon the classic X-COM foundation while adding modern project management capabilities. The system is designed for scalability, maintainability, and ease of integration into larger game systems.

Key strengths:
- **Comprehensive Resource Management**: Full validation of all requirements
- **Flexible Project Control**: Modify, pause, resume, and cancel projects
- **Accurate Progress Tracking**: Real-time completion estimates and progress monitoring
- **Financial Integration**: Detailed cost tracking and monthly invoicing
- **Scalable Architecture**: Support for multiple bases and concurrent projects

The system successfully captures the strategic depth of the original X-COM manufacturing while providing the tools needed for modern game development and management.
