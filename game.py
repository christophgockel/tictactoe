from board import Board


class GameState(object):
    ongoing  = 'ongoing'
    tie      = 'tie'
    winner_x = 'winner x'
    winner_o = 'winner o'


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
    def __init__(self, board=Board()):
        self.players = []
        self.rules = Rules()
        self.board = board
        self.current_player = None
        self.other_player = None

    def new_rules(self, rules):
        self.rules = rules

    def run(self):
        if self.rules.enough_players(self.players):
            self.prepare_players()

            while not self.rules.finished(self.board):
                move = self.current_player.next_move()
                self.board[0, move] = self.current_player.symbol

                self.switch_players()
        else:
            raise TooFewPlayers()
    
    def add_player(self, player):
        self.players.append(player)

    def state(self):
        return board.contents()

    def prepare_players(self):
        self.current_player = self.players[0]
        self.other_player = self.players[1]

    def switch_players(self):
        self.current_player, self.other_player = self.other_player, self.current_player


class TooFewPlayers(Exception):
    pass
