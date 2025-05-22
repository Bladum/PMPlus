
class TBattleEffect:
    """
    special effect that is used on battle map for all tiles / units e.g. smoke, fire, panic, sanity etc
    """

    def __init__(self, pid, data):
        self.pid = pid
        self.name = data.get('name', pid)
        self.description = data.get('description', '')
        self.icon = data.get('icon', '')


        # Requirements to get