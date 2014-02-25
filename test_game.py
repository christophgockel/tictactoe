import unittest
from mock import Mock

from game import *
from board import *


class TestGame(unittest.TestCase):
    def test_cannot_run_when_not_enough_players(self):
        game = Game()

        self.assertRaises(TooFewPlayers, game.run)

    def test_asks_the_rules_if_enough_players_available(self):
        rules = Rules()
        rules.finished = Mock(return_value=True)
        rules.enough_players = Mock(return_value=True)

        game = Game(rules)
        player_o = Mock()
        player_x = Mock()
        game.add_player(player_o)
        game.add_player(player_x)

        game.run()

        rules.enough_players.assert_called_with([player_o, player_x])

    def test_game_runs_until_finished(self):
        rules = Rules()
        rules.enough_players = Mock(return_value=True)
        rules.finished = Mock(side_effect=[False, True])

        game = Game(rules)
        game.run()

        self.assertEqual(2, rules.finished.call_count)


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
