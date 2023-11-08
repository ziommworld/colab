import random
from src import BodyType
from src.common import to_snake_case

from .action import Action
from .character_body import CharacterBody


class Character:
    def __init__(self, config):
        self.load_config(config)
        self.id = self.generate_id(self.player_name, self.character_name)

        self.init_action_pool()
        self.combat_log = []

        # Initialize equipment and then the body
        self.body = CharacterBody(
            self.body_type, self.total_hit_points, config.get("equipment", {})
        )

        # Initialize character state
        self.max_stamina = self.stamina  # max value for stamina
        self.max_hit_points = self.total_hit_points  # max value for hit points

        self.initial_stamina = self.stamina  # combat log comparison
        self.initial_hit_points = self.total_hit_points  # combat log comparison

        self.round_ap = 4
        self.previous_round_ap = 0  # used to calculate stamina penalty

    @staticmethod
    def generate_id(player_name, character_name):
        """
        Generate a unique id from player_name and character_name in snake case.
        """
        snake_case_player_name = to_snake_case(player_name)
        snake_case_character_name = to_snake_case(character_name)
        return f"{snake_case_player_name}_{snake_case_character_name}"

    def load_config(self, config):
        self.character_name = config.get("character_name", "Unknown")
        self.player_name = config.get("player_name", "Player")
        self.body_type = config.get("body_type", BodyType.HUMANOID)

        self.move_speed = config.get(
            "move_speed", 5
        )  # Assuming a default move speed of 5
        self.stamina = config.get("stamina", 10)  # Assuming a default stamina of 10
        self.total_hit_points = config.get("total_hit_points", 100)  # Default HP of 100
        self.initiative_score = config.get(
            "initiative_score", 10
        )  # Default initiative score of 10

        self.inventory = config.get("inventory", {})  # Default empty inventory
        self.modifiers = config.get("modifiers", [])  # Default empty list of modifiers

    def init_action_pool(self):
        # Initialize an empty dictionary for the action pool
        self.action_pool = {}

        # Loop through each modifier that the character has
        for modifier in self.modifiers:
            # Get the list of action configurations from the modifier
            action_configs = modifier.actions

            # Loop through each action configuration and create an Action instance
            for action_config in action_configs:
                # Create the Action instance
                action = Action(action_config)

                # Add the action to the action pool using the action ID as the key
                self.action_pool[action.id] = action

    def roll_for_initiative(self, initiative_roll=None):
        """
        Roll for initiative using a D20 or use the provided initiative_roll if given.
        """
        # If an initiative_roll is provided, use it, otherwise roll a D20
        roll = initiative_roll if initiative_roll is not None else random.randint(1, 20)
        self.initiative_score = roll + self.composure

        self.log_event(
            description=f"Rolled for initiative: {roll} + {self.composure} (Composure) = {self.initiative_score}",
        )

        return self.initiative_score

    def play_action(self, action_name, ap_spent=None):
        action_id = action_name if ap_spent is None else f"{action_name}_{ap_spent}"

        # Check if the action exists in the action pool
        if action_id not in self.action_pool:
            raise ValueError(f"Action '{action_id}' not found in the action pool.")

        # Get the action object from the action pool
        action = self.action_pool[action_id]

        # Check if the AP spent is compatible with the action's cost
        if ap_spent is not None and ap_spent != action.ap_cost:
            raise ValueError(
                f"AP cost '{ap_spent}' not valid for action '{action_name}'."
            )

        # Deduct AP cost and apply the action
        self.round_ap -= action.ap_cost
        self.stamina -= action.stamina_cost
        self.check_stamina_state()  # check if we need to apply the winded state

        # Update combat log with the action name and details

        self.log_event(
            description=f"Performed action '{action_name}'.",
            stamina_cost=action.stamina_cost,
            ap_cost=action.ap_cost,
        )

    def take_damage(
        self, damage_amount, body_part_type, damage_source, modality=None, dmg_roll=None
    ):
        """
        Apply damage to a specific body part of the character.
        """
        # Locate the body part in the character's body
        body_part = self.body.get_body_part(body_part_type)

        # If the body part is found, apply damage to it
        if body_part:
            body_part.get_damage(damage_source, modality, dmg_roll)
        else:
            raise ValueError(f"Body part '{body_part_type}' not found.")

        self.log_event(
            description=f"{body_part_type.value.capitalize()} took {damage_amount} damage.",
            hp_loss=damage_amount,
        )

    def round_reset(self):
        # Now, we save the initial values for the next round
        self.initial_stamina = self.stamina
        self.initial_hit_points = self.total_hit_points

        # check for stamina penalty before resetting AP
        self.check_stamina_penalty()

        self.previous_round_ap = 4 - self.round_ap
        self.round_ap = 4  # Reset action points for the new round

    def check_stamina_penalty(self):
        """
        Check if a stamina penalty should be applied based on AP spent in the current and the last round.
        """
        # Calculate the total AP spent in the current and previous round
        total_ap_spent = self.round_ap + self.previous_round_ap
        penalty_applied = 0

        if total_ap_spent == 7:
            penalty_applied = 1
        elif total_ap_spent == 8:
            penalty_applied = 2

        self.stamina -= penalty_applied
        self.check_stamina_state()  # check if we need to apply the winded state

        if penalty_applied > 0:
            self.log_event(
                description=f"Stamina penalty applied for excessive AP use: {penalty_applied} stamina point(s) lost.",
                stamina_cost=penalty_applied,
            )

    def check_stamina_state(self):
        """
        Check if the character is winded, and apply the winded state if necessary.
        """
        if self.stamina == 0:
            self.log_event(
                description=f"Character is blacked-out ({self.stamina} stamina).",
            )
        elif self.stamina == 1:
            self.log_event(
                description=f"Character is fatigued ({self.stamina} stamina).",
            )
        elif self.stamina <= 3:
            self.log_event(
                description=f"Character is tired ({self.stamina} stamina).",
            )
        elif self.stamina <= 5:
            self.log_event(
                description=f"Character is winded ({self.stamina} stamina).",
            )

    def summarize_round(self):
        ap_spent = 4 - self.round_ap
        stamina_spent = self.initial_stamina - self.stamina
        hp_loss = self.initial_hit_points - self.total_hit_points

        self.log_event(
            description=f"Round Summary: Stamina: {self.initial_stamina} -> {self.stamina}, HP: {self.initial_hit_points} -> {self.total_hit_points}",
            stamina_cost=stamina_spent,
            ap_cost=ap_spent,
            hp_loss=hp_loss,
        )

    def log_event(
        self,
        description="",
        stamina_cost=0,
        ap_cost=0,
        hp_loss=0,
    ):
        """
        Add an entry to the combat log with a consistent format.
        """
        entry = {
            "description": description,
            "stamina_cost": stamina_cost,
            "ap_cost": ap_cost,
            "hp_loss": hp_loss,
        }

        self.combat_log.append(entry)
