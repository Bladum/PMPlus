"""
XCOM Unit Module: side.py

Represents a faction or side in the game (e.g., player, alien, civilian).

Classes:
    TSide: Identifies unit allegiance and determines combat relationships.

Last updated: 2025-06-14
"""

class TSide:
    """
    Represents a faction or side in the game (e.g., player, alien, civilian).
    Used to define unit ownership, allegiance, and combat relationships.
    """

    XCOM = 0
    ALIEN = 1
    CIVILIAN = 2
    ALLIED = 3

    pass
