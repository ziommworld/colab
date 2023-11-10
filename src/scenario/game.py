from datetime import datetime
import pandas as pd
import random
import gspread
from google.auth import default

from src.character import Character


class Game:
    def __init__(self, sheet_name=None):
        self.init_google_sheets(sheet_name)

        self.game_phase = "unknown"  # game state can be 'unknown', 'draft', or 'active'
        self.game_state = {}
        self.game_map = {}
        self.game_matrix = None  # game_map in dataframe form
        self.game_storage = None  # game_state in dataframe form
        self.characters = []  # characters array sorted by initiative
        self.current_idx = 0  # index of character currently on initiative
        self.character_map = {}  # map from character id to character object

        try:
            self.load_game()
        except:  # Handle exceptions if the worksheet is empty or not properly formatted
            pass
        
    def init_google_sheets(self, sheet_name=f"game_{datetime.now().strftime("%Y%m%d%H%M%S")}"):
        # Initialize gspread client and open the sheet
        self.online = True
        try:
            credentials, _ = default()
        except:
            self.online = False
            
        if self.online:
            self.client = gspread.authorize(credentials)
            self.sheet_name = sheet_name
            self.spreadsheet = self.client.open(self.sheet_name)
            try:
                self.game_storage_worksheet = self.spreadsheet.worksheet("game_state")
            except gspread.WorksheetNotFound:
                self.game_storage_worksheet = self.spreadsheet.add_worksheet(
                    "game_state", rows="681", cols="420"
                )
        else:
            pass  # Placeholder for offline storage
            
    def encode_game_state(self):
        # Convert the game state into a dictionary that is compatible with pandas DataFrame
        game_data = {
            "game_phase": [self.game_phase],
            "current_idx": [self.current_idx],
            "characters": [[char.to_dict() for char in self.characters]]  # Convert each character to a dictionary
        }
        return pd.DataFrame(game_data)

    def decode_game_state(self, df):
        # Convert the DataFrame back into the game state
        self.game_phase = df["game_phase"][0]
        self.current_idx = df["current_idx"][0]
        self.characters = [Character(char_config) for char_config in df["characters"][0]]

    def save_game(self):
        df = self.encode_game_state()
        """Sets a dataframe into a worksheet from google sheet"""
        spreadsheet = self.client.open(self.sheet_name)
        worksheet = spreadsheet.worksheet(worksheet)
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())

    def load_game(self):
        # Load data from the worksheet into a pandas DataFrame
        data = self.worksheet.get_all_records()
        df = pd.DataFrame(data)
        if not df.empty:
            self.decode_game_state(df)

    def add_character(self, character_config):
        """
        Adds a character to the game, initializing their entry in character_map.
        """
        character = Character(character_config)
        self.character_map[character.id] = character
        self.characters.append(character)

    def set_character_order(self, character_order=None):
        """
        Set character order manually or roll for initiative if not provided.
        `character_order` is an optional list of character IDs defining the order.
        """
        if character_order:
            # Set characters based on the provided order
            self.characters = [
                self.character_map[char_id] for char_id in character_order
            ]
        else:
            # Automatically roll for initiative and resolve ties
            self.roll_initiative()

    def roll_initiative(self):
        """
        Roll initiative for all characters and resolve any ties.
        """
        initiative_rolls = {}

        # Roll initiative for each character
        for char_id, char in self.character_map.items():
            total_initiative = random.randint(1, 20) + char.get("composure", 0)
            char["initiative"] = total_initiative
            if total_initiative in initiative_rolls:
                initiative_rolls[total_initiative].append(char_id)
            else:
                initiative_rolls[total_initiative] = [char_id]

        # Resolve ties
        self.resolve_ties(initiative_rolls)

        # Flatten initiative rolls into a sorted list
        sorted_initiatives = sorted(initiative_rolls.keys(), reverse=True)
        self.characters = [
            self.character_map[char_id]
            for initiative in sorted_initiatives
            for char_id in initiative_rolls[initiative]
        ]

    def resolve_ties(self, initiative_rolls):
        """
        If there are ties, reroll until the ties are resolved.
        """
        reroll_needed = True
        while reroll_needed:
            reroll_needed = False
            for initiative_score, char_ids in list(initiative_rolls.items()):
                if len(char_ids) > 1:
                    reroll_needed = True
                    rerolls = {}
                    for char_id in char_ids:
                        reroll = random.randint(1, 20) + self.character_map[
                            char_id
                        ].get("composure", 0)
                        if reroll in rerolls:
                            rerolls[reroll].append(char_id)
                        else:
                            rerolls[reroll] = [char_id]

                    # Merge rerolls back into initiative_rolls, potentially creating new ties
                    initiative_rolls[initiative_score] = []  # Clear the current tie
                    for reroll_score, reroll_char_ids in rerolls.items():
                        if reroll_score in initiative_rolls:
                            initiative_rolls[reroll_score].extend(reroll_char_ids)
                        else:
                            initiative_rolls[reroll_score] = reroll_char_ids

                    # Remove empty lists from initiative_rolls
                    initiative_rolls = {k: v for k, v in initiative_rolls.items() if v}

    def start_game(self):
        """Changes the game state to active and starts the game."""
        self.game_phase = "active"

    def save_game(self):
        """
        Saves the game state to a pandas dataframe.
        Placeholder for storing dataframe in the cloud.
        """
        game_data = {
            "game_state": self.game_phase,
            "characters": [char.character_name for char in self.characters],
            "current_idx": self.current_idx,
        }
        df = pd.DataFrame(game_data)
        # Placeholder for cloud storage code
        # e.g., df.to_csv('cloud_storage_path.csv')
        return df

    def load_game(self, df):
        """
        Restores the game state from a pandas dataframe object.
        """
        self.game_phase = df["game_state"][0]
        self.current_idx = df["current_idx"][0]
        self.characters = [
            Character(character_config) for _, character_config in df.iterrows()
        ]

    def end_game(self):
        """
        Ends the game, updating the game state and creating stats to append to the saved dataframe.
        """
        self.game_phase = (
            "draft"  # Assuming 'draft' signifies a completed game ready for review
        )
        self.save_game()

    def play_action(self, config):
        """
        Performs an action with the character that is currently on initiative.
        Calls save_game() at the end of each action.
        """
        # Implementation of the action depends on what 'config' contains
        # Placeholder for action logic

        # After action logic, save the game state
        self.save_game()

    def end_turn(self):
        """Ends the turn for the character on the initiative in the current round."""
        self.current_idx = (self.current_idx + 1) % len(self.characters)

    def end_round(self):
        """Called automatically by the next action if all players have played, resets the counter."""
        if self.current_idx == len(self.characters) - 1:
            self.end_turn()  # This will reset the counter to 0
            # Additional logic for ending the round can be implemented here
