class TSite(TLocation):
    """
    Represent a mission on world map, which is not UFO, neither base
    Its does not move, it is static
    Its temporary, when mission is finished, it will be removed and points scored
    It has deployment to control what units are during battle
    it has no ufo script
    """
    def __init__(self, loc_id, data):
        super().__init__(loc_id, data)

        self.map_blocks = data.get('map_blocks', {})