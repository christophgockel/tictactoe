from collections import namedtuple

from game import GameState, Rules
from player import Player


RatedMove = namedtuple('RatedMove', 'score location')

class AutomaticInput(object):
    def next_move(self, symbol, board):
        self._symbol = symbol

        return self._best_move(board)

    def _best_move(self, board):
        move = self._negamax(board, -1, 1, self._symbol)

        return move.location

    def _negamax(self, board, alpha, beta, symbol):
        opponent = self._opponent_of(symbol)
        best_move = (-1, -1)
        best_score = -1

        if self._board_has_final_state(board):
            return RatedMove(score=self._score(board, symbol), location=best_move)

        for move in board.available_locations():
            board.set(move, symbol)
            score = -self._negamax(board, -beta, -alpha, opponent).score
            board.unset(move)

            if score > best_score:
                best_score = score
                best_move = move

            if score > alpha:
                alpha = score

            if self._move_is_uninteresting(alpha, beta):
                break

        return RatedMove(score=best_score, location=best_move)

    def _opponent_of(self, symbol):
        if symbol == Player.X:
            return Player.O

        return Player.X

    def _move_is_uninteresting(self, alpha, beta):
        return alpha >= beta

    def _board_has_final_state(self, board):
        rules = Rules()
        return rules.finished(board)
    
    def _score(self, board, symbol):
        rules = Rules()

        state = rules.game_state(board)
        move_count = sum(1 for row in board.rows() for cell in row if cell)

        if state == GameState.tie:
            return 0.0
        elif state == GameState.winner_x:
            if symbol == Player.X:
                return 1.0 / move_count
            else:
                return -1.0 / move_count
        else:
            if symbol == Player.X:
                return -1.0 / move_count
            else:
                return 1.0 / move_count
