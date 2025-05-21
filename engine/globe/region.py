
class TRegion:
    """
    Each tile on worls map is assigned to a region
    Regions are used to control location of missions
    Regions have analytics for score
    """

    def __init__(self, data : dict = {}):
        # Required fields
        self.name = data.get("name", "")
        self.is_land = data.get("is_land", False)
        self.id = data.get("id", 0)

        # Optional fields with defaults
        self.description = data.get("description", "")
        self.color = data.get("color", "#000000")
        self.mission_weight = data.get("mission_weight", 10)
        self.base_cost = data.get("base_cost", 500)

        # Lists
        self.service_provided = data.get("service_provided", [])
        self.service_forbidden = data.get("service_forbidden", [])
