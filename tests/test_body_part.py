# Let's write the tests for the BodyPart class based on the provided code and updates.

import unittest
from unittest import mock

from src.character.body_part import BodyPart
from src import BODY_CONFIGS, BodyPartType, BodyType, InjuryType


class TestBodyPart(unittest.TestCase):
    def setUp(self):
        # Setup can be used to create common objects for each test
        self.body_part = BodyPart(
            BodyType.HUMANOID, BodyPartType.HEAD, armor_value=2, hp_threshold=5
        )

    def test_initialization(self):
        # Check if the body part is initialized with correct attributes
        self.assertEqual(self.body_part.body_type, BodyType.HUMANOID)
        self.assertEqual(self.body_part.body_part_type, BodyPartType.HEAD)
        self.assertEqual(self.body_part.armor_value, 2)
        self.assertEqual(self.body_part.hp_threshold, 5)

        # Check if the injury config is initialized correctly
        expected_injury_config = BODY_CONFIGS[BodyType.HUMANOID][BodyPartType.HEAD][
            "max_injuries"
        ]
        self.assertDictEqual(self.body_part.injury_config, expected_injury_config)

        # Check if the damage and injury counters are initialized correctly
        for injury_type in InjuryType:
            self.assertIn(injury_type, self.body_part.damage_counters)
            self.assertEqual(self.body_part.damage_counters[injury_type], 0)

            self.assertIn(injury_type, self.body_part.injury_counters)
            self.assertEqual(self.body_part.injury_counters[injury_type], 0)

    def test_initialize_injury_config(self):
        for body_part_type in BodyPartType:
            body_part = BodyPart(
                BodyType.HUMANOID, body_part_type, armor_value=1, hp_threshold=5
            )
            expected_injury_config = BODY_CONFIGS[BodyType.HUMANOID][body_part_type][
                "max_injuries"
            ]
            self.assertDictEqual(body_part.injury_config, expected_injury_config)

    def test_get_damage_physical_without_armor(self):
        body_part = BodyPart(
            BodyType.HUMANOID, BodyPartType.TORSO, armor_value=0, hp_threshold=5
        )
        source = {"damage_value": 7, "damage_type": "physical", "abilities": []}

        # Mock random.randint to return a fixed value
        with mock.patch("random.randint", return_value=3):
            body_part.get_damage(source)

        # Since armor_value is 0, damage should not be reduced
        # Check if the damage counters are updated correctly
        self.assertEqual(body_part.damage_counters[InjuryType.BLEED], 7)
        # Check if the injury counter is updated correctly
        self.assertEqual(body_part.injury_counters[InjuryType.BLEED], 1)

    def test_get_damage_physical_with_armor(self):
        body_part = BodyPart(
            BodyType.HUMANOID, BodyPartType.TORSO, armor_value=3, hp_threshold=5
        )
        source = {
            "damage_value": 10,
            "damage_type": "physical",
            "abilities": [],
            "modality": {"damage_variability": 6},
        }

        # Pass a fixed dmg_roll value to the method
        body_part.get_damage(source, dmg_roll=2)

        # Armor should reduce the damage by its value
        expected_damage = max(0, (source["damage_value"] + 2) - body_part.armor_value)
        self.assertEqual(body_part.damage_counters[InjuryType.BLEED], expected_damage)

        # Check if the injury counter is updated correctly
        expected_injuries = min(
            expected_damage // body_part.hp_threshold,
            body_part.injury_config[InjuryType.BLEED],
        )
        self.assertEqual(body_part.injury_counters[InjuryType.BLEED], expected_injuries)

    def test_get_damage_elemental(self):
        body_part = BodyPart(
            BodyType.HUMANOID, BodyPartType.TORSO, armor_value=2, hp_threshold=5
        )
        source = {
            "damage_value": 8,
            "damage_type": "elemental",
            "abilities": [],
            "modality": {"damage_variability": 6},
        }

        # Pass a fixed dmg_roll value to the method
        body_part.get_damage(source, dmg_roll=2)

        # Armor should reduce the damage by its value
        expected_damage = max(0, (source["damage_value"] + 2) - body_part.armor_value)
        self.assertEqual(body_part.damage_counters[InjuryType.SHOCK], expected_damage)

        # Check if the injury counter is updated correctly
        expected_injuries = min(
            expected_damage // body_part.hp_threshold,
            body_part.injury_config.get(InjuryType.SHOCK, float("inf")),
        )
        self.assertEqual(body_part.injury_counters[InjuryType.SHOCK], expected_injuries)

    def test_get_damage_concussive(self):
        body_part = BodyPart(
            BodyType.HUMANOID, BodyPartType.HEAD, armor_value=1, hp_threshold=3
        )
        source = {
            "damage_value": 5,
            "damage_type": "physical",
            "abilities": ["concussive"],
            "modality": {"damage_variability": 6},
        }

        # Pass a fixed dmg_roll value to the method
        body_part.get_damage(source, dmg_roll=1)

        # Armor should reduce the damage by its value
        expected_damage = max(0, (source["damage_value"] + 1) - body_part.armor_value)
        self.assertEqual(
            body_part.damage_counters[InjuryType.CONCUSSION], expected_damage
        )

        # Check if the injury counter is updated correctly
        expected_injuries = min(
            expected_damage // body_part.hp_threshold,
            body_part.injury_config.get(InjuryType.CONCUSSION, float("inf")),
        )
        self.assertEqual(
            body_part.injury_counters[InjuryType.CONCUSSION], expected_injuries
        )

    def test_injury_counter_update(self):
        body_part = BodyPart(
            BodyType.HUMANOID, BodyPartType.TORSO, armor_value=1, hp_threshold=5
        )
        source = {
            "damage_value": 4,
            "damage_type": "physical",
            "abilities": [],
            "modality": {"damage_variability": 6},
        }

        # Apply damage several times to exceed the hp_threshold and cause multiple injuries
        for _ in range(4):  # Applying damage 4 times
            body_part.get_damage(source, dmg_roll=4)

        # Check if the injury counter is updated correctly
        expected_injuries = min(
            4 * (source["damage_value"] + 4) // body_part.hp_threshold,
            body_part.injury_config[InjuryType.BLEED],
        )
        self.assertEqual(body_part.injury_counters[InjuryType.BLEED], expected_injuries)

    def test_damage_at_hp_threshold(self):
        body_part = BodyPart(
            BodyType.HUMANOID, BodyPartType.TORSO, armor_value=1, hp_threshold=5
        )
        source = {
            "damage_value": body_part.hp_threshold,  # Set damage to one less than the hp_threshold
            "damage_type": "physical",
            "abilities": [],
            "modality": {"damage_variability": 6},
        }

        # Apply damage once
        body_part.get_damage(source, dmg_roll=1)

        # Check if the injury counter is updated correctly
        expected_injuries = 1  # Damage meets hp_threshold exactly once
        self.assertEqual(body_part.injury_counters[InjuryType.BLEED], expected_injuries)

    def test_max_injuries_limit(self):
        body_part = BodyPart(
            BodyType.HUMANOID, BodyPartType.TORSO, armor_value=1, hp_threshold=5
        )
        max_injuries = body_part.injury_config[InjuryType.BLEED]
        source = {
            "damage_value": 20,  # High damage value to ensure max injuries are reached
            "damage_type": "physical",
            "abilities": [],
            "modality": {"damage_variability": 6},
        }

        # Apply damage once
        body_part.get_damage(source, dmg_roll=1)

        # The injury counter should not exceed the max_injuries limit
        self.assertEqual(body_part.injury_counters[InjuryType.BLEED], max_injuries)


if __name__ == "__main__":
    unittest.main()
