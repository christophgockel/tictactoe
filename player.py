class Player(object):
    def __init__(self, symbol, player_input=None):
        self._symbol = symbol
        self._input = player_input

    @property
    def symbol(self):
        return self._symbol

    def next_move(self, board=None):
        if self._input:
            return self._input.next_move(self.symbol, board)

    def revised_next_move(self, board=None):
        if self._input:
            return self._input.revised_next_move(self.symbol, board)
