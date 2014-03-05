import sys
from copy import deepcopy
from collections import namedtuple

from game import GameState, Rules
from player import Player


Move = namedtuple('Move', 'score coordinates')

class AutomaticInput(object):
    def __init__(self, symbol):
        self._symbol = symbol
        
        if self._symbol == Player.X:
            self._opponent = Player.O
        else:
            self._opponent = Player.X

    def next_move(self, symbol, board):
        return self._best_move(board)

    def _best_move(self, board):
        move = self._maximize(board, -sys.maxint - 1, sys.maxint)

        return self._linearize_coordinates(move.coordinates)

    def _linearize_coordinates(self, coordinates):
        return (coordinates[0] * 3) + coordinates[1]
    
    def _maximize(self, board, alpha, beta):
        moves = self.available_moves(board)
        best_move = (-1, -1)

        if self._board_has_final_state(board):
            return Move(score=self._score(board), coordinates=best_move)

        for move in moves:
            new_board = deepcopy(board)
            new_board[move] = self._symbol

            moved = self._minimize(new_board, alpha, beta)

            if moved.score > alpha:
                alpha = moved.score
                best_move = move

            if alpha >= beta:
                break

        return Move(score=alpha, coordinates=best_move)

    def _minimize(self, board, alpha, beta):
        moves = self.available_moves(board)
        best_move = (-1, -1)

        if self._board_has_final_state(board):
            return Move(score=self._score(board), coordinates=best_move)

        for move in moves:
            new_board = deepcopy(board)
            new_board[move] = self._opponent

            moved = self._maximize(new_board, alpha, beta)

            if moved.score < beta:
                beta = moved.score
                best_move = move

            if alpha >= beta:
                break

        return Move(score=beta, coordinates=best_move)

    def available_moves(self, board):
        moves = []

        for row, row_content in enumerate(board.rows()):
            cols = [(row, column) for column, cell in enumerate(row_content) if cell is None]
            moves += cols

        return moves

    def _board_has_final_state(self, board):
        rules = Rules()
        return rules.finished(board)
    
    def _score(self, board):
        rules = Rules()

        state = rules.game_state(board)

        if state == GameState.tie:
            return 0
        elif state == GameState.winner_x:
            if self._symbol == Player.X:
                return 1
            else:
                return -1
        else:
            if self._symbol == Player.X:
                return -1
            else:
                return 1
