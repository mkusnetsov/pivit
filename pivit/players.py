from itertools import cycle

class Player:
    STARTING_MINIONS = 12
    STARTING_MASTERS = 0

    def __init__(self, name, colour):
        self.name = name
        self.colour = colour
        self.minions = self.STARTING_MINIONS
        self.masters = self.STARTING_MASTERS
        self.defeated = False
        self.first_master = None

    def lose_piece(self, master):
        if master:
            self.masters -= 1
        else:
            self.minions -= 1
        if self.masters + self.minions == 0:
            self.defeated = True

    def promote_piece(self, turn):
        self.masters += 1
        self.minions -= 1
        if self.first_master is None:
            self.first_master = turn

    def __repr__(self):
        return self.name

    def __lt__(self, other):
        if other.defeated:
            return False

        if self.defeated:
            return True

        if self.masters != other.masters:
            return self.masters < other.masters
        elif self.masters == 0:
            return False
        else:
            return self.first_master > other.first_master

class Players:
    def __init__(self, players):
        self.number = len(players)
        self.active_number = len(players)
        self.names = [p.name for p in players]
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
        self._current = next(self._players_cycle)
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
        return sorted(active_players, reverse=True)[0]
