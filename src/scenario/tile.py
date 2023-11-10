class Tile(Environment):
    # Represents a basic building block of the game's world
    def __init__(self, coordinates, tile_type):
        super().__init__(coordinates)
        self.tile_type = tile_type

    def describe(self):
        return f"Tile of type {self.tile_type} at {self.coordinates}"
