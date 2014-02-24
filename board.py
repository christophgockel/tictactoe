class Board(object):
    def __init__(self, rows=3, columns=3):
        self._grid = self._initialize_grid(rows, columns)

    def _initialize_grid(self, rows, columns):
        return [[None for y in range(rows)] for x in range(columns)]

    def __setitem__(self, key, value):
        x, y = key
        self._grid[x][y] = value

    def __getitem__(self, key):
        x, y = key
        return self._grid[x][y]
