from game import *
from player import *


def user_input(player_symbol):
    while True:
       input = raw_input('Next move for {0}:'.format(player_symbol))
       try:
           move = int(input)

           if move >= 0 and move <= 8:
               return move
           else:
               print 'Move has to be between 0 and 8. Please try again.'
       except ValueError:
           print 'Not a valid move. Please try again.'

def board_printer(board):
    index = 0
    for row in range(board.row_count()):
        row_content = ''

        for column in range(board.column_count()):
            symbol = board[row, column]
            if symbol is None:
                symbol = index
            row_content += '{0} '.format(symbol)
            index += 1

        print row_content

player_x = Player('x', user_input)
player_o = Player('o', user_input)

board = Board(callback=board_printer)
game = Game(board=board)
game.add_player(player_x)
game.add_player(player_o)

game.run()
