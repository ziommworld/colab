import unittest
from unittest import mock

from src import BODY_CONFIGS, BodyPartType, BodyType
from src.character.character_body import CharacterBody


# Test cases for CharacterBody
class TestCharacterBody(unittest.TestCase):
    def setUp(self):
        # Setup can be used to create common objects for each test
        self.total_hit_points = 100
        self.equipment = {
            BodyPartType.HEAD: mock.Mock(armor_value=5),
            BodyPartType.TORSO: mock.Mock(armor_value=7),
            BodyPartType.L_ARM_1: mock.Mock(armor_value=3),
            BodyPartType.R_ARM_1: mock.Mock(armor_value=3),
            BodyPartType.L_LEG_1: mock.Mock(armor_value=4),
            BodyPartType.R_LEG_1: mock.Mock(armor_value=4),
        }

        self.character_body = CharacterBody(
            BodyType.HUMANOID, self.total_hit_points, self.equipment
        )

    def test_initialization(self):
        body_parts_count = len(BODY_CONFIGS[BodyType.HUMANOID])

        # Check if the character body is initialized with the correct total hit points
        self.assertEqual(self.character_body.total_hit_points, self.total_hit_points)
        # Check if the character body has the correct number of body parts
        self.assertEqual(len(self.character_body.body_parts), body_parts_count)
        # Check if each body part in the character body has the correct hp threshold
        expected_hp_threshold = self.total_hit_points // body_parts_count
        for bopdy_part_type, body_part in self.character_body.body_parts.items():
            if bopdy_part_type != BodyPartType.TORSO:
                self.assertEqual(body_part.hp_threshold, expected_hp_threshold)
            else:
                remainder = self.total_hit_points % body_parts_count
                self.assertEqual(
                    body_part.hp_threshold, expected_hp_threshold + remainder
                )

    # More test methods would follow here to fully test the functionality of the CharacterBody class


if __name__ == "__main__":
    unittest.main()
