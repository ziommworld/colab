from src.scenario.environment import Environment

class Blueprint(Environment):
    # Represents a design or layout made up of multiple Tiles
    def __init__(self, coordinates, blueprint_name, tiles):
        super().__init__(coordinates)
        self.blueprint_name = blueprint_name
        self.tiles = tiles  # A list or dictionary of Tile objects

    def describe(self):
        return f"Blueprint '{self.blueprint_name}' at {self.coordinates} with {len(self.tiles)} tiles"
