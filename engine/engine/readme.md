# Engine Module Classes

This document summarizes the core classes in the `engine/engine/` directory, their purposes, attributes, and main methods.

---

## TAnimation
Manages visual animations in both tactical and strategic views. Controls unit movements, weapon effects, explosions, and other visual effects.
- **Attributes:** animations
- **Methods:** play_animation(), stop_animation(), update(), clear()

## TDifficulty
Controls game difficulty settings. Adjusts AI behavior, alien research progress, funding, and other parameters.
- **Attributes:** level, modifiers
- **Methods:** set_level(), get_modifier(), apply_modifiers()

## TSaveGame
Handles saving and loading game state. Manages serialization of all game objects and state.
- **Attributes:** save_path, last_saved
- **Methods:** save(), load(), get_save_metadata()

## TSoundManager
Manages all game sounds and music. Handles ambient sounds, battle effects, and UI feedback.
- **Attributes:** sounds, music_tracks
- **Methods:** play_sound(), play_music(), stop_all(), load_sounds()

## TStatistics
Tracks player performance metrics across the campaign. Records kills, mission success rates, and achievements.
- **Attributes:** kills, missions_completed, missions_failed, achievements
- **Methods:** record_kill(), record_mission_result(), add_achievement(), get_summary()

## TGame
Main game class (singleton). Holds all game data, including world map, campaigns, calendar, budget, research, mod data, and bases.
- **Attributes:** worldmap, campaigns, calendar, budget, funding, scoring, research_tree, mod, bases, current_base_name, base_labels
- **Methods:** get_active_base(), set_active_base(), set_active_base_by_index(), add_base(), remove_base(), base_exists(), get_base_status(), get_base_status_by_index(), get_current_base_units(), get_current_base_items(), get_current_base_crafts(), get_base_summary(), initialize_starting_bases()

## TModLoader
Loads and merges all YAML files from a mod's rules directory, building a unified dictionary (yaml_data) for use by TMod and the game engine.
- **Attributes:** mod_name, mod_path, yaml_data
- **Methods:** load_all_yaml_files()

---

For more details, see the class docstrings and the [API documentation](../../wiki/API.yml).
