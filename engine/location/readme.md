# Location Module

This folder contains classes for representing locations and mission sites on the world map in the game. Each class is responsible for a specific type of location or related logic.

## TCity
Represents a city on the world map as a location.
- **Attributes:** size, name, description, terrains
- **Methods:** get_random_terrain()

## TSite
Represents a static mission site (not a UFO or base) on the world map.
- **Attributes:** site_type, map_blocks, game
- **Methods:** generate_random_map_blocks()

## TSiteType
Defines the type and parameters for a mission site.
- **Attributes:** pid, name, pedia, marker, size, map_blocks, deployment

## TUfo
Represents a UFO on the world map, with movement and combat logic.
- **Attributes:** ufo_id, position, ufo_type, ufo_script, script_step, speed, speed_max, health, game
- **Methods:** advance_script(), move_to(), set_position(), get_position(), distance_to(), take_damage(), is_destroyed(), is_crashed()

## TUfoScript
Defines a scripted trajectory and behavior sequence for UFOs.
- **Attributes:** pid, name, description, steps
- **Methods:** get_step(), total_steps(), process_current_step()

## TUfoType
Defines the specifications and capabilities of a specific UFO class.
- **Attributes:** pid, name, pedia, vessel, marker, size, health, speed, shield, shield_regen, damage, rate, range, accuracy, fire_sound, radar_range, radar_power, radar_cover, radar_cover_change, is_hunter, hunt_bravery, bombard_power, score_complete, score_destroy, score_avoid, score_damage, score_turn, map_block, map_width, map_height, force_terrain, deployments

---

- All classes follow project documentation and testing standards.
- See test/ subfolder for unit tests covering all public methods and attributes.
- For API details, see wiki/API.yml.

