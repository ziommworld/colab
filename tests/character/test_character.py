import unittest

from src.character import Character
from src import BodyType


class TestCharacter(unittest.TestCase):
    def setUp(self):
        self.config = {
            "character_name": "TestCharacter",
            "player_name": "TestPlayer",
            "body_type": BodyType.HUMANOID,
            "move_speed": 5,
            "stamina": 10,
            "total_hit_points": 100,
            "initiative_score": 15,
            "inventory": {},
            "modifiers": [{"actions": []}],  # Example modifier with no actions
            "equipment": {
                "head": {"armor_value": 5},
                "torso": {"armor_value": 7},
                "l_arm": {"armor_value": 3},
                "r_arm": {"armor_value": 3},
                "l_leg": {"armor_value": 4},
                "r_leg": {"armor_value": 4},
            },  # Simplified for testing
        }
        self.character = Character(self.config)

    def test_id_generation(self):
        self.assertEqual(self.character.id, "test_player_test_character")

    def test_character_initialization(self):
        # Test that character initialization sets the expected attributes
        self.assertEqual(self.character.character_name, "TestCharacter")
        # ... other attribute checks ...

    def test_init_action_pool(self):
        # Test initialization of action pool
        self.character.init_action_pool()
        self.assertIsInstance(self.character.action_pool, dict)

    def test_play_action_not_in_pool(self):
        # Test playing an action not in the pool raises a ValueError
        with self.assertRaises(ValueError):
            self.character.play_action("NonExistentAction")

    def test_play_action(self):
        # Test playing an action reduces round AP and stamina accordingly
        action_config = {
            "name": "TestAction",
            "ap_cost": 2,
            "stamina_cost": 1,
            "id": "TestAction_2",
        }
        self.character.modifiers[0]["actions"].append(action_config)
        self.character.init_action_pool()
        initial_round_ap = self.character.round_ap
        initial_stamina = self.character.stamina
        self.character.play_action("TestAction", 2)
        self.assertEqual(self.character.round_ap, initial_round_ap - 2)
        self.assertEqual(self.character.stamina, initial_stamina - 1)

    def test_take_damage(self):
        # Test that taking damage updates the character's hit points
        initial_hit_points = self.character.total_hit_points
        damage_amount = 20
        self.character.take_damage(damage_amount, "TORSO", "Sword")
        self.assertEqual(
            self.character.total_hit_points, initial_hit_points - damage_amount
        )

    def test_round_reset(self):
        # Test that resetting the round updates the character's AP and other round-based attributes
        self.character.round_ap = 1
        self.character.stamina = 5
        self.character.total_hit_points = 90
        self.character.end_round()
        self.assertEqual(self.character.round_ap, 4)
        self.assertEqual(
            self.character.stamina, 4
        )  # Assuming a penalty was applied for low AP
        self.assertEqual(self.character.total_hit_points, 90)

    # Add more tests for other methods like check_stamina_state, summarize_round, etc.


if __name__ == "__main__":
    unittest.main()
