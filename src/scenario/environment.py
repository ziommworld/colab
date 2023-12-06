class Environment:
    def __init__(self, coordinates, interactions):
        self.coordinates = coordinates  # Coordinates in the form of NxEy
        self.interactions = {  # Possible interactions on each side
            "north": [],
            "east": [],
            "south": [],
            "west": [],
        }
        self.interactions.update(interactions)
        self.stackable = False  # Determines if this tile can be stacked

    def add_interaction(self, direction, interaction):
        if direction in self.interactions:
            self.interactions[direction].append(interaction)

    # Method to check if an interaction is possible on a given side
    def can_interact(self, direction):
        return len(self.interactions[direction]) > 0

    # This method would be more complex, depending on the rules for combining environments
    def combine_with(self, other_environment):
        pass

    # Additional properties and methods related to the environment
    # ...