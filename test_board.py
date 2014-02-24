import unittest
import mock

from board import *

class TestBoard(unittest.TestCase):
    def test_has_grid_like_coordinates(self):
        board = Board()
        board[0, 0] = 'X'
        self.assertEqual('X', board[0, 0])
