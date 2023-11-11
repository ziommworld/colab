class CharacterBuilder:
    def __init__(self, basic_settings):
        # Raises KeyError if not all required keys are present
        self.name = basic_settings["name"]
        self.level = basic_settings["level"]
        self.body_type = basic_settings["body_type"]
        self.race = basic_settings["race"]
        self.alignment = basic_settings["alignment"]
        
        
