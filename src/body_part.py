import random

from src import BODY_CONFIGS, BodyPartType, InjuryType


class BodyPart:
    def __init__(self, body_type, body_part_type, armor_value, hp_threshold):
        self.body_type = body_type
        self.body_part_type = body_part_type
        self.armor_value = armor_value
        self.hp_threshold = hp_threshold
        self.injury_config = self.initialize_injury_config()

        # Each injury type will now have its own damage counter
        self.damage_counters = {injury: 0 for injury in InjuryType}
        self.injury_counter = {injury: 0 for injury in InjuryType}

    def initialize_injury_config(self):
        # Fetch the injury configuration for the body type and part type from BODY_CONFIGS
        body_config = BODY_CONFIGS.get(self.body_type, {})
        body_part_config = body_config.get(self.body_part_type, {})
        return body_part_config.get("max_injuries", {})

    # ... rest of the BodyPart methods remain unchanged ...

    def get_damage(self, source, modality=None, dmg_roll=None):
        """
        Process the damage received by the body part from a given source, updating the state of the body part.
        """
        damage_value = source.get("damage_value", 0)
        damage_type = source.get(
            "damage_type", "physical"
        )  # Default to 'physical' if not specified
        abilities = source.get("abilities", [])

        # If dmg_roll is not provided, roll for damage variability
        if dmg_roll is None and modality in source:
            damage_variability = source[modality].get(
                "damage_variability", 6
            )  # Default to d6 if not specified
            dmg_roll = random.randint(1, damage_variability)
        damage_value += dmg_roll or 0

        # Apply armor reduction to the damage value
        damage_after_armor = max(0, damage_value - self.armor_value)

        # Determine the type of injury caused by the damage
        injury_type = None
        if damage_type == "elemental":
            injury_type = InjuryType.SHOCK
        elif damage_type == "physical":
            if self.body_part_type == BodyPartType.HEAD and "concussive" in abilities:
                injury_type = InjuryType.CONCUSSION
            else:
                injury_type = InjuryType.BLEED
        elif InjuryType.INJURY in self.injury_config["max_injuries"]:
            injury_type = InjuryType.INJURY

        # Update the damage and injury counters
        if injury_type:
            self.damage_counters[injury_type] += damage_after_armor
            max_injuries = self.injury_config.get(injury_type, float("inf"))
            self.injury_counter[injury_type] = min(
                self.damage_counters[injury_type] // self.hp_threshold,
                max_injuries,
            )
