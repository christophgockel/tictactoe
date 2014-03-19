from unittest import TestCase
from mock import Mock

from ai import AutomaticInput
from board import make_board


class TestAutomaticInput(TestCase):
    def test_gathers_available_moves(self):
        ai = AutomaticInput('x')

        moves = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
        self.assertEqual(moves, ai.available_moves(make_board('         ')))

        moves = [(0, 2), (1, 1), (2, 0)]
        self.assertEqual(moves, ai.available_moves(make_board('ox x o ox')))

    def test_blocks_possible_wins(self):
        ai = AutomaticInput('o')

        self.assertEqual(0, ai.next_move('o', make_board(' xx      ')))
        self.assertEqual(0, ai.next_move('o', make_board('   x  x  ')))
        self.assertEqual(0, ai.next_move('o', make_board('    x   x')))

        self.assertEqual(1, ai.next_move('o', make_board('x x      ')))
        self.assertEqual(1, ai.next_move('o', make_board('    x  x ')))

        self.assertEqual(2, ai.next_move('o', make_board('    x x  ')))
        self.assertEqual(2, ai.next_move('o', make_board('xx       ')))
        self.assertEqual(2, ai.next_move('o', make_board('     x  x')))

        self.assertEqual(3, ai.next_move('o', make_board('    xx   ')))
        self.assertEqual(3, ai.next_move('o', make_board('x     x  ')))

        self.assertEqual(4, ai.next_move('o', make_board('   x x   ')))
        self.assertEqual(4, ai.next_move('o', make_board(' x     x ')))
        self.assertEqual(4, ai.next_move('o', make_board('  x   x  ')))
        self.assertEqual(4, ai.next_move('o', make_board('x       x')))

        self.assertEqual(5, ai.next_move('o', make_board('  x     x')))
        self.assertEqual(5, ai.next_move('o', make_board('   xx    ')))

        self.assertEqual(6, ai.next_move('o', make_board('x  x     ')))
        self.assertEqual(6, ai.next_move('o', make_board('       xx')))
        self.assertEqual(6, ai.next_move('o', make_board('  x x    ')))

        self.assertEqual(7, ai.next_move('o', make_board('      x x')))
        self.assertEqual(7, ai.next_move('o', make_board(' x  x    ')))

        self.assertEqual(8, ai.next_move('o', make_board('      xx ')))
        self.assertEqual(8, ai.next_move('o', make_board('  x  x   ')))
        self.assertEqual(8, ai.next_move('o', make_board('x   x    ')))

    def test_can_block_wins_for_x(self):
        ai = AutomaticInput('o')
        self.assertEqual(0, ai.next_move('o', make_board(' xx      ')))

    def test_can_block_wins_for_o(self):
        ai = AutomaticInput('x')
        self.assertEqual(0, ai.next_move('x', make_board(' oo      ')))
