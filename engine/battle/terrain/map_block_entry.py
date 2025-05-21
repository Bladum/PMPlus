class TMapBlockEntry:
    """
    represents how map blocks are managed inside terrain
    """
    def __init__(self, data):
        self.name = data.get('name', '')
        self.size = data.get('size', 1)
        self.group = data.get('group', 0)
        self.chance = data.get('chance', 1)
        self.items = data.get('items', {})
        self.units = data.get('units', {})
        self.show = data.get('show', False)