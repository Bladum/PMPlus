# Unit Module

This folder contains classes for unit representation, stats, traits, inventory, and related logic in the game.

## Classes

### TRace
Represents a race (type of unit) and its basic stats, abilities, and AI behavior.
- **Attributes:** pid, name, description, sprite, is_big, is_mechanical, gain_experience, health_regen, sound_death, corpse_image, stats, aggression, intelligence, immune_panic, immune_pain, immune_bleed, can_run, can_kneel, can_sneak, can_surrender, can_capture, spawn_on_death, avoids_fire, spotter, sniper, sell_cost, female_frequency, level_max, level_train, level_start
- **Methods:** __init__

### TSide
Represents a faction or side in the game (e.g., player, alien, civilian).
- **Attributes:** XCOM, ALIEN, CIVILIAN, ALLIED

### TTrait
Base class for all unit traits (promotions, wounds, effects, etc.), modifying stats and abilities.
- **Attributes:** id, name, sprite, description, type, stats, cost, items_needed, races, min_level, max_level, services_needed, tech_needed, recovery_time, transfer_time, battle_duration, battle_effect, battle_chance_complete, battle_only
- **Methods:** __init__, get_stat_modifiers

### TUnit
Represents an individual unit in the game with all its attributes and capabilities. Handles stats, equipment, traits, and status for gameplay.
- **Attributes:** game, unit_type, side_id, name, nationality, face, female, stats, race, traits, inventory_manager, inventory, position, direction, alive, dead, mind_controlled, panicked, crazy, stunned, kneeling, running
- **Methods:** __init__, calculate_stats, armour, weapon, equipment

### TUnitInventoryManager
Unified inventory manager for a single unit. Handles slot logic, stat modification, template save/load, dynamic slot availability, and auto-equip.
- **Attributes:** unit, equipment_slots, slot_types, available_slots, stat_modifiers, _template, _named_templates
- **Methods:** __init__, equip_item, unequip_item, get_total_weight, get_available_slots, save_template, load_template, save_named_template, load_named_template, list_templates, clear_all, get_all_items, to_dict, from_dict, auto_equip

### TUnitStats
Represents a unit's stats and provides methods to manage them during the game.
- **Attributes:** health, speed, strength, energy, aim, melee, reflex, psi, bravery, sanity, sight, sense, cover, morale, action_points, size, action_points_left, energy_left, hurt, stun, morale_left
- **Methods:** __init__, receive_damage, receive_stun, restore_health, restore_stun, restore_energy, restore_morale, use_ap, new_game, new_turn, action_rest, get_effective_ap, is_alive, is_conscious, is_panicked, is_crazy, get_sight, get_health_left, get_stun_left, __add__, sum_with, __repr__

### TUnitType
Represents a type/template of unit with stats, race, traits, and equipment. Used as a template for creating units in the game.
- **Attributes:** pid, name, race, sprite, rank, traits, armour, primary, secondary, score_dead, score_alive, items_dead, items_alive, ai_ignore, vip, drop_items, drop_armour
- **Methods:** __init__, create_unit_from_template

---

See also: `wiki/unit.md` for more details on unit mechanics and structure.
