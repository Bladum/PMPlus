class TPediaEntry:
    """
    represents a single entry in pedia
    """

    CRAFTS = 0
    CRAFT_WEAPONS = 1
    UNITS = 2
    ARMOURS = 3
    ITEMS = 4  # primary secondary items
    FACILITIES = 5

    RACES = 6  # all non alien race
    CLASSES = 7  # classes type 0 only
    ORIGINS = 8  # classes type 2 only
    TRANSFORMATIONS = 8  # classes type 3 only
    MEDALS = 9  # classes type 4 only
    WOUNDS = 10  # classes type 5 only
    EFFECTS = 11  # classes type 6 only

    FACTIONS = 20   # all factions on all worlds
    COUNTRIES = 21  # all countries on all worlds
    REGIONS = 22    # all regions for all worlds
    WORLDS = 23     # earth, mars, moon
    BIOMES = 26     # available bioms on world

    DOSSIERS = 24  # all dossiers for all worlds
    XCOM = 25  # internal xcom communition

    ALIEN_BASES = 29  # alien base
    ALIEN_SITES = 29  # terror site, crash site
    ALIEN_UFO = 30  # small scout ufo
    ALIEN_RACES = 31  # autopsy sectoid
    ALIEN_UNITS = 32  # sectoid soldier corpse
    ALIEN_ITEMS = 33  # plasma weapons, grenades, alien weapons
    ALIEN_ARMOURS = 34  # sectoid armour, shields,
    ALIEN_CLASSES = 35  # medic, navigator, engineer, psionic, type 1 only
    ALIEN_MISSIONS = 36  # research, base supply
    ALIEN_ARTEFACTS = 37  # alien alloys, zrbite, power navigation

    def __init__(self, pid, data):
        self.pid = pid
        self.type = data.get('type', 0)
        self.name = data.get('name', pid)
        self.section = data.get('section', '')
        self.description = data.get('description', '')
        self.image = data.get('image', '')
        self.tech_needed = data.get('tech_needed', [])
        self.order = data.get('order', 0)

        # additional fields that might be present in some entries
        self.related = data.get('related', [])
        self.stats = data.get('stats', {})