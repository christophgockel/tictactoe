from unittest import TestCase
from mock import Mock

from player import Player, PlayerO, PlayerX
from board import make_board

class TestPlayer(TestCase):
    def test_player_has_symbol(self):
        o = Player(Player.O)
        x = Player(Player.X)

        self.assertEqual(Player.O, o.symbol)
        self.assertEqual(Player.X, x.symbol)

    def test_has_convenience_factory_functions(self):
        self.assertEqual(Player.O, PlayerO().symbol)
        self.assertEqual(Player.X, PlayerX().symbol)

    def test_can_provide_next_move_with_input_object(self):
        player_input = Mock()
        player_input.next_move = Mock(return_value=2)
        player = PlayerX(player_input)

        self.assertEqual(2, player.next_move())
        player_input.next_move.assert_called()

    def test_player_inputs_next_move_is_called_with_players_symbol_and_current_board(self):
        board = Mock()
        player_input = Mock()
        player_input.next_move = Mock(return_value=2)
        player = PlayerX(player_input)

        self.assertEqual(2, player.next_move(board))
        player_input.next_move.assert_called_with(player.symbol, board)
