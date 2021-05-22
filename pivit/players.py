from itertools import cycle

from pygame import error

class Player:
    STARTING_MINIONS = 12
    STARTING_MASTERS = 0

    def __init__(self, name, colour):
        self.name = name
        self.colour = colour
        self.minions = self.STARTING_MINIONS
        self.masters = self.STARTING_MASTERS
        self.defeated = False

    def lose_piece(self, master):
        if master:
            self.masters -= 1
        else:
            self.minions -= 1
        if self.masters + self.minions == 0:
            self.defeated = True

    def promote_piece(self):
        self.masters += 1
        self.minions -= 1

    def __repr__(self):
        return self.name

class Players:
    def __init__(self, players):
        self.number = len(players)
        self.active_number = len(players)
        self.names = [p.name for p in players]
        self._players_cycle = cycle(players)
        self._players_dict = {p.name: p for p in players}
        self._starting = players[0]
        self._current = players[0]

    def __getitem__(self, key):
        return self._players_dict[key]

    def starting(self):
        return self._starting

    def current(self):
        return self._current
     
    def next(self):
        self._current = next(self.players)
        if self._current.defeated:
            return self.next()
        return self._current

    def get_active_players(self):
        return [player for player in self._players_dict.values() if not player.defeated]

    def update_active_number(self):
        active_players = self.get_active_players()
        self.active_number = len(active_players)

    def no_minions_left(self):
        active_players = self.get_active_players()
        minion_counts = [player.minions for player in active_players]
        return sum(minion_counts) == 0

    def winner_if_game_over(self):
        active_players = self.get_active_players()
        master_counts = [player.masters for player in active_players]
        max_count = max(master_counts)
        most_master_players = [player for player in active_players if player.masters == max_count]
        if len(most_master_players) == 1:
            return most_master_players[0]
        else:
            raise RuntimeError("Ties still need to be implemented")
