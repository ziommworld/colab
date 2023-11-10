import random
from src import BodyType, InjuryType
from src.common import to_snake_case
from src.errors import InvalidBodyPartError
from src.state import State

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
        self.states = []
        self.states_map = {}

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

    def set_state(self, state_name, duration=-1, intensity=0):
        """
        Set a state on the character, either adding a new state or updating the intensity of an existing one.
        """
        has_intensity = intensity > 0
        has_duration = duration > -1  # 0 is reserved for indefinitely small duration

        # Find if the state already exists
        existing_state = self.states_map.get(state_name)

        if existing_state :
            if has_intensity:
                existing_state.increase_intensity(intensity)

            if has_duration:
                existing_state.duration += duration # ! check if this is correct
        else:
            # Add a new state if it doesn't exist
            new_state = State(state_name, duration, intensity)

        self.states_map[state_name] = existing_state or new_state

    def remove_state(self, state_name):
        # Remove a state from the character's list of states by name
        self.states = [state for state in self.states if state.name != state_name]

        if state_name in self.states_map:
            del self.states_map[state_name]
        else:
            raise ValueError(f"State '{state_name}' not found.")

    def update_states(self):
        # Update the list of states, removing any that have expired
        for state in self.states[:]:  # Make a copy of the list for safe iteration
            state.decrement_duration()
            if state.is_expired():
                self.remove_state(state.name)

    def start_round(self):
        """
        Perform actions at the start of the round, such as applying bleeding damage.
        """
        # apply the hit points loss (bleeding/etc)
        hit_points_loss = self.calculate_state_modifiers()["damage_per_round"]
        self.total_hit_points -= hit_points_loss

        # make sure the game continues
        if not self.check_is_dead():
            # Update character states (like decrementing duration of 'blacked_out')
            self.update_states()

    def end_round(self):
        # check for stamina penalty before resetting AP
        self.check_ap_stamina_penalty()

        # summarize round after everything is done
        self.summarize_round()

        # now, we save the initial values for the next round
        self.initial_stamina = self.stamina
        self.initial_hit_points = self.total_hit_points

        # store and reset action points for the new round
        self.previous_round_ap = 4 - self.round_ap
        self.round_ap = 4

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

    def take_damage(self, body_part_type, damage_source, modality=None, dmg_roll=None):
        """
        Apply damage to a specific body part of the character.
        """
        # Locate the body part in the character's body
        body_part = self.body.get_body_part(body_part_type)

        # If the body part is found, apply damage to it
        if body_part:
            damage_amount = body_part.get_damage(damage_source, modality, dmg_roll)
            self.total_hit_points -= damage_amount

        else:
            raise InvalidBodyPartError(body_part_type)

        self.log_event(
            description=f"{body_part_type.value.capitalize()} took {damage_amount} damage.",
            hp_loss=damage_amount,
        )

    def calculate_state_modifiers(self):
        """
        Calculate the cumulative modifuers of the character's states (including injuries).
        """
        modifiers = {
            "stamina": 0,
            "move_speed": 0,
            "action_points": 0,
            "damage_per_round": 0,
            "combat_proficiency": 0,
            "general_proficiency": 0,
        }

        # Evaluate state effects
        for state in self.states:
            if state.name == "fatigued":
                modifiers["move_speed"] -= 3
                modifiers["combat_proficiency"] -= 3
                modifiers["general_proficiency"] -= 3
            elif state.name == "tired":
                modifiers["move_speed"] -= 2
                modifiers["combat_proficiency"] -= 2
                modifiers["general_proficiency"] -= 2
            elif state.name == "winded":
                modifiers["move_speed"] -= 1
                modifiers["combat_proficiency"] -= 1
                modifiers["general_proficiency"] -= 1

        return modifiers

    def apply_injuries_as_states(self):
        """
        Create states based on the current injuries and add them to the character's states
        with appropriate names and durations.
        """
        injuries = self.body.get_injuries()

        for injury_type, count in injuries.items():
            if injury_type == InjuryType.CONCUSSION:
                # Apply blackout state if 4 or more concussions are present
                if count >= 4 and not any(
                    state.name == "blacked_out" for state in self.states
                ):
                    self.add_state("blacked_out", 1)  # Blacked out for 1 round

            if injury_type == InjuryType.BLEED:
                # Apply bleeding state for each stack of bleeding
                bleeding_state_exists = any(
                    state.name == "bleeding" for state in self.states
                )
                if not bleeding_state_exists:
                    self.add_state("bleeding", -1)  # Indefinite duration until healed

            if injury_type == InjuryType.MALFUNCTION:
                # Apply malfunction state for each stack
                self.add_state("malfunction", -1)

            if injury_type == InjuryType.SHOCK:
                # Apply shock state for each stack
                self.add_state("shocked", -1)

            if injury_type == InjuryType.DISABLE:
                # Apply disable state for each stack
                self.add_state("disabled", -1)

            if injury_type == InjuryType.IMMOBILIZE:
                # Apply immobilize state for each stack
                self.add_state("immobilized", -1)

    def check_ap_stamina_penalty(self):
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
        Check the character's stamina and apply states if necessary.
        """
        if self.stamina == 0:
            # If character is blacked-out, create a blacked-out state that lasts for 1 round
            self.states.append(State("blacked_out", 1))
            self.log_event(
                description=f"Character is blacked-out ({self.stamina} stamina).",
            )

        elif self.stamina == 1:
            # If character is fatigued, create a fatigued state
            self.states.append(State("fatigued", -1))  # Duration -1 for indefinite
            self.log_event(
                description=f"Character is fatigued ({self.stamina} stamina).",
            )

        elif self.stamina <= 3:
            # If character is tired, create a tired state
            self.states.append(State("tired", -1))  # Duration -1 for indefinite
            self.log_event(
                description=f"Character is tired ({self.stamina} stamina).",
            )

        elif self.stamina <= 5:
            # If character is winded, create a winded state
            self.states.append(State("winded", -1))  # Duration -1 for indefinite
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

    def check_is_dead(self):
        """
        Check if the character is dead, i.e., total hit points are zero or less.
        """
        self.is_dead = self.total_hit_points <= 0

        if self.is_dead:
            self.log_event(
                description=f"Character is dead ({self.total_hit_points} HP).",
            )

        return self.is_dead
