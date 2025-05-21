
class TBattleScriptStep:
    """
    Represents a single step in a map generation script
    """

    def __init__(self, data):
        self.type = data.get('type', '')
        self.group = data.get('group', 0)
        self.label = data.get('label', None)
        self.condition = data.get('condition', [])
        self.chance = data.get('chance', 1.0)
        self.runs = data.get('runs', 1)
        self.size = data.get('size', 1)

        # Direction for line generation
        self.direction = data.get('direction', 'horizontal')

        # UFO type for UFO placement
        self.ufo = data.get('ufo', None)