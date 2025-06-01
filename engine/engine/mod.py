"""
Module Overview: mod.py
-----------------------
This module provides core enumeration types and the main mod management class that serves
as a central repository for all game data loaded from mod files and directories.

Class Relationships:
- TItemCategory: Used by TUnitInventory for slot validation and by TMod for UI elements
- TItemRarity: Used by TItemType to determine item properties and availability
- TUnitCategory: Used by TMod and TGame for unit filtering and organization
- TMod: Central data manager that loads, stores, and provides access to all game entities
  * Interfaces with TModLoader to load data from files
  * Accessed by TGame to provide data to the game systems
  * Contains collections of all game object types for global access
"""

from pathlib import Path
from enum import Enum
from typing import List, Dict, Any, Tuple

from PIL.Image import Image
from pytmx import TiledTileset

from base.facility_type import TFacilityType
from battle.map.battle_script import TBattleScript
from battle.map.deployment import TDeployment
from battle.mission.objective import TBattleObjective
from battle.support.battle_effect import TBattleEffect
from battle.support.damage_model import TDamageModel
from battle.terrain.map_block import TMapBlock
from battle.terrain.terrain import TTerrain
from craft.craft_type import TCraftType
from economy.manufacture_entry import TManufactureEntry
from economy.purchase_entry import TPurchaseEntry
from economy.research_entry import TResearchEntry
from globe.biome import TBiome
from globe.country import TCountry
from globe.region import TRegion
from globe.world import TWorld
from item.item_type import TItemType
from item.item_mode import TWeaponMode
from location.city import TCity
from location.site import TSite
from location.site_type import TSiteType
from location.ufo_script import TUfoScript
from location.ufo_type import TUfoType
from lore.campaign import TCampaign
from lore.event import TEvent
from lore.faction import TFaction
from lore.mission import TMission
from pedia.pedia_entry import TPediaEntry
from traits.trait import TTrait
from unit.race import TRace
from unit.unit_type import TUnitType


class TItemCategory(Enum):
    """
    Enumeration for different types of equipment items.

    Used for categorizing items and determining valid equipment slots.
    """
    ARMOUR = "armour"
    WEAPON = "weapon"
    EQUIPMENT = "equipment"
    OTHER = "other"


class TItemRarity(Enum):
    """
    Enumeration for item rarity levels affecting gameplay balance.

    Determines item availability, power level, and visual presentation.
    """
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


class TUnitCategory(Enum):
    """
    Enumeration for different unit types in the game.

    Used for filtering, organization, and applying category-specific logic.
    """
    SOLDIER = "soldier"
    TANK = "tank"
    DOG = "dog"
    ALIEN = "alien"


class TMod:
    """
    Represents a mod in game, it is a list of files and folders
    It is used to load data from files and folders
    It is used to manage all data in game
    It is used to manage all events in game
    """
    def __init__(self, mod_data, mod_path):
        self.mod_data = mod_data
        self.mod_path = Path(mod_path)

        if self.mod_path:
            self.maps_path = self.mod_path / 'maps'
            self.rules_path = self.mod_path / 'rules'
            self.tiles_path = self.mod_path / 'tiles'
        else:
            self.maps_path = None
            self.rules_path = None
            self.tiles_path = None

        # here save all graphics tiles

        from battle.tile.tileset_manager import TTilesetManager
        self.tileset_manager: TTilesetManager = None

        # base
        self.facilities: dict[str, TFacilityType] = {}

        # units
        self.races : dict[str, TRace] = {}
        self.units: dict[str, TUnitType] = {}
        self.traits : dict[str, TTrait] = {}

        # economy
        self.researches : dict[str, TResearchEntry] = {}
        self.purchases : dict[str, TPurchaseEntry] = {}
        self.manufacturing : dict[str, TManufactureEntry] = {}

        # battle
        self.deployments: dict[str, TDeployment] = {}
        self.effects: dict[str, TBattleEffect] = {}
        self.map_blocks : dict[str, TMapBlock] = {}
        self.map_scripts: dict[str, TBattleScript] = {}
        self.objectives: dict[str, TBattleObjective] = {}
        # self.tilesets : dict[str, TiledTileset] = {} TODO fix
        self.terrains : dict[str, TTerrain] = {}

        # items
        self.items: dict[str, TItemType] = {}
        self.weapon_modes : dict[str, TWeaponMode] = {}
        # self.damage_types: dict[str, TDamageType] = {} TODO fix
        self.damage_models: dict[str, TDamageModel] = {}
        # self.resistances : dict[str, TArmourResistance] = {} TODO

        # globe
        self.worlds : dict[str, TWorld] = {}
        self.biomes : dict[str, TBiome] = {}
        self.countries : dict[str, TCountry] = {}
        self.regions : dict[str, TRegion] = {}
        self.cities : dict[str, TCity] = {}

        # lore
        self.factions : dict[str, TFaction] = {}
        self.campaigns: dict[str, TCampaign] = {}
        self.events : dict[str, TEvent] = {}
        self.sites: dict[str, TSiteType] = {}
        self.mission : dict[str, TMission] = {}

        # crafts
        self.ufo_types : dict[str, TUfoType] = {}
        self.craft_types: dict[str, TCraftType] = {}
        self.ufo_scripts : dict[str, TUfoScript] = {}
        self.starting_base: dict = {}

        # pedia
        self.pedia_entries : dict[str, TPediaEntry] = {}

    def load_objects_from_data(self):
        """
        For each section in mod_data, create objects and store them in the appropriate dict.
        """

        # BASE
        mod_data = self.mod_data

        datas = mod_data.get('facilities', {})
        for pid, dat in datas.items():
            obj = TFacilityType(pid, dat)
            self.facilities[pid] = obj
        print(f"Loaded {len(self.facilities)} facilities")

        datas = mod_data.get('start_bases', {})
        for pid, dat in datas.items():
            self.starting_base[pid] = dat
        print(f"Loaded {len(self.starting_base)} starting bases")

        # ECONOMY

        datas = mod_data.get('manufacturing', {})
        for pid, dat in datas.items():
            obj = TManufactureEntry(pid, dat)
            self.manufacturing[pid] = obj
        print(f"Loaded {len(self.manufacturing)} manufacturing entries")

        datas = mod_data.get('purchasing', {})
        for pid, dat in datas.items():
            obj = TPurchaseEntry(pid, dat)
            self.purchases[pid] = obj
        print(f"Loaded {len(self.purchases)} purchase entries")

        datas = mod_data.get('research', {})
        for pid, dat in datas.items():
            obj = TResearchEntry(pid, dat)
            self.researches[pid] = obj
        print(f"Loaded {len(self.researches)} research entries")

        # CRAFT

        datas = mod_data.get('crafts', {})
        for pid, dat in datas.items():
            obj = TCraftType(pid, dat)
            self.craft_types[pid] = obj
        print(f"Loaded {len(self.craft_types)} craft types")

        datas = mod_data.get('ufo_script', {})
        for pid, dat in datas.items():
            obj = TUfoScript(pid, dat)
            self.ufo_scripts[pid] = obj
        print(f"Loaded {len(self.ufo_scripts)} UFO scripts")

        datas = mod_data.get('ufos', {})
        for pid, dat in datas.items():
            obj = TUfoType(pid, dat)
            self.ufo_types[pid] = obj
        print(f"Loaded {len(self.ufo_types)} UFO types")

        # GLOBE

        datas = mod_data.get('biomes', {})
        for pid, dat in datas.items():
            obj = TBiome(pid, dat)
            self.biomes[pid] = obj
        print(f"Loaded {len(self.biomes)} biomes")

        datas = mod_data.get('cities', {})
        for pid, dat in datas.items():
            obj = TCity(pid, dat)
            self.cities[pid] = obj
        print(f"Loaded {len(self.cities)} cities")

        datas = mod_data.get('countries', {})
        for pid, dat in datas.items():
            obj = TCountry(pid, dat)
            self.countries[pid] = obj
        print(f"Loaded {len(self.countries)} countries")

        datas = mod_data.get('regions', {})
        for pid, dat in datas.items():
            obj = TRegion(pid, dat)
            self.regions[pid] = obj
        print(f"Loaded {len(self.regions)} regions")

        datas = mod_data.get('worlds', {})
        for pid, dat in datas.items():
            obj = TWorld(pid, dat)
            self.worlds[pid] = obj
        print(f"Loaded {len(self.worlds)} worlds")

        # BATTLE

        datas = mod_data.get('effects', {})
        for pid, dat in datas.items():
            obj = TBattleEffect(pid, dat)
            self.effects[pid] = obj
        print(f"Loaded {len(self.effects)} battle effects")

        datas = mod_data.get('deployments', {})
        for pid, dat in datas.items():
            obj = TDeployment(pid, dat)
            self.deployments[pid] = obj
        print(f"Loaded {len(self.deployments)} battle deployments")

        datas = mod_data.get('terrains', {})
        for pid, dat in datas.items():
            obj = TTerrain(pid, dat)
            self.terrains[pid] = obj
        print(f"Loaded {len(self.terrains)} battle terrains")

        datas = mod_data.get('map_scripts', {})
        for pid, dat in datas.items():
            obj = TBattleScript(pid, dat)
            self.map_scripts[pid] = obj
        print(f"Loaded {len(self.map_scripts)} battle scripts")

        datas = mod_data.get('pedia', {})
        for pid, dat in datas.items():
            obj = TPediaEntry(pid, dat)
            self.pedia_entries[pid] = obj
        print(f"Loaded {len(self.pedia_entries)} pedia entries")

        datas = mod_data.get('objectives', {})
        for pid, dat in datas.items():
            obj = TBattleObjective(pid, dat)
            self.objectives[pid] = obj
        print(f"Loaded {len(self.objectives)} battle objectives")

        # traits

        datas = mod_data.get('effects', {})
        for pid, dat in datas.items():
            dat['category'] = TTrait.TRAIT_EFFECT
            obj = TTrait(pid, dat)
            self.traits[pid] = obj

        datas = mod_data.get('origins', {})
        for pid, dat in datas.items():
            dat['category'] = TTrait.TRAIT_ORIGIN
            obj = TTrait(pid, dat)
            self.traits[pid] = obj

        datas = mod_data.get('ranks', {})
        for pid, dat in datas.items():
            dat['category'] = TTrait.TRAIT_ENEMY_RANK
            obj = TTrait(pid, dat)
            self.traits[pid] = obj

        datas = mod_data.get('medals', {})
        for pid, dat in datas.items():
            dat['category'] = TTrait.TRAIT_MEDAL
            obj = TTrait(pid, dat)
            self.traits[pid] = obj

        datas = mod_data.get('promotions', {})
        for pid, dat in datas.items():
            dat['category'] = TTrait.TRAIT_PROMOTION
            obj = TTrait(pid, dat)
            self.traits[pid] = obj

        datas = mod_data.get('transformations', {})
        for pid, dat in datas.items():
            dat['category'] = TTrait.TRAIT_TRANSFORMATION
            obj = TTrait(pid, dat)
            self.traits[pid] = obj

        print(f"Loaded {len(self.traits)} traits")

        # UNITS

        datas = mod_data.get('units', {})
        for pid, dat in datas.items():
            obj = TUnitType(pid, dat)
            self.units[pid] = obj
        print(f"Loaded {len(self.units)} units")

        datas = mod_data.get('races', {})
        for pid, dat in datas.items():
            obj = TRace(pid, dat)
            self.races[pid] = obj
        print(f"Loaded {len(self.races)} races")

        # LORE

        datas = mod_data.get('sites', {})
        for pid, dat in datas.items():
            obj = TSiteType(pid, dat)
            self.sites[pid] = obj
        print(f"Loaded {len(self.sites)} sites")

        datas = mod_data.get('factions', {})
        for pid, dat in datas.items():
            obj = TFaction(pid, dat)
            self.factions[pid] = obj
        print(f"Loaded {len(self.factions)} factions")

        datas = mod_data.get('campaigns', {})
        for pid, dat in datas.items():
            obj = TCampaign(pid, dat)
            self.campaigns[pid] = obj
        print(f"Loaded {len(self.campaigns)} campaigns")

        datas = mod_data.get('events', {})
        for pid, dat in datas.items():
            obj = TEvent(pid, dat)
            self.events[pid] = obj
        print(f"Loaded {len(self.events)} events")

        # ITEM MODES

        datas = mod_data.get('item_modes', {})
        for pid, dat in datas.items():
            obj = TWeaponMode(pid, dat)
            self.weapon_modes[pid] = obj
        print(f"Loaded {len(self.weapon_modes)} item modes")

        datas = mod_data.get('craft_items', {})
        for pid, dat in datas.items():
            dat['category'] = TItemType.ITEM_CRAFT_ITEM
            obj = TItemType(pid, dat)
            self.items[pid] = obj

        datas = mod_data.get('unit_armours', {})
        for pid, dat in datas.items():
            dat['category'] = TItemType.ITEM_UNIT_ARMOUR
            obj = TItemType(pid, dat)
            self.items[pid] = obj

        datas = mod_data.get('unit_items', {})
        for pid, dat in datas.items():
            dat['category'] = TItemType.ITEM_UNIT_ITEM
            obj = TItemType(pid, dat)
            self.items[pid] = obj
        print(f"Loaded {len(self.items)} items")

        # here iterate over the mod_data and create objects
        #

            # # battle

            # map_blocks = TMapBlock
            # tiles =
            # tilesets = TTiledTileset
            #
            # # globe
            # cities = TCity
            #
            #

            # # story
            # calendar = TCalendar
            #
            # # vars
            # item_types = 1
            # start_base = 1
            # battlemap_sizes = 1
            # terrain_resistance = TArmourResistance
            # armour_resistance = TArmourResistance
            # salaries = 1

    def load_all_terrain_map_blocks(self):
        """
        Loads all map blocks for all terrains in this mod.
        """
        for terrain in self.terrains.values():
            terrain.load_maps_and_blocks(self.maps_path / terrain.maps_folder)

    def render_all_map_blocks(self):
        """
        Render all map blocks to PNG for debugging/visualization.
        """
        for terrain in self.terrains.values():
            terrain.render_map_blocks()

    @staticmethod
    def get_equipment_slots() -> List[Dict[str, Any]]:
        """
        Get equipment slot configuration data.

        Returns:
            List of slot dictionaries containing position, type, and styling info

        Each slot dictionary contains:
        - name: Display name for the slot
        - type: ItemType enum value for slot validation
        - position: (x, y) grid coordinates for UI positioning
        - color_adjust: (r, g, b) color adjustment values for visual variety
        """
        return [
            {"name": "Armour", "type": TItemCategory.ARMOUR, "position": (20, 7), "color_adjust": (0, 0, 0.05)},  # Blue tint
            {"name": "Weapon", "type": TItemCategory.WEAPON, "position": (28, 7), "color_adjust": (0.05, 0, 0)},  # Red tint
            {"name": "Equipment 1", "type": TItemCategory.EQUIPMENT, "position": (21, 13), "color_adjust": (0, 0.05, 0)},  # Green tint
            {"name": "Equipment 2", "type": TItemCategory.EQUIPMENT, "position": (21, 18), "color_adjust": (0, 0.05, 0)},  # Green tint
            {"name": "Equipment 3", "type": TItemCategory.EQUIPMENT, "position": (27, 13), "color_adjust": (0, 0.05, 0)},  # Green tint
            {"name": "Equipment 4", "type": TItemCategory.EQUIPMENT, "position": (27, 18), "color_adjust": (0, 0.05, 0)},  # Green tint
        ]

    @staticmethod
    def get_unit_categories() -> List[Dict[str, str]]:
        """
        Get list of unit categories for filtering UI.

        Returns:
            List of dictionaries containing category names and icon paths

        Used by UI components to populate filter dropdowns and organize
        unit displays by type.
        """
        return [
            {"name": "All", "icon": "units/icon_a.png"},
            {"name": "Soldier", "icon": "units/icon_a.png"},
            {"name": "Tank", "icon": "units/icon_b.png"},
            {"name": "Dog", "icon": "units/icon_c.png"},
            {"name": "Alien", "icon": "units/icon_d.png"},
        ]

    @staticmethod
    def get_item_categories() -> List[Dict[str, str]]:
        """
        Get list of item categories for filtering UI.

        Returns:
            List of dictionaries containing category names and icon paths

        Used by UI components to populate filter dropdowns and organize
        item displays by type.
        """
        return [
            {"name": "All", "icon": "other/item2.png"},
            {"name": "Armour", "icon": "other/item2.png"},
            {"name": "Weapon", "icon": "other/item2.png"},
            {"name": "Equipment", "icon": "other/item.png"},
            {"name": "Other", "icon": "other/item.png"},
        ]

