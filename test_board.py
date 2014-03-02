import unittest
from mock import Mock

from board import *

class TestBoard(unittest.TestCase):
    def test_has_grid_like_coordinates(self):
        board = Board()
        board[0, 0] = 'X'
        self.assertEqual('X', board[0, 0])

    def test_can_return_rows(self):
        board = make_board('abcdefghi')

        self.assertEqual(['a', 'b', 'c'], board.row(0))
        self.assertEqual(['d', 'e', 'f'], board.row(1))
        self.assertEqual(['g', 'h', 'i'], board.row(2))

    def test_can_return_columns(self):
        board = make_board('abcdefghi')

        self.assertEqual(['a', 'd', 'g'], board.column(0))
        self.assertEqual(['b', 'e', 'h'], board.column(1))
        self.assertEqual(['c', 'f', 'i'], board.column(2))

    def test_can_return_diagonals(self):
        board = make_board('abcdefghi')

        self.assertEqual(['a', 'e', 'i'], board.diagonal(0))
        self.assertEqual(['c', 'e', 'g'], board.diagonal(1))

    def test_knows_whether_its_full_or_not(self):
        unfinished_board = make_board('xo ooxoxo')
        finished_board = make_board('xoooxoxoo')

        self.assertFalse(unfinished_board.is_full())
        self.assertTrue(finished_board.is_full())

    def test_passes_itself_to_callback_when_value_gets_set(self):
        update_callback = Mock()
        board = Board(callback=update_callback)

        board[1, 1] = 'x'

        update_callback.assert_called_with(board)

    def test_rows_can_be_iterated(self):
        board = Board(rows=5)
        count = 0

        for row in board.rows():
            count += 1

        self.assertEqual(5, count)

    def test_columns_can_be_iterated(self):
        board = Board(columns=7)
        count = 0

        for column in board.columns():
            count += 1

        self.assertEqual(7, count)

    def test_translates_single_key_values_to_proper_indexes(self):
        board = Board()

        board[0] = 'o'
        board[1] = 'x'
        board[2] = 'o'
        board[3] = 'x'
        board[4] = 'o'
        board[5] = 'x'
        board[6] = 'o'
        board[7] = 'x'
        board[8] = 'o'

        self.assertEqual(board[0], board[0, 0])
        self.assertEqual(board[1], board[0, 1])
        self.assertEqual(board[2], board[0, 2])
        self.assertEqual(board[3], board[1, 0])
        self.assertEqual(board[4], board[1, 1])
        self.assertEqual(board[5], board[1, 2])
        self.assertEqual(board[6], board[2, 0])
        self.assertEqual(board[7], board[2, 1])
        self.assertEqual(board[8], board[2, 2])

    def test_placed_values_cannot_be_overwritten(self):
        board = Board()
        board[0, 0] = 'x'

        try:
            board[0, 0] = 'o'
            self.fail('Expected exception was not thrown')
        except UnallowedMove:
            pass


class TestBoardMaker(unittest.TestCase):
    def test_creates_boards_from_string(self):
        board = make_board('xoooxooox')

        self.assertEqual('x', board[0, 0])
        self.assertEqual('o', board[0, 1])
        self.assertEqual('o', board[0, 2])
        self.assertEqual('o', board[1, 0])
        self.assertEqual('x', board[1, 1])
        self.assertEqual('o', board[1, 2])
        self.assertEqual('o', board[2, 0])
        self.assertEqual('o', board[2, 1])
        self.assertEqual('x', board[2, 2])
