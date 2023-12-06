from src import BODY_CONFIGS, BodyPartType
from src.character.body_part import BodyPart
from src.character.equipment import Equipment
from src.shared.errors import InvalidBodyPartError


class CharacterBody:
    def __init__(self, body_type, total_hit_points, equipment):
        self.body_type = body_type
        self.total_hit_points = total_hit_points

        self.init_equipment(equipment)
        self.init_body_parts(self.body_type, self.total_hit_points, self.equipment)

    def init_body_parts(self, body_type, total_hit_points, equipment):
        body_parts = {}

        # Determine the number of body parts based on the body type
        num_body_parts = len(BODY_CONFIGS[body_type])

        # Divide total HP into body parts equally
        hp_segment = total_hit_points // num_body_parts
        hp_distribution = {
            body_part: hp_segment for body_part in BODY_CONFIGS[body_type].keys()
        }

        # Add up remainder HP
        hp_distribution[BodyPartType.TORSO] += total_hit_points % num_body_parts

        # Create BodyPart instances for each part
        for body_part in BODY_CONFIGS[body_type].keys():
            body_parts[body_part] = BodyPart(
                body_type=body_type,
                body_part_type=body_part,
                armor_value=self.equipment[body_part].armor_value,
                hp_threshold=hp_distribution[body_part],
            )

        self.body_parts = body_parts

    def init_equipment(self, equipment_config):
        """
        Initialize the character's equipment based on the provided configuration.
        """
        equipment = {}
        for body_part in BODY_CONFIGS[self.body_type].keys():
            armor_value = equipment_config.get(body_part, {}).get("armor_value", 0)
            equipment[body_part] = Equipment(
                body_part=body_part,
                armor_value=armor_value,
            )

        self.equipment = equipment

    def get_body_part_count(self, body_type):
        return len(BODY_CONFIGS.get(body_type, {}))

    def get_body_part(self, body_part_type):
        return self.body_parts.get(body_part_type, None)

    def get_injuries(self):
        """
        Return a dictionary of injuries aggregated by type across all body parts.
        """
        combined_injuries = {}

        # Iterate over each body part and combine the injury counters
        for body_part in self.body_parts.values():
            for injury_type, count in body_part.injury_counter.items():
                if count > 0:  # Only include injuries that are present
                    if injury_type in combined_injuries:
                        combined_injuries[injury_type] += count
                    else:
                        combined_injuries[injury_type] = count

        return combined_injuries

    def get_damage(self, body_part_type, damage_amount, damage_type, abilities):
        """
        Apply damage to a specified body part.
        """
        # Find the corresponding BodyPart object
        body_part = self.get_body_part(body_part_type)

        # If the body part exists, call its receive_damage() method
        if body_part:
            body_part.receive_damage(damage_amount, damage_type, abilities)
        else:
            raise InvalidBodyPartError(body_part_type)