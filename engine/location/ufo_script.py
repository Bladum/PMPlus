class TUfoScript:
    """
    Represents a trajectory of UFO
    Used to calculate move path of UFO and how it score points, even when not moving
        alien base has different logic and not need script
        sites are just waiting to be picked up
    """
    def __init__(self, script_id, data):
        self.id = script_id
        self.name = data.get('name', script_id)
        self.description = data.get('desc', '')

        # Steps in the trajectory, with their duration
        self.steps = data.get('steps', {})
