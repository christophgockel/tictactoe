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

player_x = Player('x', user_input)
player_o = Player('o', user_input)

game = Game()
game.add_player(player_x)
game.add_player(player_o)

game.run()
