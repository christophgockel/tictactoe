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

    def test_cannot_run_when_not_enough_players(self):
        game = Game()

        self.assertRaises(TooFewPlayers, game.run)

    def test_asks_the_rules_if_enough_players_available(self):
        rules = Rules()
        rules.finished = Mock(return_value=True)
        rules.enough_players = Mock(return_value=True)

        game = Game()
        game.new_rules(rules)
        game.add_player(self.player_o)
        game.add_player(self.player_x)

        game.run()

        rules.enough_players.assert_called_with([self.player_o, self.player_x])

    def test_game_runs_until_finished(self):
        rules = Rules()
        rules.enough_players = Mock(return_value=True)
        rules.finished = Mock(side_effect=[False, True])

        game = Game()
        game.new_rules(rules)
        game.add_player(self.player_x)
        game.add_player(self.player_o)
        game.run()

        self.assertEqual(2, rules.finished.call_count)

    def test_when_game_runs_players_get_asked_for_their_next_moves(self):
        rules = Rules()
        rules.enough_players = Mock(return_value=True)
        rules.finished = Mock(side_effect=[False, False, True])
        self.player_x.next_move = Mock(return_value=0)
        self.player_o.next_move = Mock(return_value=1)

        game = Game()
        game.new_rules(rules)
        game.add_player(self.player_x)
        game.add_player(self.player_o)

        game.run()

        self.assertEqual(1, self.player_x.next_move.call_count)
        self.assertEqual(1, self.player_o.next_move.call_count)

    def test_full_game_cycle_tie(self):
        self.player_x.next_move = Mock(side_effect=[0,1,5,6,8])
        self.player_o.next_move = Mock(side_effect=[2,3,4,7])

        game = Game()
        game.add_player(self.player_x)
        game.add_player(self.player_o)

        self.assertEqual(GameState.tie, game.run())

    def test_full_game_cycle_winner_x(self):
        self.player_x.next_move = Mock(side_effect=[0,4,8])
        self.player_o.next_move = Mock(side_effect=[1,2])

        game = Game()
        game.add_player(self.player_x)
        game.add_player(self.player_o)

        self.assertEqual(GameState.winner_x, game.run())

    def test_full_game_cycle_winner_o(self):
        self.player_x.next_move = Mock(side_effect=[1,2])
        self.player_o.next_move = Mock(side_effect=[0,4,8])

        game = Game()
        game.add_player(self.player_o)
        game.add_player(self.player_x)

        self.assertEqual(GameState.winner_o, game.run())

    def test_players_are_asked_again_for_next_move_if_cell_is_already_occupied(self):
        rules = Rules()
        rules.finished = Mock(side_effect=[False, False, True])

        self.player_x.next_move = Mock(side_effect=[1])
        self.player_o.next_move = Mock(side_effect=[1,0])

        game = Game()
        game.new_rules(rules)
        game.add_player(self.player_x)
        game.add_player(self.player_o)

        game.run()

        self.assertEqual(2, self.player_o.next_move.call_count)

    def test_when_cell_is_already_occupied_a_corresponding_message_will_be_presented(self):
        display = Mock()
        rules = Rules()
        rules.finished = Mock(side_effect=[False, False, True])

        self.player_x.next_move = Mock(side_effect=[1])
        self.player_o.next_move = Mock(side_effect=[1,0])

        game = Game(display=display)
        game.new_rules(rules)
        game.add_player(self.player_x)
        game.add_player(self.player_o)

        game.run()

        self.assertEqual(1, display.show_illegal_move_warning.call_count)

    def test_displays_the_board_state_for_every_round_played_and_when_finished(self):
        display = Mock()
        rules = Rules()
        rules.enough_players = Mock(return_value=True)
        rules.finished = Mock(side_effect=[False, False, True])

        self.player_x.next_move = Mock(side_effect=[1])
        self.player_o.next_move = Mock(side_effect=[2])

        game = Game(display=display)
        game.new_rules(rules)
        game.add_player(self.player_x)
        game.add_player(self.player_o)

        game.run()

        self.assertEqual(3, display.show_board_state.call_count)


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
