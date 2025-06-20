"""
XCOM Lore Module: campaign.py

Defines a campaign for a specific faction and region.

Classes:
    TCampaign: Campaign definition for a faction and region.

Last updated: 2025-06-14
"""

from engine.lore.mission import TMission


class TCampaign:
    """
    Represents a set of missions for a specific faction in a specific region.
    Created by the calendar and has a start date, end date, and list of missions, limited by research status.

    Attributes:
        pid (str): Campaign identifier.
        name (str): Campaign name.
        score (int): Points awarded for campaign completion.
        objective (int): Campaign objective type.
        faction (str): Faction name.
        tech_start (list): Technologies required to start.
        tech_end (list): Technologies that end the campaign.
        regions (dict): Region weights for campaign occurrence.
        missions (list): List of TMission objects.
    """

    OBJECTIVE_SCOUT = 0             # scout, find bases, crafts, cities
    OBJECTIVE_INFILTRATE = 1        # impact country
    OBJECTIVE_BASE = 2              # create alien base
    OBJECTIVE_TERROR = 3            # terror city
    OBJECTIVE_RETALIATION = 4       # attack xcom base
    OBJECTIVE_RESEARCH = 5          # improve technology
    OBJECTIVE_DESTRUCTION = 6       # destroy city
    OBJECTIVE_SUPPLY = 7            # supply existing base
    OBJECTIVE_HUNT = 8              # hunt xcom crafts

    def __init__(self, pid, data):
        """
        Initialize a campaign.

        Args:
            pid (str): Campaign identifier.
            data (dict): Campaign data (name, score, objective, faction, tech_start, tech_end, regions, missions).
        """
        self.pid = pid
        self.name = data.get('name', '')
        self.score = data.get('score', 0)
        self.objective = data.get('objective', 0)
        self.faction = data.get('faction', '')
        self.tech_start = data.get('tech_start', [])
        self.tech_end = data.get('tech_end', [])
        self.regions = {}
        if 'regions' in data and isinstance(data['regions'], dict):
            self.regions = data['regions']
        self.missions = []
        if 'missions' in data and isinstance(data['missions'], list):
            for mission_data in data['missions']:
                try:
                    self.missions.append(TMission(mission_data))
                except Exception as e:
                    import logging
                    logging.error(f"Error initializing TMission for campaign {pid}: {e}")
