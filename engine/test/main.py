"""
Test entry point for XCOM/AlienFall engine systems.

Provides a sample main script for initializing the game, loading mods, and rendering the world map using PySide6.

Last standardized: 2025-06-14
"""

from pathlib import Path
import sys

from battle.map.battle_generator import TBattleGenerator
from engine.engine.modloader import TModLoader

from battle.tile.tileset_manager import TTilesetManager

# Add PySide6 import for GUI
from PySide6.QtWidgets import QApplication

# Example usage:
if __name__ == "__main__":

    # Create Qt application
    app = QApplication(sys.argv)

    mod_name = 'xcom'

    # CREATE GAME

    from engine.engine.game import TGame
    game = TGame()

    current_dir = Path(__file__).resolve().parent
    root_dir = current_dir.parent.parent
    mod_path = root_dir / 'mods' / mod_name

    loader = TModLoader(mod_name, mod_path)
    loader.load_all_yaml_files()  # Changed to load YAML files

    # LOAD MOD DATA FROM YAML FILES

    from engine.engine.mod import TMod
    game.mod = TMod(loader.yaml_data, mod_path)  # Changed to use yaml_data
    game.mod.load_objects_from_data()

    # LOAD ALL GRAPHICS TILESETS

    game.mod.tileset_manager = TTilesetManager()
    game.mod.tileset_manager.load_all_images(game.mod.tiles_path, game.mod.gfx_path)

    # # LOAD ALL MAP BLOCKS

    # game.mod.load_all_terrain_map_blocks()
    # game.mod.render_all_map_blocks()

    # LOAD WORLD FROM TMX FILE

    # from engine.globe.world import TWorld
    # world_tmx_path = mod_path / 'worlds' / 'earth.tmx'
    # if world_tmx_path.exists():
    #     game.mod.world = TWorld.from_tmx(world_tmx_path)
    #     print(f"Loaded world from {world_tmx_path}")
    # else:
    #     print(f"World TMX file not found: {world_tmx_path}")


    # RENDER THE WORLD MAP TO TEXT AND PNG

    # game.mod.world.render_tile_map_to_text(mod_path / 'export' / 'world_map.txt')
    # game.mod.world.render_world_layers_to_png(mod_path / 'export' / 'world_map.png')

    # LOAD INITIAL BASE DATA

    game.mod.load_initial_base_data()

    # CREATE BASE GUI
    from gui.gui_base import TGuiBase
    from gui.base.gui_barracks import TGuiBarracks
    from gui.base.gui_hangar import TGuiHangar
    from gui.base.gui_lab import TGuiLab
    from gui.base.gui_workshop import TGuiWorkshop
    from gui.base.gui_storage import TGuiStorage
    from gui.base.gui_base_info import TGuiBaseInfo

    # Create the main Base GUI widget
    base_gui = TGuiBase()

    # Register all base screens
    base_gui.register_screen("barracks", TGuiBarracks(base_gui))
    base_gui.register_screen("hangar", TGuiHangar())
    base_gui.register_screen("research", TGuiLab())
    base_gui.register_screen("workshop", TGuiWorkshop())
    base_gui.register_screen("storage", TGuiStorage())
    base_gui.register_screen("base_info", TGuiBaseInfo())

    # Set initial screen to display
    base_gui.set_initial_screen("base_info")

    # Display the GUI
    base_gui.show()
    base_gui.setMinimumSize(640, 400)
    base_gui.setWindowTitle("XCOM Base Management")

    # Run the application event loop
    sys.exit(app.exec())

    # CREATE A BATTLE MAP GENERATOR

    # ter = game.mod.terrains.get('farmland')
    # script = game.mod.map_scripts.get('polar')
    #
    # for x in range(9):
    #     gg = TBattleGenerator(ter, script, blocks_x=6, blocks_y=6)
    #     gg.generate()
    #     gg.render_to_png(f'battle_map_{x}.png')
