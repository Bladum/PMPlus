"""
mission.py

Defines the TMission class, representing a mission created by a campaign. Encapsulates deployment, tech requirements, and world map location logic for campaign-generated missions.

Classes:
    TMission: Mission definition for campaign-generated world map locations.

Last standardized: 2025-06-14
"""

class TMission:
    """
    TMission represents a mission created by a campaign, with deployment and tech requirements.
    It is a physical location on the world map (UFO, base, or static site).

    Attributes:
        ufo (str|None): UFO type if mission is a UFO.
        site (str|None): Site type if mission is a static site.
        base (str|None): Base type if mission is a base.
        count (int): Number of missions to generate.
        chance (float): Probability of mission occurrence.
        timer (int): Delay before mission activation.
        tech_start (list): Technologies required to start.
        tech_end (list): Technologies that end the mission.
        deployments (dict): Deployment options for the mission.
    """

    def __init__(self, data):
        """
        Initialize a mission.

        Args:
            data (dict): Mission data and parameters.
        """
        # what will be created by this mission
        self.ufo = data.get('ufo', None)
        self.site = data.get('site', None)
        self.base = data.get('ufo', None)

        # how many and what is delay before next mission
        self.count = data.get('count', 1)
        self.chance = data.get('chance', 1)
        self.timer = data.get('timer', 0)

        self.tech_start = data.get('tech_start', [])
        self.tech_end = data.get('tech_end', [])

        # Handle deployment options if available
        self.deployments = data.get('deployments', {})