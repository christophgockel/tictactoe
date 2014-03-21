from collections import namedtuple

from game import *
from board import make_board
from player import *
from ai import AutomaticInput


Players = namedtuple('Players', 'human computer')


class TerminalInput(object):
    def next_move(self, player_symbol, board):
        while True:
            try:
                move = self._get_move_for(player_symbol)

                if move >= 1 and move <= 9:
                    return move - 1
                else:
                    print 'Move has to be between 1 and 9. Please try again.'
            except ValueError:
               print 'Not a valid move. Please try again.'

    def _get_move_for(self, player_symbol):
        input = raw_input('Next move for {0}: '.format(player_symbol))

        return int(input)


class TerminalDisplay(object):
    def __init__(self, display_indices=False):
        self._display_indices = display_indices

    def show_board_state(self, board):
        for index, row in enumerate(board.rows()):
            row_content = self._format_row_content(index, row)

            print row_content

            if index < board.row_count() - 1:
                print '-' * len(row_content)

        print

    def _format_row_content(self, index, row):
        cells = [self._format_cell(index, row, cell_index) if cell is None else cell
                 for cell_index, cell in enumerate(row)]
        formatted_row = '  |  '.join(cells)

        return ' ' + formatted_row + ' '

    def _format_cell(self, row_index, row, cell_index):
        if self._display_indices:
            return str(row_index * len(row) + cell_index + 1)
        else:
            return ' '


    def show_illegal_move_warning(self):
        print 'Error: Move not allowed. Please provide another coordinate.'


def print_introduction():
    print 'Play using the following coordinates:'
    print_board_coordinates()


def create_players(player_symbol):
    if player_symbol == 'x':
        return Players(human=PlayerX(TerminalInput()), computer=PlayerO(AutomaticInput()))
    elif player_symbol == 'o':
        return Players(human=PlayerO(TerminalInput()), computer=PlayerX(AutomaticInput()))


def get_symbol_for_human_player():
    while True:
        choice = raw_input('Which player do you want to be? (x or o): ').lower()

        if choice == 'x' or choice == 'o':
            break

        print 'Invalid choice'

    return choice


def sort_for_first_turn(order, players):
    if order == '':
        return players.human, players.computer
    else:
        return players.computer, players.human


def get_symbol_for_first_turn():
    print 'Who makes the first turn?'
    return raw_input('(No value = you, everything else = computer) ').strip()

def get_indices_option():
    print 'Would you like having the board indices displayed while playing?'
    return raw_input('(No value = no, everything else = yes) ').strip()

def print_board_coordinates():
    TerminalDisplay().show_board_state(make_board('123456789'))


def print_outcome(outcome):
    if outcome == GameState.tie:
        print 'This game ended in a tie.'
    elif outcome == GameState.winner_x:
        print 'Player x is the winner.'
    elif outcome == GameState.winner_o:
        print 'Player o is the winner.'
    else:
        print 'Unknown outcome {0}.'.format(outcome)
    print


def player_is_done():
    print 'Play another round?'
    input = raw_input('If not, please enter "no", everything else means "yes": ')

    if input.lower() == 'no':
        return True

    return False


try:
    print_introduction()

    symbol = get_symbol_for_human_player()
    players = create_players(player_symbol=symbol)

    symbol_for_first_turn = get_symbol_for_first_turn()
    players = sort_for_first_turn(symbol_for_first_turn, players)

    display_indices = get_indices_option()

    while True:
        game = Game(display=TerminalDisplay(display_indices))
        game.add_player(players[0])
        game.add_player(players[1])

        outcome = game.run()
        print_outcome(outcome)

        if player_is_done():
            break
except KeyboardInterrupt:
    pass
