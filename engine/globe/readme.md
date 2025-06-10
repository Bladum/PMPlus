# Globe Module

This module contains classes representing the world map, its structure, and related entities in the game. Each class is responsible for a specific aspect of the globe, such as biomes, countries, regions, locations, and radar detection.

## Class Summaries

### TBiome
Represents a biome type assigned to each tile on the world map (e.g., forest, desert, ocean). Used to generate battles with specific terrain types.
- **Attributes:** pid, name, description, image, type, terrains
- **Methods:** get_random_terrain()

### TCountry
Represents a country on the world map, manages funding and relations with XCOM. Owns tiles and can join or leave XCOM.
- **Attributes:** pid, name, description, color, funding, funding_cap, service_provided, service_forbidden, owned_tiles, initial_relation, relation, active
- **Methods:** monthly_update(), add_tile(), remove_tile(), calculate_owned_tiles()

### TDiplomacy
Manages diplomacy between XCOM and other factions from the faction's perspective. (Currently a placeholder.)
- **Attributes:** None
- **Methods:** None

### TFunding
Manages XCOM's funding based on country scores and generates monthly reports.
- **Attributes:** countries, month_scores
- **Methods:** add_tile_score(), monthly_report()

### TLocation
Represents a single location on the world map (base, city, crash site, etc.). Handles radar detection and visibility.
- **Attributes:** pid, name, description, position, initial_cover, cover, cover_change, visible
- **Methods:** update_visibility(), replenish_cover(), get_position(), distance_to()

### TGlobalRadar
Manages radar detection of UFOs and locations on the world map.
- **Attributes:** world
- **Methods:** scan()

### TRegion
Represents a region on the world map, used for mission control and analytics.
- **Attributes:** pid, name, is_land, tiles, neighbors, description, color, mission_weight, base_cost, service_provided, service_forbidden
- **Methods:** calculate_region_tiles()

### TWorld
Represents the world map as a 2D array of tiles. Handles loading from TMX, rendering, and managing cities, countries, and regions.
- **Attributes:** pid, name, description, size, map_file, countries, bases, factions, regions, tech_start, transfer_list, tiles, cities, factions, diplomacy
- **Methods:** get_day_night_map(), render_tile_map_to_text(), render_world_layers_to_png(), from_tmx()

### TWorldPoint
Represents a position on the world map (tile coordinates). Provides utility methods for position handling.
- **Attributes:** x, y
- **Methods:** from_tuple(), to_tuple(), distance_to(), manhattan_distance(), __eq__(), __hash__(), __repr__(), __add__(), __sub__(), scale(), is_within_bounds(), midpoint(), get_adjacent_points(), get_adjacent_points_with_diagonals(), round_to_grid()

### TWorldTile
Represents a single tile on the world map. Assigned to a region, country, and biome. May have locations.
- **Attributes:** x, y, region_id, country_id, biome_id, locations
- **Methods:** None

