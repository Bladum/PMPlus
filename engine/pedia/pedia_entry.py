"""
TPediaEntry: Represents a single entry in the UFOpedia system.
Purpose: Stores all data and metadata for a pedia entry, including type, name, description, and related stats.
Last update: 2025-06-11
"""

class TPediaEntry:
    """
    Represents a single entry in the UFOpedia.
    Stores all relevant data, such as type, name, description, sprite, and related stats.
    Attributes:
        pid (str): Entry ID.
        type (int): Entry type/category.
        name (str): Display name.
        section (str): Section/category name.
        description (str): Entry description.
        sprite (str): Sprite or image reference.
        tech_needed (list): Technologies required to unlock.
        order (int): Display order.
        related (list): Related entries.
        stats (dict): Additional stats or metadata.
    """

    CRAFTS = 0
    CRAFT_WEAPONS = 1
    UNITS = 2
    ARMOURS = 3
    ITEMS = 4  # primary secondary items
    FACILITIES = 5

    RACES = 6  # all non alien race
    PROMOTIONS = 7 # traits type 0
    ORIGINS = 8  # traits type 2 only
    TRANSFORMATIONS = 8  # traits type 3 only
    MEDALS = 9  # traits type 4 only
    WOUNDS = 10  # traits type 5 only
    EFFECTS = 11  # traits type 6 only

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
    ALIEN_RANKS = 35  # medic, navigator, engineer, psionic, type 1 only
    ALIEN_MISSIONS = 36  # research, base supply
    ALIEN_ARTEFACTS = 37  # alien alloys, zrbite, power navigation

    def __init__(self, pid, data):
        """
        Initialize a TPediaEntry.
        Args:
            pid (str): Unique identifier for the entry.
            data (dict): Dictionary containing entry data and metadata.
        Attributes:
            pid (str): Entry ID.
            type (int): Entry type/category.
            name (str): Display name.
            section (str): Section/category name.
            description (str): Entry description.
            sprite (str): Sprite or image reference.
            tech_needed (list): Technologies required to unlock.
            order (int): Display order.
            related (list): Related entries.
            stats (dict): Additional stats or metadata.
        """
        self.pid = pid
        self.type = data.get('type', 0)
        self.name = data.get('name', pid)
        self.section = data.get('section', '')
        self.description = data.get('description', '')
        self.sprite = data.get('sprite', '')
        self.tech_needed = data.get('tech_needed', [])
        self.order = data.get('order', 0)
        self.related = data.get('related', [])
        self.stats = data.get('stats', {})

    def is_unlocked(self, unlocked_techs):
        """
        Check if the entry is unlocked based on available technologies.
        Args:
            unlocked_techs (list): List of unlocked technology names/IDs.
        Returns:
            bool: True if all required techs are unlocked, else False.
        """
        return all(tech in unlocked_techs for tech in self.tech_needed)
