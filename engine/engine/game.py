from engine.globe.world import TWorld
from engine.lore.campaign import TCampaign
from engine.lore.calendar import TCalendar
from engine.economy.research_tree import TResearchTree
from engine.economy.transfer import TTransfer
from engine.lore.faction import TFaction
from engine.engine.mod import TMod

class TGame:
    """
    Main game class, holds all data
    It is a singleton
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(TGame, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # World map: tiles, countries, regions, biomes, locations
        self.worldmap = None  # type: TWorld
        # Current campaigns, missions, and campaign generator
        self.campaigns = []  # type: list[TCampaign]
        # Calendar for date, turn, and event triggers
        self.calendar = None  # type: TCalendar
        # XCOM budget, funding, and scoring
        self.budget = 0
        self.funding = 0
        self.scoring = 0
        # Global research tree
        self.research_tree = None  # type: TResearchTree
        # Global transfer list
        self.transfer_list = []  # type: list[TTransfer]
        # Factions and diplomacy/relations
        self.factions = []  # type: list[TFaction]
        self.diplomacy = {}  # type: dict[str, int]
        # Loaded mod data (e.g., item stats)
        self.mod_data = None  # type: TMod
