
class TMission:
    """
    Mission is created by campaign
    it is a physical location on world map
        - it's flying ufo (temporary and moving) and must be first intercepted
        - it's new alien base (static and permanent), usually 2 level mission, grounded
        - it's a static site (temporary and static), 1 level mission, grounded
    manage points when mission is failed / succeeded
    """

    def __init__(self, data):

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