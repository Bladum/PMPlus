# Battle Action Module

**File:** `battle_action.py`

## Description
Implements the `TBattleActions` class, which handles all unit actions during battle, such as moving, crouching, using items, taking cover, throwing, overwatch, suppression, and resting.

## Main Class
- `TBattleActions`: Provides methods for executing and managing unit actions on the battle map.

## Usage Notes
- Intended to be used by the battle engine to process player and AI actions.
- Extend this class to implement specific action logic.

---
Keep this README in sync with code docstrings and `API.yml`.
# Battle Effect Module

**File:** `battle_effect.py`

## Description
Implements the `TBattleEffect` class, representing special effects (e.g., smoke, fire, panic, sanity) that can be applied to battle map tiles or units.

## Main Class
- `TBattleEffect`: Stores effect metadata and properties, such as name, description, and icon.

## Usage Notes
- Effects are initialized with a unique `pid` and a data dictionary.
- Extend this class to implement effect logic and requirements.

---
Keep this README in sync with code docstrings and `API.yml`.
# Battle Fog of War Module

**File:** `battle_fow.py`

## Description
Implements the `TBattleFOW` class, which manages fog of war (visibility) for units and tiles on the battle map for all sides.

## Main Class
- `TBattleFOW`: Provides methods for updating and querying visibility states.

## Usage Notes
- Used by the battle engine to determine what each side can see.
- Extend this class to implement specific FOW logic.

---
Keep this README in sync with code docstrings and `API.yml`.
# Battle Loot Module

**File:** `battle_loot.py`

## Description
Implements the `BattleLoot` class, which generates post-battle reports including loot, score, captures, experience, sanity, ammo, and medals.

## Main Class
- `BattleLoot`: Provides static methods to summarize battle outcomes and rewards.

## Usage Notes
- Use `BattleLoot.generate(battle)` to obtain a summary report as a dictionary.
- Designed for integration with the battle engine's end-of-battle processing.

---
Keep this README in sync with code docstrings and `API.yml`.
# Battle Line of Sight Module

**File:** `battle_los.py`

## Description
Implements the `BattleLOS` class, which provides static line-of-sight (LOS) calculations for battle map tiles using Bresenham's algorithm.

## Main Class
- `BattleLOS`: Offers static methods to check LOS between two points, considering walls, smoke, fire, and tile properties.

## Usage Notes
- Use `BattleLOS.has_los(battle, start, end, max_range)` to check visibility.
- Designed for use in AI, targeting, and FOW systems.

---
Keep this README in sync with code docstrings and `API.yml`.
# Battle Pathfinder Module

**File:** `battle_pathfinder.py`

## Description
Implements the `BattlePathfinder` class, which provides static pathfinding for battle map tiles using the A* algorithm and tile walkability.

## Main Class
- `BattlePathfinder`: Offers static methods to find paths for units of various sizes.

## Usage Notes
- Use `BattlePathfinder.find_path(battle, start, end, unit_size)` to get a path as a list of coordinates.
- Designed for use in AI and movement systems.

---
Keep this README in sync with code docstrings and `API.yml`.
# Damage Model Module

**File:** `damage_model.py`

## Description
Implements the `TDamageModel` class, which handles damage calculation for weapons, explosions, and other sources in battle.

## Main Class
- `TDamageModel`: Provides methods for calculating damage, armor penetration, critical hits, and distributing damage to body parts.

## Usage Notes
- Extend this class to implement specific damage logic.
- Used by the battle engine for all damage-related calculations.

---
Keep this README in sync with code docstrings and `API.yml`.
# Reaction Fire Module

**File:** `reactions.py`

## Description
Implements the `TReactionFire` class, which handles reaction fire mechanics in battle.

## Main Class
- `TReactionFire`: Provides methods for managing and resolving reaction fire events.

## Usage Notes
- Extend this class to implement specific reaction fire logic.
- Used by the battle engine to process reaction fire triggers and outcomes.

---
Keep this README in sync with code docstrings and `API.yml`.

