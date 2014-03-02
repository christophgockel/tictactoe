class Player(object):
    def __init__(self, symbol, input=None):
        self._symbol = symbol
        self._input = input

    @property
    def symbol(self):
        return self._symbol

    def next_move(self, board=None):
        if self._input:
            return self._input.next_move(self.symbol, board)
