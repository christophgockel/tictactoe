import unittest
from mock import Mock

from board import *

class TestBoard(unittest.TestCase):
    def test_new_board_is_empty(self):
        board = Board()
        self.assertTrue(board.is_empty())

    def test_after_placing_symbols_board_is_not_empty(self):
        board = Board()
        board.set(3, 'x')

        self.assertFalse(board.is_empty())

    def test_can_have_symbols_in_specific_locations(self):
        board = Board()
        board.set(0, 'x')
        self.assertEqual('x', board.get(0))

    def test_moves_can_be_undone(self):
        board = Board()
        board.set(2, 'x')
        board.unset(2)

        self.assertTrue(board.is_empty())

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

    def test_rows_can_be_iterated(self):
        board = Board()
        count = sum(1 for i in board.rows())

        self.assertEqual(3, count)

    def test_columns_can_be_iterated(self):
        board = Board()
        count = sum(1 for i in board.columns())

        self.assertEqual(3, count)

    def test_diagonals_can_be_iterated(self):
        board = Board()
        count = sum(1 for i in board.diagonals())

        self.assertEqual(2, count)

    def test_placed_values_cannot_be_overwritten(self):
        board = Board()
        board.set(0, 'x')

        try:
            board.set(0, 'o')
            self.fail('Expected exception was not thrown')
        except UnallowedMove:
            pass

    def test_on_new_board_all_cells_are_available(self):
        board = Board()

        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7, 8], board.available_locations())

    def test_provides_list_of_possible_locations(self):
        board = make_board('ox x o ox')

        self.assertEqual([2, 4, 6], board.available_locations())


class TestBoardMaker(unittest.TestCase):
    def test_creates_boards_from_string(self):
        board = make_board('012345678')

        self.assertEqual('0', board.get(0))
        self.assertEqual('1', board.get(1))
        self.assertEqual('2', board.get(2))
        self.assertEqual('3', board.get(3))
        self.assertEqual('4', board.get(4))
        self.assertEqual('5', board.get(5))
        self.assertEqual('6', board.get(6))
        self.assertEqual('7', board.get(7))
        self.assertEqual('8', board.get(8))
