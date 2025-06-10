# engine/base/ README

## TBaseXComBattleGenerator
TBaseXComBattleGenerator generates a tactical battle map layout for an XCOM base using its facilities and their positions.
- **Attributes:** base
- **Methods:** __init__(), generate_battle_map()

## TBaseXCom
TBaseXCom represents an XCOM base on the world map, managing facilities, inventory, and base serialization.
- **Attributes:** facilities, inventory, game
- **Methods:** __init__(), add_facility(), remove_facility(), update_inventory_capacities(), can_build_facility(), can_place_facility_at(), build_day(), get_active_facilities(), get_services_provided(), get_total_capacity(), get_storage_space(), get_unit_space(), get_prison_space(), get_alien_space(), get_craft_space(), get_hospital_space(), get_training_space(), get_workshop_space(), get_research_space(), get_psi_space(), get_relax_space(), get_repair_space(), get_radar_facilities(), get_defense_facilities(), add_item(), remove_item(), get_item_quantity(), consume_items(), add_unit(), remove_unit(), get_units_count(), get_units_by_type(), add_craft(), remove_craft(), get_crafts_count(), get_crafts_by_type(), add_capture(), remove_capture(), get_capture_quantity(), save_data(), load_data()

---
This folder contains classes for base facility management, battle map generation, and inventory handling. See code docstrings for details.

