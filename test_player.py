from unittest import TestCase
from mock import Mock

from player import Player, PlayerO, PlayerX, AutomaticInput
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


class TestAutomaticInput(TestCase):
    def test_gathers_available_moves(self):
        ai = AutomaticInput('x')

        moves = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
        self.assertEqual(moves, ai.available_moves(make_board('         ')))

        moves = [(0, 2), (1, 1), (2, 0)]
        self.assertEqual(moves, ai.available_moves(make_board('ox x o ox')))

    def test_blocks_possible_wins(self):
        ai = AutomaticInput('o')

        self.assertEqual(2, ai.next_move('o', make_board('    x x o')))
        self.assertEqual(2, ai.next_move('o', make_board('xx       ')))
        self.assertEqual(2, ai.next_move('o', make_board('   oox  x')))
