from game import *
from board import make_board
from player import *
from ai import AutomaticInput


class TerminalInput(object):
    def next_move(self, player_symbol, board):
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

class TerminalDisplay(object):
    def show_board_state(self, board):
        index = 0
        for row in range(board.row_count()):
            row_content = ' | '.join([' ' if symbol is None else symbol for symbol in board.row(row)])
            print row_content

            if row < board.row_count() - 1:
                print '-' * len(row_content)
        print

    def show_illegal_move_warning(self):
        print 'Error: Move not allowed. Please provide another coordinate.'

def print_introduction():
    print 'Play using the following coordinates:'
    print_board_coordinates()

def ask_for_player():
    while True:
        choice = raw_input('Which player do you want to be? (x or o): ')

        if choice.lower() == 'x':
            human = PlayerX(TerminalInput())
            computer = PlayerO(AutomaticInput(Player.O))
            break
        elif choice.lower() == 'o':
            human = PlayerO(TerminalInput())
            computer = PlayerX(AutomaticInput(Player.X))
            break
        else:
            print "Invalid"

    return human, computer

def ask_for_first_turn(human, computer):
    print 'Who makes the first turn?'
    choice = raw_input('(No value = you, everything else = computer) ')

    if choice.strip() == '':
        return human, computer
    else:
        return computer, human

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
    players = ask_for_first_turn(*ask_for_player())

    while True:
        game = Game(display=TerminalDisplay())
        game.add_player(players[0])
        game.add_player(players[1])

        outcome = game.run()
        print_outcome(outcome)

        if player_is_done():
            break

        print_board_coordinates()
except KeyboardInterrupt:
    pass
