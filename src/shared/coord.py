class Coordinate:
    def __init__(self, coord_str):
        self.x, self.y, self.z = self.parse_coord_string(coord_str)

    @staticmethod
    def parse_coord_string(coord_str):
        # Regular expression to extract x, y, z values from the string
        match = re.match(r"x(-?\d+)y(-?\d+)z(-?\d+)", coord_str)
        if match:
            return tuple(map(int, match.groups()))
        else:
            raise ValueError(f"Invalid coordinate string: {coord_str}")

    def __str__(self):
        return f"x{self.x}y{self.y}z{self.z}"
