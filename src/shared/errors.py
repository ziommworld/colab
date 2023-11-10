class InvalidBodyPartError(Exception):
    """Exception raised for errors in the input body part type."""

    def __init__(self, body_part_type, message="Invalid body part specified"):
        self.body_part_type = body_part_type
        self.message = f"{message}: {body_part_type}"
        super().__init__(self.message)
