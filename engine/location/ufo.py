class TUfo(TLocation):
    """
    Represents a UFO on the world map as location
    Its temporary, but has assigned a ufo script to manage its movement
    It has deployment to control what units are during battle
    ufo must be first shot down by interception
    """
    def __init__(self, ufo_id, data):
        super().__init__(data)

        self.map_block = data.get('map_block', None)