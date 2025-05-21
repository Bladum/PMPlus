from engine.lore.mission import TMission


class TCampaign:
    """
    Single campaign is set of missions for specific faction in specific region
    It is created by calendar
    It has a start date, end date, and list of missions, limited by research status
    It has a goal to achieve, when alien will score points
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

    def __init__(self, campaign_id, data):
        self.id = campaign_id
        self.score = data.get('score', 0)
        self.objective = data.get('objective', 0)
        self.faction = data.get('faction', '')

        # Technology requirements
        self.tech_start = data.get('tech_start', [])
        self.tech_end = data.get('tech_end', [])

        # Region weights
        self.regions = {}
        if 'regions' in data and isinstance(data['regions'], dict):
            self.regions = data['regions']

        # Missions list
        self.missions = []
        if 'missions' in data and isinstance(data['missions'], list):
            for mission_data in data['missions']:
                self.missions.append(TMission(mission_data))
