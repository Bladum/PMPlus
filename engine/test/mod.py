from pathlib import Path

from engine.engine.modloader import TModLoader

from battle.tile.tileset_manager import TTilesetManager

# Example usage:
if __name__ == "__main__":

    mod_name = 'xcom'

    from engine.engine.game import TGame
    game = TGame()

    current_dir = Path(__file__).resolve().parent
    root_dir = current_dir.parent.parent
    mod_path = root_dir / 'mods' / mod_name

    loader = TModLoader(mod_name, mod_path)
    loader.load_all_yaml_files()  # Changed to load YAML files

    # load mod data from yaml files
    from engine.engine.mod import TMod
    game.mod = TMod(loader.yaml_data, mod_path)  # Changed to use yaml_data
    game.mod.load_objects_from_data()

    # load all graphics tilesets
    game.mod.tileset_manager = TTilesetManager(game.mod.tiles_path)
    game.mod.tileset_manager.load_all_tilesets_from_folder()

    # # load all map blocks
    # game.mod.load_all_terrain_map_blocks()
    # game.mod.render_all_map_blocks()

    # Load world from TMX file
    from engine.globe.world import TWorld
    world_tmx_path = mod_path / 'worlds' / 'earth.tmx'
    if world_tmx_path.exists():
        game.mod.world = TWorld.from_tmx(world_tmx_path)
        print(f"Loaded world from {world_tmx_path}")
    else:
        print(f"World TMX file not found: {world_tmx_path}")
    game.mod.world.render_tile_map_to_text(mod_path / 'export' / 'world_map.txt')
    game.mod.world.render_world_layers_to_png(mod_path / 'export' / 'world_map.png')


    # ter = game.mod.terrains.get('farmland')
    # script = game.mod.map_scripts.get('polar')
    #
    # for x in range(9):
    #     gg = TBattleGenerator(ter, script, blocks_x=6, blocks_y=6)
    #     gg.generate()
    #     gg.render_to_png(f'battle_map_{x}.png')

