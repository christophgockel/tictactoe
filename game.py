class Rules(object):
    def new_method(self):
        pass
    def have_enough_players(self, players):
        if len(players) == 2:
            return True
        else:
            return False

class Game(object):
    def __init__(self, rules = Rules()):
        self.players = []
        self.rules = rules

    def run(self):
        if self.rules.have_enough_players(self.players):
            pass
        else:
            raise TooFewPlayers()
    
    def add_player(self, player):
        self.players.append(player)

class TooFewPlayers(Exception):
    pass
