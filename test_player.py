import unittest
from mock import Mock

from player import Player

class TestPlayer(unittest.TestCase):
    def test_player_has_symbol(self):
        player = Player('o')

        self.assertEqual('o', player.symbol)

    def test_can_provide_next_move_with_callback(self):
        callback = Mock(return_value=2)
        player = Player('x', callback)

        self.assertEqual(2, player.next_move())
        callback.assert_called()

    def test_next_move_callback_is_called_with_players_symbol(self):
        callback = Mock(return_value=2)
        player = Player('x', callback)

        self.assertEqual(2, player.next_move())
        callback.assert_called_with('x')
