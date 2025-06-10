# Economy Module

This folder contains classes for managing the economic systems in the game, including manufacturing, purchasing, research, and transfers.

## TManufacture
Manages a collection of manufacturing projects and their entries. Provides methods to load, filter, and check the availability of manufacturing projects.
- **Attributes:** entries (dict of project_id -> TManufactureEntry)
- **Methods:** load(), get_entry(), get_projects_by_category(), get_available_projects()

## TManufactureEntry
Represents a single manufacturing project entry, storing all data and requirements for a manufacturing project.
- **Attributes:** pid, name, category, build_time, build_cost, give_score, tech_start, items_needed, services_needed, region_needed, country_needed, items_build, units_build, crafts_build
- **Methods:** __init__()

## PurchaseOrder
Represents a purchase order made by the player, handling items, units, and crafts to be purchased, their quantities, and order status.
- **Attributes:** id, base_id, items, units, crafts, status
- **Methods:** is_empty(), mark_processed(), mark_cancelled(), calculate_total_cost()

## TPurchaseEntry
Represents a purchasable entry (item/unit/craft) that can be purchased, with all requirements and results.
- **Attributes:** pid, name, category, supplier, purchase_cost, purchase_time, tech_needed, items_needed, services_needed, region_needed, country_needed, items_buy, units_buy, crafts_buy
- **Methods:** __init__()

## TResearchEntry
Represents a research entry (project) that can be researched, with all requirements and results.
- **Attributes:** pid, name, cost, score, tech_needed, items_needed, services_needed, event_spawn, item_spawn, tech_disable, tech_give, tech_unlock, pedia, complete_game
- **Methods:** __init__()

## TResearchTree
Manages the research tree, research progress, dependencies, and visualization.
- **Attributes:** entries, completed, in_progress, available, locked
- **Methods:** add_entry(), start_research(), progress_research(), complete_research(), get_research_progress(), get_available_research(), assign_scientists(), progress_all_research(), daily_progress(), is_completed(), lock_entry(), unlock_entry(), get_entry(), reset(), visualize_dependencies(), export_dependencies_to_file(), visualize_dependencies_tree(), export_dependencies_tree_to_file()

## TTransfer & TransferManager
TTransfer represents a single transit for one item, craft, or unit. TransferManager manages all transits and handles daily updates and delivery to base storage.
- **Attributes (TTransfer):** id, base_id, object_type, object_id, quantity, days_left, status
- **Methods (TTransfer):** tick(), is_delivered(), cancel()
- **Attributes (TransferManager):** transits
- **Methods (TransferManager):** add_transit(), tick_all()

---

All classes are documented and follow the BIS coding agent best practices. See `wiki/API.yml` for parameter documentation.

