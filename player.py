class Player(object):
    def __init__(self, symbol, callback=None):
        self._symbol = symbol
        self._callback = callback

    @property
    def symbol(self):
        return self._symbol

    def next_move(self):
        if self._callback:
            return self._callback(self.symbol)
