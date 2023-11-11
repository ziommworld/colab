from enum import Enum


# Define an enumeration for skill types
class SkillType(Enum):
    MOVEMENT = "movement"
    ATTACK = "attack"
    UTILITY = "utility"


# Define a class for skill modalities with their specific configurations
class SkillModality:
    def __init__(self, modality_config):
        self.id = modality_config["id"]
        self.name = modality_config["name"]
        self.distance = modality_config.get("distance", 0)
        self.damage = modality_config.get("damage", 0)
        self.accuracy = modality_config.get("accuracy", 0)
        self.ap_cost = modality_config.get("ap_cost", 0)
        self.stamina_cost = modality_config.get("stamina_cost", 0)
        self.stamina_recovery = modality_config.get("stamina_recovery", 0)


class Skill:
    def __init__(self, skill_config):
        self.id = skill_config["id"]
        self.name = skill_config["name"]
        self.skill_type = skill_config["skill_type"]
        self.modalities = {}  # Contains SkillModality instances

    def add_modality(self, modality_config):
        modality = SkillModality(**modality_config)
        self.modalities[modality.name] = modality

    def play(self, modality_name, *args, **kwargs):
        modality = self.modalities.get(modality_name)
        if not modality:
            raise ValueError(f"Modality {modality_name} not found in skill.")
        # Implement logic to play the skill based on the modality

    def get_modalities(self):
        return list(self.modalities.keys())


class Action(Skill):
    # Specific implementation for actions
    pass


class Reaction(Skill):
    # Specific implementation for reactions
    pass


class Interaction(Skill):
    # Specific for environment interactions
    pass


BASIC_ATTACK_MODALITIES = {
    "quick": {
        "id": "quick",
        "name": "Quick Attack",
        "ap_cost": 2,
        "stamina_cost": 1,
        "accuracy": -1,
        "damage": -6,
    },
    "normal": {
        "id": "normal",
        "name": "Normal Attack",
        "ap_cost": 3,
        "stamina_cost": 1,
        "accuracy": 0,
        "damage": 0,
    },
    "steady": {
        "id": "steady",
        "name": "Steady Attack",
        "ap_cost": 4,
        "stamina_cost": 1,
        "accuracy": +2,
        "damage": 0,
    },
    "charged": {
        "id": "charged",
        "name": "Charged Attack",
        "ap_cost": 3,
        "stamina_cost": 1,
        "accuracy": -1,
        "damage": +6,
    },
    "dual_wield": {
        "id": "dual_wield",
        "name": "Dual Wield Attack",
        "ap_cost": 3,
        "stamina_cost": 2,
        "accuracy": -2,
        "damage": 0,
    },
    # Additional modalities can be added here
}

BASIC_SKILLS = {
    "crouch": {"id": "crouch", "name": "Crouch", "type": "action", "ap_cost": 1},
    "crawl": {"id": "crawl", "name": "Crawl", "type": "action", "ap_cost": 1},
    "stand_up": {"id": "stand_up", "name": "Stand Up", "type": "action", "ap_cost": 1},
    "pass": {"id": "pass", "name": "Pass", "type": "action", "ap_cost": 0},
    "rest": {
        "id": "rest",
        "name": "Rest",
        "type": "action",
        "ap_cost": 0,
        "rounds_duration": 3,
        "stamina_recovery": [1, 2, 4],
    },
    "recovery": {"id": "recovery", "name": "Recovery", "type": "action", "ap_cost": 0},
    "push": {
        "id": "push",
        "name": "Push",
        "type": "action",
        "ap_cost": 2,
        "stamina_cost": 1,
    },
    "wrestle": {
        "id": "wrestle",
        "name": "Wrestle",
        "type": "action",
        "ap_cost": 2,
        "stamina_cost": 1,
    },
    "maintain_distance": {
        "id": "maintain_distance",
        "name": "Maintain/Remove Distance",
        "type": "action",
        "ap_cost": 1,
        "stamina_cost": 1,
    },
    "jump": {"id": "jump", "name": "Jump", "type": "action", "ap_cost": 2},
    "drop_down": {
        "id": "drop_down",
        "name": "Drop Down",
        "type": "action",
        "ap_cost": 1,
    },
    "look_out": {"id": "look_out", "name": "Look Out", "type": "action", "ap_cost": 2},
    "hide": {"id": "hide", "name": "Hide", "type": "action", "ap_cost": 2},
    "pick_up": {"id": "pick_up", "name": "Pick Up", "type": "action", "ap_cost": 1},
    "drop": {"id": "drop", "name": "Drop", "type": "action", "ap_cost": 0},
    "equip": {"id": "equip", "name": "Equip/Unequip", "type": "action", "ap_cost": 1},
    "overwatch": {
        "id": "overwatch",
        "name": "Overwatch",
        "type": "action",
        "ap_cost": 1,
    },
    "dodge": {
        "id": "dodge",
        "name": "Dodge",
        "type": "reaction",
        "ap_cost": 2,
        "stamina_cost": 1,
    },
    "block": {
        "id": "block",
        "name": "Block",
        "type": "reaction",
        "ap_cost": 2,
        "stamina_cost": 1,
    },
    "attack_of_opportunity": {
        "id": "attack_of_opportunity",
        "name": "Attack of Opportunity",
        "type": "reaction",
        "ap_cost": 0,
    }
    # Add interaction skills here if any
}
