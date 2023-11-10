class Action:
    def __init__(self, action_config):
        self.id = action_config['id']
        self.name = action_config['name']
        self.distance = action_config.get('distance', 0)
        self.damage = action_config.get('damage', 0)
        self.accuracy = action_config.get('accuracy', 0)
        self.ap_cost = action_config.get('ap_cost', 0)
        self.stamina_cost = action_config.get('stamina_cost', 0)
        self.stamina_recovery = action_config.get('stamina_recovery', 0)