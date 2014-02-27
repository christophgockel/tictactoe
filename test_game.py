import unittest
from mock import Mock

from game import *
from board import *
from player import *


class TestGame(unittest.TestCase):
    def setUp(self):
        self.player_x = Player('x', Mock(return_value=0))
        self.player_o = Player('o', Mock(return_value=1))

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
        self.assertEquals(GameState.ongoing, Rules().game_state(make_board('xoxoxox  ')))

    def test_finished_game_with_no_winner_is_in_state_tie(self):
        self.assertEquals(GameState.tie, Rules().game_state(make_board('xoxoxoxox')))

    def test_finished_game_with_x_as_winner_is_in_state_winner_x(self):
        self.assertEquals(GameState.winner_x, Rules().game_state(make_board('xoxxoxxxo')))
        self.assertEquals(GameState.winner_x, Rules().game_state(make_board('xxooxxoxo')))
        self.assertEquals(GameState.winner_x, Rules().game_state(make_board('xoxxoxoox')))

        self.assertEquals(GameState.winner_x, Rules().game_state(make_board('xxxoooooo')))
        self.assertEquals(GameState.winner_x, Rules().game_state(make_board('oooxxxooo')))
        self.assertEquals(GameState.winner_x, Rules().game_state(make_board('ooooooxxx')))

    def test_finished_game_with_o_as_winner_is_in_state_winner_o(self):
        self.assertEquals(GameState.winner_o, Rules().game_state(make_board('oxooxooox')))
        self.assertEquals(GameState.winner_o, Rules().game_state(make_board('xooxoxoox')))
        self.assertEquals(GameState.winner_o, Rules().game_state(make_board('xxooxoxoo')))

        self.assertEquals(GameState.winner_o, Rules().game_state(make_board('oooxoxoxo')))
        self.assertEquals(GameState.winner_o, Rules().game_state(make_board('oxooooxox')))
        self.assertEquals(GameState.winner_o, Rules().game_state(make_board('oxoxoxooo')))
