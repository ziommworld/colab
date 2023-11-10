import unittest

from src.scenario.game import Game


class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.add_character({'character_name': 'Warrior', 'initiative_score': 15})
        self.game.add_character({'character_name': 'Mage', 'initiative_score': 10})
    
    def test_add_character(self):
        # Ensure that characters are added and sorted correctly
        self.assertEqual(len(self.game.characters), 2)
        self.assertEqual(self.game.characters[0].character_name, 'Warrior')
        self.assertEqual(self.game.characters[1].character_name, 'Mage')

    def test_game_state_on_start(self):
        # Check if the game state is set to 'active' on start
        self.game.start_game()
        self.assertEqual(self.game.game_phase, 'active')
    
    def test_save_and_load_game(self):
        # Test saving and loading game functionality
        self.game.start_game()
        saved_df = self.game.save_game()
        self.game.game_phase = 'unknown'  # Change state to test loading function
        
        self.game.load_game(saved_df)
        self.assertEqual(self.game.game_phase, 'active')
        self.assertEqual(self.game.characters[0].character_name, 'Unknown')
    
    def test_end_game(self):
        # Test if ending the game updates the game state correctly
        self.game.end_game()
        self.assertEqual(self.game.game_phase, 'draft')
    
    def test_play_action(self):
        # Play an action and check if the game is saved (the game state remains 'active')
        self.game.start_game()
        self.game.play_action({'type': 'attack', 'target': 'Orc'})
        self.assertEqual(self.game.game_phase, 'active')

    def test_end_turn(self):
        # Test if ending the turn updates the current index correctly
        self.game.current_idx = 0  # Ensure the current index is 0
        self.game.end_turn()
        self.assertEqual(self.game.current_idx, 1)

    def test_end_round(self):
        # Test if ending the round resets the index when all characters have played
        self.game.current_idx = len(self.game.characters) - 1
        self.game.end_round()
        self.assertEqual(self.game.current_idx, 0)

if __name__ == '__main__':
    unittest.main()