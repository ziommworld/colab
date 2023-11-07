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

    def perform(self, character):
        """
        Apply the action to the given character, modifying their state as necessary.
        """
        result = {
            "action_name": self.name,
            "distance": self.distance,
            "accuracy": self.accuracy,
            "damage": self.damage,
            "ap_cost": self.ap_cost,
            "stamina_cost": self.stamina_cost,
            "stamina_recovery": self.stamina_recovery
        }

        # Deduct AP and stamina cost
        character.round_ap -= self.ap_cost
        character.stamina -= self.stamina_cost
        character.stamina += self.stamina_recovery

        return result

