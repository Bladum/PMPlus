"""
XCOM Lore Module: faction.py

Defines a faction in the game, with properties, relationships, and requirements.

Classes:
    TFaction: Faction definition for the game.

Last updated: 2025-06-14
"""

class TFaction:
    """
    Represents a faction in the game, which can own missions and locations. May be ally or enemy of XCOM.

    Attributes:
        pid (str): Faction identifier.
        name (str): Faction name.
        description (str): Faction description.
        id (int): Faction numeric ID.
        aggression (int): Aggression level.
        pedia (str): Encyclopedia entry.
        sprite (str): Faction icon or sprite.
        tech_start (list): Technologies required to start.
        tech_end (list): Technologies that end the faction's activity.
    """

    def __init__(self, pid, data : dict = {}):
        """
        Initialize a faction.

        Args:
            pid (str): Faction identifier.
            data (dict): Faction data and parameters.
        """
        # Required fields
        self.pid = pid

        self.name = data.get("name", "")
        self.description = data.get("description", "")
        self.id = data.get("id", 0)

        self.aggression = data.get("aggression", 0)
        self.pedia = data.get("pedia", '')
        self.sprite = data.get("sprite", '')

        self.tech_start = data.get("tech_start", [])
        self.tech_end = data.get("tech_end", [])