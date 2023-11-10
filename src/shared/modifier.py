class Modifier:
    def __init__(self, modifier_config):
        self.load_config(modifier_config)

    def load_config(self, modifier_config):
        self.actions = modifier_config.get("actions", [])
        pass
