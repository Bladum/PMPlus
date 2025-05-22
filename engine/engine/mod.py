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
from location.site import TSite
from location.ufo_script import TUfoScript
from location.ufo_type import TUfoType
from lore.campaign import TCampaign
from lore.event import TEvent
from lore.faction import TFaction
from lore.mission import TMission
from pedia.pedia_entry import TPediaEntry
from skill.skill import TSkill
from unit.race import TRace
from unit.unit_type import TUnitType



class TMod:
    """
    Represents a mod in game, it is a list of files and folders
    It is used to load data from files and folders
    It is used to manage all data in game
    It is used to manage all events in game
    """
    def __init__(self, mod_data):

        # Path setup
        import os
        self.mod_path = mod_data.get('mod_path') if isinstance(mod_data, dict) else None
        if self.mod_path:
            self.maps_path = os.path.join(self.mod_path, 'maps')
            self.rules_path = os.path.join(self.mod_path, 'rules')
            self.tiles_path = os.path.join(self.mod_path, 'tiles')
        else:
            self.maps_path = None
            self.rules_path = None
            self.tiles_path = None

        # base
        self.facilities: dict[str, TFacilityType] = {}

        # units
        self.races : dict[str, TRace] = {}
        self.units: dict[str, TUnitType] = {}
        self.skills : dict[str, TSkill] = {}

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

        # lore
        self.factions : dict[str, TFaction] = {}
        self.campaigns: dict[str, TCampaign] = {}
        self.events : dict[str, TEvent] = {}
        self.sites: dict[str, TSite] = {}
        self.mission : dict[str, TMission] = {}

        # crafts
        self.ufo_types : dict[str, TUfoType] = {}
        self.craft_types: dict[str, TCraftType] = {}
        self.ufo_scripts : dict[str, TUfoScript] = {}

        # pedia
        self.pedia_entries : dict[str, TPediaEntry] = {}



