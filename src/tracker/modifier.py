class Modifier:
    def __init__(self, modifier_config):
        self.load_config(modifier_config)

    def load_config(self, modifier_config):
        self.skills = modifier_config.get("skills", [])
        pass


# Item and Trait classes derived from Modifier
class Item(Modifier):
    # Implementation specific to items
    pass


class Trait(Modifier):
    # Implementation specific to traits
    pass

