from game import *
from board import make_board
from player import *


def user_input(player_symbol):
    while True:
       input = raw_input('Next move for {0}: '.format(player_symbol))
       try:
           move = int(input)

           if move >= 1 and move <= 9:
               return move - 1
           else:
               print 'Move has to be between 1 and 9. Please try again.'
       except ValueError:
           print 'Not a valid move. Please try again.'

def board_printer(board):
    index = 0
    for row in range(board.row_count()):
        row_content = ' | '.join([' ' if symbol is None else symbol for symbol in board.row(row)])
        print row_content

        if row < board.row_count() - 1:
            print '-' * len(row_content)

def print_introduction():
    print 'Tic Tac Toe'
    print 'Play using the following coordinates:'
    print_board_coordinates()

def print_board_coordinates():
    board_printer(make_board('123456789'))

def print_outcome(outcome):
    if outcome == GameState.tie:
        print 'This game ended in a tie.'
    elif outcome == GameState.winner_x:
        print 'Player x is the winner.'
    elif outcome == GameState.winner_o:
        print 'Player o is the winner.'
    else:
        print 'Unknown outcome {0}.'.format(outcome)

def player_is_done():
    print 'Play another round?'
    input = raw_input('If not, please enter "no", everything else means "yes": ')

    if input.lower() == 'no':
        return True

    return False


print_introduction()

try:
    while True:
        player_x = Player('x', user_input)
        player_o = Player('o', user_input)

        board = Board(callback=board_printer)
        game = Game(board=board)
        game.add_player(player_x)
        game.add_player(player_o)

        outcome = game.run()
        print_outcome(outcome)

        if player_is_done():
            break
        print_board_coordinates()
except KeyboardInterrupt:
    pass
