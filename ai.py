from copy import deepcopy
from collections import namedtuple

from game import GameState, Rules
from player import Player


RatedMove = namedtuple('Move', 'score coordinates')

class AutomaticInput(object):
    def next_move(self, symbol, board):
        self._symbol = symbol

        return self._best_move(board)

    def _best_move(self, board):
        move = self._negamax(board, -1, 1, self._symbol)

        return self._linearize_coordinates(move.coordinates)

    def _linearize_coordinates(self, coordinates):
        return (coordinates[0] * 3) + coordinates[1]

    def _negamax(self, board, alpha, beta, symbol):
        opponent = self._opponent_of(symbol)
        best_move = (-1, -1)
        best_score = -1

        if self._board_has_final_state(board):
            return RatedMove(score=self._score(board, symbol), coordinates=best_move)

        for move in self.available_moves(board):
            new_board = deepcopy(board)
            new_board[move] = symbol

            score = -self._negamax(new_board, -beta, -alpha, opponent).score

            if score > best_score:
                best_score = score
                best_move = move

            if score > alpha:
                alpha = score

            if self._move_is_uninteresting(alpha, beta):
                break

        return RatedMove(score=best_score, coordinates=best_move)

    def _opponent_of(self, symbol):
        if symbol == Player.X:
            return Player.O

        return Player.X

    def _move_is_uninteresting(self, alpha, beta):
        return alpha >= beta

    def available_moves(self, board):
        moves = []

        for row, row_content in enumerate(board.rows()):
            cols = [(row, column) for column, cell in enumerate(row_content) if cell is None]
            moves += cols

        return moves

    def _board_has_final_state(self, board):
        rules = Rules()
        return rules.finished(board)
    
    def _score(self, board, symbol):
        rules = Rules()

        state = rules.game_state(board)
        moves = sum(1 for row in board.rows() for cell in row if cell)

        if state == GameState.tie:
            return 0
        elif state == GameState.winner_x:
            if symbol == Player.X:
                return 1.0 / moves
            else:
                return -1.0 / moves
        else:
            if symbol == Player.X:
                return -1.0 / moves
            else:
                return 1.0 / moves
