import unittest
from mock import Mock

from game import *
from board import *
from player import *


class TestGame(unittest.TestCase):
    def setUp(self):
        self.player_x = Player('x')
        self.player_x.next_move = Mock(return_value=0)

        self.player_o = Player('o')
        self.player_o.next_move = Mock(return_value=1)

        self.rules = Rules()
        self.display = Mock()
        self.game = Game(display=self.display)

        self.game.new_rules(self.rules)
        self.game.add_player(self.player_x)
        self.game.add_player(self.player_o)

    def test_cannot_run_when_not_enough_players(self):
        self.assertRaises(TooFewPlayers, Game().run)

    def test_asks_the_rules_if_enough_players_available(self):
        self.rules.finished = Mock(return_value=True)
        self.rules.enough_players = Mock(return_value=True)

        self.game.run()

        self.rules.enough_players.assert_called_with([self.player_x, self.player_o])

    def test_game_runs_until_finished(self):
        self.rules.enough_players = Mock(return_value=True)
        self.rules.finished = Mock(side_effect=[False, True])

        self.game.run()

        self.assertEqual(2, self.rules.finished.call_count)

    def test_when_game_runs_players_get_asked_for_their_next_moves(self):
        self.rules.enough_players = Mock(return_value=True)
        self.rules.finished = Mock(side_effect=[False, False, True])
        self.player_x.next_move = Mock(return_value=0)
        self.player_o.next_move = Mock(return_value=1)

        self.game.run()

        self.assertEqual(1, self.player_x.next_move.call_count)
        self.assertEqual(1, self.player_o.next_move.call_count)

    def test_full_game_cycle_tie(self):
        self.player_x.next_move = Mock(side_effect=[0,1,5,6,8])
        self.player_o.next_move = Mock(side_effect=[2,3,4,7])

        self.assertEqual(GameState.tie, self.game.run())

    def test_full_game_cycle_winner_x(self):
        self.player_x.next_move = Mock(side_effect=[0,4,8])
        self.player_o.next_move = Mock(side_effect=[1,2])

        self.assertEqual(GameState.winner_x, self.game.run())

    def test_full_game_cycle_winner_o(self):
        self.player_x.next_move = Mock(side_effect=[1,2])
        self.player_o.next_move = Mock(side_effect=[0,4,8])

        game = Game()
        game.add_player(self.player_o)
        game.add_player(self.player_x)

        self.assertEqual(GameState.winner_o, game.run())

    def test_players_are_asked_again_for_next_move_if_cell_is_already_occupied(self):
        self.rules.finished = Mock(side_effect=[False, False, True])

        self.player_x.next_move = Mock(side_effect=[1])
        self.player_o.next_move = Mock(side_effect=[1,0])

        self.game.run()

        self.assertEqual(2, self.player_o.next_move.call_count)

    def test_when_cell_is_already_occupied_a_corresponding_message_will_be_presented(self):
        self.rules.finished = Mock(side_effect=[False, False, True])

        self.player_x.next_move = Mock(side_effect=[1])
        self.player_o.next_move = Mock(side_effect=[1,0])

        self.game.run()

        self.assertEqual(1, self.display.show_illegal_move_warning.call_count)

    def test_displays_the_board_state_for_every_round_played_and_when_finished(self):
        self.rules.enough_players = Mock(return_value=True)
        self.rules.finished = Mock(side_effect=[False, False, True])

        self.player_x.next_move = Mock(side_effect=[1])
        self.player_o.next_move = Mock(side_effect=[2])

        self.game.run()

        self.assertEqual(3, self.display.show_board_state.call_count)


class TestRules(unittest.TestCase):
    def test_needs_players(self):
        self.assertFalse(Rules().enough_players([]))

    def test_needs_more_than_one_player(self):
        self.assertFalse(Rules().enough_players([Mock()]))

    def test_two_players_are_enough(self):
        self.assertTrue(Rules().enough_players([Mock(), Mock()]))

    def test_game_is_not_finished_until_all_fields_are_filled(self):
        board = make_board('oxo xooox')
        self.assertFalse(Rules().finished(board))

    def test_unfinished_game_is_in_state_ongoing(self):
        self.assertEquals(GameState.ongoing, Rules().game_state(make_board('xoxoxoo  ')))

    def test_full_board_with_no_winner_is_in_state_tie(self):
        self.assertEquals(GameState.tie, Rules().game_state(make_board('xoxoxooxo')))

    def test_winning_column_combinations_for_x(self):
        self.assertEquals(GameState.winner_x, Rules().game_state(make_board('x  x  x  ')))
        self.assertEquals(GameState.winner_x, Rules().game_state(make_board(' x  x  x ')))
        self.assertEquals(GameState.winner_x, Rules().game_state(make_board('  x  x  x')))

    def test_winning_row_combinations_for_x(self):
        self.assertEquals(GameState.winner_x, Rules().game_state(make_board('xxx      ')))
        self.assertEquals(GameState.winner_x, Rules().game_state(make_board('   xxx   ')))
        self.assertEquals(GameState.winner_x, Rules().game_state(make_board('      xxx')))

    def test_winning_diagonal_combinations_for_x(self):
        self.assertEquals(GameState.winner_x, Rules().game_state(make_board('x   x   x')))
        self.assertEquals(GameState.winner_x, Rules().game_state(make_board('  x x x  ')))

    def test_winning_column_combinations_for_o(self):
        self.assertEquals(GameState.winner_o, Rules().game_state(make_board('o  o  o  ')))
        self.assertEquals(GameState.winner_o, Rules().game_state(make_board(' o  o  o ')))
        self.assertEquals(GameState.winner_o, Rules().game_state(make_board('  o  o  o')))

    def test_winning_row_combinations_for_o(self):
        self.assertEquals(GameState.winner_o, Rules().game_state(make_board('ooo      ')))
        self.assertEquals(GameState.winner_o, Rules().game_state(make_board('   ooo   ')))
        self.assertEquals(GameState.winner_o, Rules().game_state(make_board('      ooo')))

    def test_winning_diagonal_combinations_for_o(self):
        self.assertEquals(GameState.winner_o, Rules().game_state(make_board('o   o   o')))
        self.assertEquals(GameState.winner_o, Rules().game_state(make_board('  o o o  ')))
