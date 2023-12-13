from src import BODY_CONFIGS, BodyPartType, DamageType, InjuryType


class BodyPart:
    def __init__(self, body_type, body_part_type, armor_value, hp_threshold):
        self.body_type = body_type
        self.body_part_type = body_part_type
        self.armor_value = armor_value
        self.hp_threshold = hp_threshold
        self.injury_config = self.init_injury_config()

        # Each injury type will now have its own damage counter
        self.damage_counters = {injury: 0 for injury in InjuryType}
        self.injury_counters = {injury: 0 for injury in InjuryType}

    def init_injury_config(self):
        # Fetch the injury configuration for the body type and part type from BODY_CONFIGS
        body_config = BODY_CONFIGS.get(self.body_type, {})
        body_part_config = body_config.get(self.body_part_type, {})
        return body_part_config.get("max_injuries", {})

    def receive_damage(self, damage_value, damage_type, abilities, armor_penetration=0):
        """
        Process damage received and apply injuries as needed.
        """
        effective_armor = max(self.armor_value - armor_penetration, 0)
        damage_after_armor = max(0, damage_value - effective_armor)
        injury_type = self.determine_injury_type(damage_type, abilities)

        if injury_type:
            self.damage_counters[injury_type] += damage_after_armor
            max_injuries = self.injury_config.get(injury_type, float("inf"))
            injuries = self.damage_counters[injury_type] // self.hp_threshold
            self.injury_counters[injury_type] = min(injuries, max_injuries)

    def determine_injury_type(self, damage_type, abilities):
        """
        Determine the type of injury based on the damage type and abilities of the attacker.
        """
        if damage_type == DamageType.ELEMENTAL:
            return InjuryType.SHOCK
        elif damage_type == DamageType.PHYSICAL:
            # Head injuries can be concussions if the attack is concussive
            if self.body_part_type == BodyPartType.HEAD and "concussive" in abilities:
                return InjuryType.CONCUSSION
            # Arm injuries can result in the arm being disabled
            elif self.body_part_type in [
                BodyPartType.L_ARM_1,
                BodyPartType.R_ARM_1,
                BodyPartType.L_ARM_2,
                BodyPartType.R_ARM_2,
            ]:
                return InjuryType.DISABLE
            # Leg injuries can result in immobilization
            elif self.body_part_type in [
                BodyPartType.L_LEG_1,
                BodyPartType.R_LEG_1,
                BodyPartType.L_LEG_2,
                BodyPartType.R_LEG_2,
            ]:
                return InjuryType.IMMOBILIZE
            else:
                return InjuryType.BLEED
        # If the damage type doesn't match or if there are other conditions, you may add them here
        return None  # pure
