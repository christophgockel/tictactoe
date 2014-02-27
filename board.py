class Board(object):
    def __init__(self, rows=3, columns=3, callback=None):
        self._grid = self._initialize_grid(rows, columns)
        self.callback = callback

    def _initialize_grid(self, rows, columns):
        return [[None for y in range(columns)] for x in range(rows)]

    def __setitem__(self, key, value):
        x, y = self._key_to_coordinates(key)
        self._grid[x][y] = value

        if self.callback:
            self.callback(self)

    def _key_to_coordinates(self, key):
        if isinstance(key, int):
            row = key / self.row_count()
            column = key % self.column_count()
        else:
            row, column = key

        return row, column

    def __getitem__(self, key):
        x, y = self._key_to_coordinates(key)
        return self._grid[x][y]

    def row(self, index):
        return self._grid[index]

    def column(self, index):
        column = []

        for row in self._grid:
            column.append(row[index])

        return column

    def diagonal(self, index):
        if index == 0:
            return [ row[i] for i, row in enumerate(self._grid) ]
        else:
            return [ row[-i-1] for i, row in enumerate(self._grid) ]

    def is_full(self):
        for row in self._grid:
            if None in row:
                return False

        return True

    def rows(self):
        for i in range(self.row_count()):
            yield self.row(i)

    def row_count(self):
        return len(self._grid)

    def columns(self):
        for i in range(self.column_count()):
            yield self.column(i)

    def column_count(self):
        return len(self._grid[0])


def make_board(board_state):
    def row_maker(string, n):
        while string:
            yield string[:n]
            string = string[n:]

    board = Board()

    for row, content in enumerate(row_maker(board_state, 3)):
        for column, symbol in enumerate(content):
            if symbol == ' ':
                symbol = None
            board[row, column] = symbol

    return board
