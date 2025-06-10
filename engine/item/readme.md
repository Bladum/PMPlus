# Item Module

This folder contains the core item classes for the XCOM/AlienFall engine. Each file defines a specific type of item or item-related system used in the game, such as weapons, armor, craft equipment, and inventory transfer logic.

## Modules and Classes

- **item.py**: Defines `TItem`, the base class for all game items. Handles core properties, serialization, and inventory compatibility.
- **item_armour.py**: Defines `TItemArmour`, representing armor items with shield and resistance logic.
- **item_craft.py**: Defines `TCraftItem`, for craft/vehicle-specific equipment and state.
- **item_mode.py**: Defines `TWeaponMode`, representing weapon firing/usage modes.
- **item_transfer.py**: Defines `TItemTransferManager`, managing drag-and-drop and inventory slot transfers.
- **item_type.py**: Defines `TItemType`, the static template for all item types and their parameters.
- **item_weapon.py**: Defines `TItemWeapon`, representing weapons with multiple firing modes and ammo logic.

## item_mode.py
TWeaponMode represents a specific firing/usage mode for weapons. It defines operational modes (snap, aimed, auto, etc.) with modifiers for accuracy, damage, AP cost, and shot count.
- **Attributes:** pid, name, key, ap_cost_modifier, range_modifier, accuracy_modifier, shots, damage_modifier
- **Methods:** __init__(), apply()

## item_transfer.py
TItemTransferManager manages the transfer of items between inventory slots. It handles drag-and-drop, compatibility checks, swap logic, and undo/redo history for inventory systems.
- **Attributes:** item_transfer_started, item_transfer_completed, item_transfer_cancelled, inventory_updated, MIME_TYPE, _current_drag_item, _source_widget, _source_id, _validate_slot_compatibility, _history, _history_index, _history_max, _swap_buffer
- **Methods:** __init__(), start_drag(), can_accept_drop(), accept_drop(), get_current_drag_item(), get_source_widget(), get_source_id(), record_inventory_action(), undo(), redo(), get_item_compatibility_report()

## Usage Notes
- All item classes inherit from `TItem` and use `TItemType` for static parameters.
- Inventory and equipment systems interact with these classes for all item management.
- See each file and class docstring for details on attributes and methods.

---

For detailed class summaries and API documentation, see the code docstrings and the synchronized `wiki/API.yml` file.
