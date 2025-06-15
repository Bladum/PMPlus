"""
TBattleActions: Handles all possible unit actions during battle (movement, crouch, use item, cover, throw, overwatch, suppression, rest).

Encapsulates the logic for executing and managing unit actions on the battle map, including action validation, execution, and interaction with the game state.

Classes:
    TBattleActions: Main class for unit action management in battle.

Last standardized: 2025-06-14
"""

class TBattleActions:
    """
    Manages all unit actions that can be performed during a battle.
    Includes movement, stealth/crouch, item usage, taking cover, throwing items, overwatch, suppression, and resting.

    Actions include:
        - move: Move a unit to a new tile, checking for pathfinding, AP cost, and triggering reactions.
        - crouch: Toggle crouch/stealth state, affecting visibility and hit chance.
        - use item: Use an item (e.g., fire a weapon), applying effects and consuming resources.
        - cover: Take cover behind an object or wall, modifying defense stats.
        - throw item: Throw a grenade or other throwable, handling trajectory and effects.
        - overwatch: Set the unit to reactively fire during enemy movement.
        - suppression: Suppress an area or enemy, reducing their effectiveness.
        - rest: Regain stamina or AP, possibly at the cost of skipping a turn.
    """
    pass