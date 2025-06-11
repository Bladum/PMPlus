# Tile Folder

This folder contains modules for handling individual tile components in the battle system.

## TBattleFloor
Represents a walkable floor tile with movement, sight, and accuracy properties.
- **Attributes:** move_cost, sight_cost, accuracy_cost, armor, sound, is_light_source, destroyed_floor_id
- **Methods:** on_destroy()

## TBattleObject
Represents an object on a tile, which can be picked up, destroyed, or emit light.
- **Attributes:** is_light_source, armor, destroyed_object_id
- **Methods:** on_destroy()

## TBattleRoof
Represents a roof layer on a tile. Placeholder for future gameplay or rendering attributes.
- **Attributes:** (extend as needed)
- **Methods:** (extend as needed)

## TBattleWall
Represents a wall, blocking movement and sight, with armor and destruction logic.
- **Attributes:** block_sight, block_fire, sight_mod, fire_mod, armor, material, destroyed_wall_id, is_light_source, can_explode, explosion_power
- **Methods:** on_destroy()

## TBattleTile
Main class for a single battle map tile, containing floor, wall, roof, objects, and unit info. Provides methods for copying, updating, and applying damage to tiles.
- **Attributes:** floor, wall, roof, objects, unit, smoke, fire, gas, light_level, fog_of_war, floor_id, wall_id, roof_id, passable, blocks_fire, blocks_sight, blocks_light, metadata
- **Methods:** copy(), update_properties(), has_floor(), has_wall(), has_roof(), is_walkable(), get_move_cost(), get_sight_cost(), get_accuracy_mod(), get_armor(), is_light_source(), destroy_floor(), destroy_wall(), destroy_object(), apply_damage(), apply_point_damage(), apply_area_damage(), calculate_resistance(), distribute_damage(), gid_to_tileset_name(), from_gids()

## TTilesetManager
Loads and manages all tile images from tilesets and individual images.
- **Attributes:** folder_path, all_tiles
- **Methods:** load_tileset(), load_all_tilesets_from_folder(), load_individual_images_from_folder(), load_all_images(), get_tile(), save_tiles_to_folders(), print_tileset_info()
