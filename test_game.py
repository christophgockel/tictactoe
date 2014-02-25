import unittest
from mock import Mock

from game import *


class TestGame(unittest.TestCase):
    def test_cannot_run_when_not_enough_players(self):
        game = Game()

        self.assertRaises(TooFewPlayers, game.run)

    def test_asks_the_rules_if_enough_players_available(self):
        rules = Rules()
        rules.enough_players = Mock(return_value=True)

        game = Game(rules)
        game.run()

        rules.enough_players.assert_called()


class TestRules(unittest.TestCase):
    def test_needs_players(self):
        self.assertFalse(Rules().enough_players([]))

    def test_needs_more_than_one_player(self):
        self.assertFalse(Rules().enough_players([Mock()]))

    def test_two_players_are_enough(self):
        self.assertTrue(Rules().enough_players([Mock(), Mock()]))
