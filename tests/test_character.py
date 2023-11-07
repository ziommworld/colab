import unittest
from unittest import mock

from src import BodyPartType, BodyType
from src.character import Character


class TestCharacter(unittest.TestCase):
    def setUp(self):
        # Setup code to create a character instance
        config = {
            "character_name": "TestCharacter",
            "player_name": "TestPlayer",
            "body_type": BodyType.HUMANOID,
            "move_speed": 5,
            "stamina": 10,
            "total_hit_points": 100,
            "initiative_score": 15,
            "inventory": {},
            "modifiers": [],  # Assuming modifiers have a structure that includes 'actions'
            "equipment": {
                BodyPartType.HEAD: {"armor_value": 0},
                BodyPartType.TORSO: {"armor_value": 0},
                BodyPartType.L_ARM: {"armor_value": 0},
                BodyPartType.R_ARM: {"armor_value": 0},
                BodyPartType.L_LEG: {"armor_value": 0},
                BodyPartType.R_LEG: {"armor_value": 0},
            },
        }
        self.character = Character(config)

    def test_character_initialization(self):
        # Test that character initialization sets the expected attributes
        self.assertEqual(self.character.character_name, "TestCharacter")
        self.assertEqual(self.character.player_name, "TestPlayer")
        self.assertEqual(self.character.body_type, BodyType.HUMANOID)
        self.assertEqual(self.character.move_speed, 5)
        self.assertEqual(self.character.stamina, 10)
        self.assertEqual(self.character.total_hit_points, 100)
        self.assertEqual(self.character.initiative_score, 15)

    def test_play_action_not_in_pool(self):
        # Test that playing an action not in the pool raises a ValueError
        with self.assertRaises(ValueError):
            self.character.play_action("NonExistentAction")


if __name__ == "__main__":
    unittest.main()
