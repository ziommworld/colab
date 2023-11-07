import pandas as pd

class Game:
    def __init__(self):
        self.game_state = 'unknown'  # Game state can be 'unknown', 'draft', or 'active'
        self.characters = []         # Characters array
        self.current_idx = 0         # Index of character currently on initiative

    def add_character(self, character):
        """
        Adds a character to the game, inserting into the characters array depending on initiative score.
        Character is expected to be a dictionary with at least 'name' and 'initiative' keys.
        """
        self.characters.append(character)
        self.characters.sort(key=lambda x: x['initiative'], reverse=True)

    def start_game(self):
        """Changes the game state to active and starts the game."""
        self.game_state = 'active'

    def save_game(self):
        """
        Saves the game state to a pandas dataframe.
        Placeholder for storing dataframe in the cloud.
        """
        game_data = {
            'game_state': self.game_state,
            'characters': [char['name'] for char in self.characters],
            'initiatives': [char['initiative'] for char in self.characters],
            'current_idx': self.current_idx
        }
        df = pd.DataFrame(game_data)
        # Placeholder for cloud storage code
        # e.g., df.to_csv('cloud_storage_path.csv')
        return df

    def load_game(self, df):
        """
        Restores the game state from a pandas dataframe object.
        """
        self.game_state = df['game_state'][0]
        self.current_idx = df['current_idx'][0]
        self.characters = [{'name': row['characters'], 'initiative': row['initiatives']}
                           for _, row in df.iterrows()]

    def end_game(self):
        """
        Ends the game, updating the game state and creating stats to append to the saved dataframe.
        """
        self.game_state = 'draft'  # Assuming 'draft' signifies a completed game ready for review
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
