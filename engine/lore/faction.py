class TFaction:
    """
    Owner of each mission, owns locations
    Faction may be ally or enemy of XCOM
    """

    def __init__(self, data : dict = {}):
        # Required fields
        self.name = data.get("name", "")
        self.description = data.get("description", "")
        self.id = data.get("id", 0)

        self.aggression = data.get("aggression", 0)
        self.pedia = data.get("pedia", '')

        self.tech_start = data.get("tech_start", [])
        self.tech_end = data.get("tech_end", [])