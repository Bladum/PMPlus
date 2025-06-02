"""
TSide Class
===========

Purpose:
    Represents a faction or side in the game (e.g., player, alien, civilian).
    This class identifies which faction a unit belongs to during gameplay.

Interactions:
    - Used by TUnit to define unit ownership and allegiance
    - Determines combat relationships (friendly/enemy) between units
    - Affects AI behavior and targeting decisions
    - Used for victory/defeat condition evaluation
"""

class TSide:

    XCOM = 0
    ALIEN = 1
    CIVILIAN = 2
    ALLIED = 3

    pass

