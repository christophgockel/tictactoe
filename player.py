class Player(object):
    O = 'o'
    X = 'x'

    def __init__(self, symbol, player_input=None):
        self._symbol = symbol
        self._input = player_input

    @property
    def symbol(self):
        return self._symbol

    def next_move(self, board=None):
        if self._input:
            return self._input.next_move(self.symbol, board)


def PlayerO(input_delegate=None):
    return Player(Player.O, input_delegate)

def PlayerX(input_delegate=None):
    return Player(Player.X, input_delegate)
