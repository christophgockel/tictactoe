class Board(object):
    def __init__(self):
        self._grid = self._initialize_grid(3, 3)

    def _initialize_grid(self, rows, columns):
        return [[None for y in range(columns)] for x in range(rows)]

    def set(self, index, symbol):
        x, y = self._index_to_coordinates(index)

        if self._cell_is_occupied(x, y):
            raise UnallowedMove

        self._grid[x][y] = symbol

    def _cell_is_occupied(self, x, y):
        return self._grid[x][y] is not None

    def get(self, index):
        x, y = self._index_to_coordinates(index)

        return self._grid[x][y]

    def _index_to_coordinates(self, index):
        row = index / self.row_count()
        column = index % self.column_count()

        return row, column

    def unset(self, index):
        x, y = self._index_to_coordinates(index)
        self._grid[x][y] = None

    def row(self, index):
        return self._grid[index]

    def column(self, index):
        return [row[index] for row in self._grid]

    def diagonal(self, index):
        if index == 0:
            return [row[i] for i, row in enumerate(self._grid)]
        else:
            return [row[-i-1] for i, row in enumerate(self._grid)]

    def is_empty(self):
        for row in self.rows():
            if any(cell is not None for cell in row):
                return False

        return True

    def is_full(self):
        for row in self._grid:
            if any(cell is None for cell in row):
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

    def diagonals(self):
        for i in range(2):
            yield self.diagonal(i)

    def available_locations(self):
        locations = []

        for row, row_content in enumerate(self.rows()):
            locations += [self._index_from_coordinates(row, column) for column, cell
                          in enumerate(row_content)
                          if cell is None]

        return locations

    def _index_from_coordinates(self, row, column):
        return row * self.row_count() + column


class UnallowedMove(Exception):
    pass


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
            board.set(row * 3 + column, symbol)

    return board
