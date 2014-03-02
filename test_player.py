import unittest
from mock import Mock

from player import Player

class TestPlayer(unittest.TestCase):
    def test_player_has_symbol(self):
        player = Player('o')

        self.assertEqual('o', player.symbol)

    def test_can_provide_next_move_with_input_object(self):
        player_input = Mock()
        player_input.next_move = Mock(return_value=2)
        player = Player('x', player_input)

        self.assertEqual(2, player.next_move())
        player_input.next_move.assert_called()

    def test_player_inputs_next_move_is_called_with_players_symbol_and_current_board(self):
        board = Mock()
        player_input = Mock()
        player_input.next_move = Mock(return_value=2)
        player = Player('x', player_input)

        self.assertEqual(2, player.next_move(board))
        player_input.next_move.assert_called_with('x', board)
