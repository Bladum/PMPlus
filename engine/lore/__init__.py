"""
__init__.py

Lore module package initialization.

Imports all classes and managers for handling the game's lore, including campaigns, events, factions, missions, organizations, and quests. Import this package to access all lore-related classes for campaign and event management, quest tracking, and narrative progression.

Last standardized: 2025-06-14
"""

from .calendar import TCalendar
from .campaign import TCampaign
from .campaign_step import TCampaignStep
from .event import TEvent
from .event_engine import TEventEngine
from .faction import TFaction
from .mission import TMission
from .organization import TOrganization
from .quest import TQuest
from .quest_engine import TQuestEngine
from .quest_manager import QuestManager

__all__ = [
    "TCalendar",
    "TCampaign",
    "TCampaignStep",
    "TEvent",
    "TEventEngine",
    "TFaction",
    "TMission",
    "TOrganization",
    "TQuest",
    "TQuestEngine",
    "QuestManager",
]