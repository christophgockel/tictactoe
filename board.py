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
