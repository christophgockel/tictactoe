from board import Board


class GameState(object):
    ongoing  = 0
    tie      = 1
    winner_x = 2
    winner_o = 3


class Rules(object):
    def enough_players(self, players):
        if len(players) == 2:
            return True
        else:
            return False

    def finished(self, board):
        return board.is_full()

    def game_state(self, board):
        if not board.is_full():
            return GameState.ongoing
        else:
            if self._x_has_three_in_a_row(board):
                return GameState.winner_x
            elif self._o_has_three_in_a_row(board):
                return GameState.winner_o
            else:
                return GameState.tie

    def _x_has_three_in_a_row(self, board):
        return self._has_three_in_a_row('x', board)

    def _o_has_three_in_a_row(self, board):
        return self._has_three_in_a_row('o', board)

    def _has_three_in_a_row(self, symbol, board):
        for column in range(3):
            if self._column_has_same_values(board, column):
                if board.column(column)[0] == symbol:
                    return True

        for row in range(3):
            if self._row_has_same_values(board, row):
                if board.row(row)[0] == symbol:
                    return True

        return False

    def _column_has_same_values(self, board, column):
        return board.column(column)[1:] == board.column(column)[:-1]

    def _row_has_same_values(self, board, row):
        return board.row(row)[1:] == board.row(row)[:-1]


class Game(object):
    def __init__(self, rules = Rules()):
        self.players = []
        self.rules = rules
        self.board = Board()

    def run(self):
        if self.rules.enough_players(self.players):
            while not self.rules.finished(self.board):
                pass
        else:
            raise TooFewPlayers()
    
    def add_player(self, player):
        self.players.append(player)

    def state(self):
        return board.contents()


class TooFewPlayers(Exception):
    pass
