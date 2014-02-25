class GameState(object):
    ongoing  = 0
    tie      = 1
    winner_x = 2
    winner_y = 3


class Rules(object):
    def enough_players(self, players):
        if len(players) == 2:
            return True
        else:
            return False

    def finished(self, board):
        return board.is_full()

    def game_state(self, board):
        if not board.is_full():
            return GameState.ongoing
        else:
            return GameState.tie


class Game(object):
    def __init__(self, rules = Rules()):
        self.players = []
        self.rules = rules

    def run(self):
        if self.rules.enough_players(self.players):
            while not self.rules.finished():
                pass
        else:
            raise TooFewPlayers()
    
    def add_player(self, player):
        self.players.append(player)

    def state(self):
        return board.contents()


class TooFewPlayers(Exception):
    pass
