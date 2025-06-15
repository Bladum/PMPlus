# Test Module

This folder contains test scripts and visual testbeds for the XCOM/AlienFall engine. These files are used for manual and automated testing of engine features, including tactical grid rendering, pathfinding, and animation effects.

## Files and Classes

- **blocks.py**: Defines `TileMapGame`, a tactical grid-based game testbed for XCOM mechanics.
- **main.py**: Sample entry point for initializing the game, loading mods, and rendering the world map (script, not a class).
- **test.py**: Duplicate tactical testbed for grid-based mechanics (also defines `TileMapGame`).
- **unit range.py**: Defines `Projectile` and `FloatingNumber`, visual test classes for projectile motion and floating text.

## Usage Notes
- These files are intended for development and debugging purposes.
- Some files are scripts and not meant to be imported as modules.
- See each file and class docstring for details on usage and features.

---

For more information on testing and automation, see `wiki/tests.md`.
