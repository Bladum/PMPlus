class TLocation:
    """
    Single location on world map, it could be a base, a city, a UFO crash site
    it may or may not be detected by xcom
    """
    def __init__(self, loc_id,  data : dict = {}):
        # Required fields
        self.loc_id = loc_id
        self.name = data.get("name", "")
        self.description = data.get("description", "")
        self.position = data.get("position", [])

        # Radar detection fields
        self.initial_cover = data.get("initial_cover", 0)  # max cover value
        self.cover = data.get("cover", self.initial_cover)  # current cover
        self.cover_change = data.get("cover_change", 0)  # how much cover recovers per turn
        self.visible = False  # is visible to player

    def update_visibility(self):
        self.visible = self.cover <= 0

    def replenish_cover(self):
        if self.cover < self.initial_cover:
            self.cover = min(self.initial_cover, self.cover + self.cover_change)
        self.update_visibility()
