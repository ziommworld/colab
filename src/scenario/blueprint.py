from src.scenario.environment import Environment


class Blueprint(Environment):
    def __init__(self, anchor_point, blueprint_name):
        self.anchor_point = anchor_point  # The anchor point coordinates, e.g., "x0y0z0"
        self.blueprint_name = blueprint_name
        self.tiles = {}  # A dictionary to map tiles with their position and orientation

    def add_tile(self, tile, position, orientation):
        # position: Tuple (x, y, z) representing position relative to the anchor
        # orientation: Tuple (roll, pitch, yaw) representing the tile's orientation
        self.tiles[tile] = {"position": position, "orientation": orientation}

    def describe(self):
        description = f"Blueprint '{self.blueprint_name}' at {self.anchor_point} with {len(self.tiles)} tiles:\n"
        for tile, properties in self.tiles.items():
            description += f"  - {tile.describe()} at position {properties['position']} with orientation {properties['orientation']}\n"
        return description
