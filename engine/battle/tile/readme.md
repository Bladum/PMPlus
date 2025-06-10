# Tile Folder

This folder contains modules for handling individual tile components in the battle system.

- **battle_floor.py**: `TBattleFloor` represents a walkable floor tile with movement and sight properties.
- **battle_object.py**: `TBattleObject` represents objects on tiles, which can be picked up, destroyed, or emit light.
- **battle_roof.py**: `TBattleRoof` represents a roof layer on a tile.
- **battle_tile.py**: `TBattleTile` is the main class for a single battle map tile, containing floor, wall, roof, objects, and unit info.
- **battle_wall.py**: `TBattleWall` represents a wall, blocking movement and sight, with armor and destruction logic.
- **tileset_manager.py**: `TTilesetManager` loads and manages all tile images from tilesets and individual images.

