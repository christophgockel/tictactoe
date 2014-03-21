from board import Board, UnallowedMove
from player import Player


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
        return self.game_state(board) != GameState.ongoing

    def game_state(self, board):
        if self._x_has_three_in_a_row(board):
            return GameState.winner_x
        elif self._o_has_three_in_a_row(board):
            return GameState.winner_o
        elif board.is_full():
            return GameState.tie
        else:
            return GameState.ongoing

    def _x_has_three_in_a_row(self, board):
        return self._has_three_in_a_row(Player.X, board)

    def _o_has_three_in_a_row(self, board):
        return self._has_three_in_a_row(Player.O, board)

    def _has_three_in_a_row(self, symbol, board):
        if (self._any_column_has_same_values(symbol, board) or
                self._any_row_has_same_values(symbol, board) or
                self._any_diagonal_has_same_values(symbol, board)):
            return True

        return False

    def _any_column_has_same_values(self, symbol, board):
        for column in board.columns():
            if self._has_same_value(column, symbol):
                return True

        return False

    def _any_row_has_same_values(self, symbol, board):
        for row in board.rows():
            if self._has_same_value(row, symbol):
                return True

        return False

    def _any_diagonal_has_same_values(self, symbol, board):
        for diagonal in board.diagonals():
            if self._has_same_value(diagonal, symbol):
                return True

        return False

    def _has_same_value(self, values, value):
        return (values[0] == value) and (values[1:] == values[:-1])


class Game(object):
    def __init__(self, display=None):
        self.players = []
        self.rules = Rules()
        self.board = Board()
        self.display = display
        self.current_player = None
        self.other_player = None

    def new_rules(self, rules):
        self.rules = rules

    def run(self):
        if self._has_enough_players():
            self._prepare_players()
            self._play_game()
            self._display_board_content()

            return self._game_state()
        else:
            raise TooFewPlayers()

    def add_player(self, player):
        self.players.append(player)

    def _prepare_players(self):
        self.current_player = self.players[0]
        self.other_player = self.players[1]

    def _play_game(self):
        while self._is_not_finished():
            self._display_board_content()
            self._place_move_of_current_player()
            self._switch_players()

    def _has_enough_players(self):
        return self.rules.enough_players(self.players)

    def _is_not_finished(self):
        return not self.rules.finished(self.board)

    def _place_move_of_current_player(self):
        while True:
            try:
                move = self.current_player.next_move(self.board)
                self.board.set(move, self.current_player.symbol)
                break
            except UnallowedMove:
                self._display_illegal_move_warning()

    def _switch_players(self):
        self.current_player, self.other_player = self.other_player, self.current_player

    def _game_state(self):
        return self.rules.game_state(self.board)

    def _display_board_content(self):
        if self.display:
            self.display.show_board_state(self.board)

    def _display_illegal_move_warning(self):
        if self.display:
            self.display.show_illegal_move_warning()


class TooFewPlayers(Exception):
    pass
