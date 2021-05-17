from itertools import cycle

class Player:
    def __init__(self, name, colour):
        self.name = name
        self.colour = colour

    def __repr__(self):
        return self.name

class Players:
    def __init__(self, players):
        self.number = len(players)
        self._players_cycle = cycle(players)
        self._players_dict = {p.name: p for p in players}
        self._starting = next(self._players_cycle)
        self._current = self._starting

    def __getitem__(self, key):
        return self._players_dict[key]

    def starting(self):
        return self._starting

    def current(self):
        return self._current
     
    def next(self):
        self._current = next(self.players)
        return self._current