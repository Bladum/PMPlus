"""
TFaction: Faction definition for the game.
Purpose: Represents a faction, its properties, and its relationship to XCOM.
Last update: 2025-06-10
"""

class TFaction:
    """
    TFaction represents a faction in the game, which can own missions and locations.
    Faction may be ally or enemy of XCOM.

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