"""
TDiplomacy: Manages diplomacy between XCOM and other factions from the faction's perspective.
Last update: 2025-06-12

Diplomacy System:
- Manages relations between the player (XCOM) and each faction.
- Each relation can be: ALLY, NEUTRAL, or WAR.
- Provides methods to get, set, and list diplomatic states.
- Easily extensible for future features (modifiers, events, history).
"""

from enum import Enum
from typing import Dict, List, Optional

class DiplomacyState(Enum):
    """
    Enum representing possible diplomatic states between XCOM and a faction.
    """
    ALLY = "ally"
    NEUTRAL = "neutral"
    WAR = "war"

class TDiplomacy:
    '''
    TDiplomacy manages diplomacy between XCOM (player) and other factions.

    Attributes:
        relations (Dict[str, DiplomacyState]):
            Mapping from faction ID (str) to current diplomatic state.
        history (Dict[str, List[DiplomacyState]]):
            (Optional) History of state changes for each faction.
    '''
    def __init__(self, factions: List[object]):
        '''
        Initialize diplomacy with all factions set to NEUTRAL by default.

        Args:
            factions (List[object]): List of faction objects (must have 'pid' attribute).
        '''
        self.relations: Dict[str, DiplomacyState] = {f.pid: DiplomacyState.NEUTRAL for f in factions}
        self.history: Dict[str, List[DiplomacyState]] = {f.pid: [DiplomacyState.NEUTRAL] for f in factions}

    def get_state(self, faction_id: str) -> DiplomacyState:
        '''
        Get the current diplomatic state with a faction.

        Args:
            faction_id (str): The ID of the faction.
        Returns:
            DiplomacyState: The current diplomatic state (ALLY, NEUTRAL, or WAR).
        '''
        return self.relations.get(faction_id, DiplomacyState.NEUTRAL)

    def set_state(self, faction_id: str, state: DiplomacyState) -> None:
        '''
        Set the diplomatic state with a faction. Records the change in history.

        Args:
            faction_id (str): The ID of the faction.
            state (DiplomacyState): The new diplomatic state.
        '''
        self.relations[faction_id] = state
        if faction_id not in self.history:
            self.history[faction_id] = []
        self.history[faction_id].append(state)

    def set_all(self, state: DiplomacyState) -> None:
        '''
        Set the diplomatic state for all factions at once.

        Args:
            state (DiplomacyState): The new diplomatic state to set for all factions.
        '''
        for faction_id in self.relations.keys():
            self.set_state(faction_id, state)

    def all_relations(self) -> Dict[str, DiplomacyState]:
        '''
        Get a copy of all current diplomatic relations.

        Returns:
            Dict[str, DiplomacyState]: Mapping of faction IDs to their current state.
        '''
        return self.relations.copy()

    def get_history(self, faction_id: str) -> List[DiplomacyState]:
        '''
        Get the history of diplomatic states for a faction.

        Args:
            faction_id (str): The ID of the faction.
        Returns:
            List[DiplomacyState]: List of states in chronological order.
        '''
        return self.history.get(faction_id, [DiplomacyState.NEUTRAL])

    def is_ally(self, faction_id: str) -> bool:
        '''
        Check if the faction is currently an ally.
        '''
        return self.get_state(faction_id) == DiplomacyState.ALLY

    def is_at_war(self, faction_id: str) -> bool:
        '''
        Check if the faction is currently at war.
        '''
        return self.get_state(faction_id) == DiplomacyState.WAR

    def is_neutral(self, faction_id: str) -> bool:
        '''
        Check if the faction is currently neutral.
        '''
        return self.get_state(faction_id) == DiplomacyState.NEUTRAL

# Example usage:
# from engine.lore.faction import TFaction
# factions = [TFaction('aliens', {...}), TFaction('council', {...})]
# diplomacy = TDiplomacy(factions)
# diplomacy.set_state('aliens', DiplomacyState.WAR)
# print(diplomacy.get_state('aliens'))  # DiplomacyState.WAR
# print(diplomacy.is_ally('council'))  # False