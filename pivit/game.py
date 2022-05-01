import pygame
from enum import Enum
from .constants import RED, WHITE, FIELDWIDTH, FIELDHEIGHT, PANELWIDTH, PANELHEIGHT, SQUARE_SIZE
from .board import Board

class GameStatus(Enum):
    LIVE = 0
    NOMINIONS = 1
    NOMINIONSTIE = 2
    ONEPLAYER = 3

class GameRenderer:
    def __init__(self, window, config):
        self.window = window

class GameManager:
    def __init__(self, window, config):
        self.config = config
        self.determine_offsets(config.board_size)
        self.renderer = GameRenderer(window, config)
        self.selected = None
        self.game = Game(config, self.horizontal_offset, self.vertical_offset)

    def determine_offsets(self, board_size):
        boardwidth = boardheight = SQUARE_SIZE * board_size
        self.horizontal_offset = (FIELDWIDTH - boardwidth)//2
        self.vertical_offset = (FIELDHEIGHT - boardheight)//2

    def update(self):
        self.game.board.draw(self.renderer.window)
        self.display_info(self.renderer.window)
        self.game.board.draw_valid_moves(self.renderer.window, self.game.valid_moves)
        pygame.display.update()
        self.game.update_game_status()

    def display_info(self, window):
        panelsurf = pygame.Surface((PANELWIDTH, PANELHEIGHT))
        panelsurf.fill(color=RED)

        fontsize = 15
        font = pygame.font.Font(pygame.font.get_default_font(), fontsize)

        turnstrings = [f"Current turn: {self.game.turn}", f"Current player: {self.game.current_player.name}"]
        minionstrings = [f"{name} Minions: {self.game.players[name].minions}" for name in self.game.players.names]
        mastersstrings = [f"{name} Masters: {self.game.players[name].masters}" for name in self.game.players.names]
        infostrings = turnstrings + [i for pair in zip(minionstrings, mastersstrings) for i in pair]

        inforenders = [font.render(s, True, WHITE) for s in infostrings]

        for i in range(len(inforenders)):
            panelsurf.blit(inforenders[i], dest = (10, 10 + (i * (fontsize + 15))))

        window.blit(panelsurf, dest = (FIELDWIDTH, 0))

    def get_row_col_from_mouse(self, pos):
        voffset = self.vertical_offset
        hoffset = self.horizontal_offset
        x, y = pos
        row = (y - voffset) // SQUARE_SIZE
        col = (x - hoffset) // SQUARE_SIZE
        return row, col

    def process_mouse_click(self, pos):
        row, col = self.get_row_col_from_mouse(pos)
        self.select(row, col)

    def select(self, row, col):
        board_size = self.config.board_size
        if row < 0 or row >= board_size or col < 0 or col >= board_size:
            return

        if self.selected:
            result = self._move(row, col, self.game.turn)
            if not result:
                self.selected = None
                self.game.reset_valid_moves()
                self.select(row, col)
        
        piece = self.game.board.get_piece(row, col)
        if piece is not None and piece.player == self.game.current_player:
            self.selected = piece
            self.game.valid_moves = self.game.board.get_valid_moves(piece)

    def _move(self, row, col, turn):
        piece = self.game.board.get_piece(row, col)
        if self.selected and (row, col) in self.game.valid_moves:
            if piece is not None:
                self.game.board.remove(piece)
            self.game.board.move(self.selected, row, col, turn)
            self.game.change_turn()
        else:
            return False

        return True

    def game_is_over(self):
        return self.game.status != GameStatus.LIVE

    def game_status_message(self):
        status = self.game.status
        if status == GameStatus.LIVE:
            return "The game is ongoing. There is no winner yet."

        winner = self.game.players.winner_if_game_over()

        if status == GameStatus.ONEPLAYER:
            return f"{winner} wins as the only remaining player"
        elif status == GameStatus.NOMINIONS:
            return f"{winner} wins as they have the largest number of masters"
        elif status == GameStatus.NOMINIONSTIE:
            return f"{winner} wins as they tie for the largest number of masters and earned their first master first"
        else:
            raise ValueError

class Game:
    def __init__(self, config, hoffset, voffset):
        self.board = Board(config.board_size, config.num_players, hoffset, voffset)
        self.players = self.board.players
        self.current_player = self.players.starting()
        self.turn = 1
        self.valid_moves = []
        self.status = GameStatus.LIVE

    def update_game_status(self):
        if self.players.active_number == 1:
            self.status = GameStatus.ONEPLAYER
        elif self.players.no_minions_left():
            if self.players.master_tie():
                self.status = GameStatus.NOMINIONSTIE
            else:
                self.status = GameStatus.NOMINIONS
        else:
            self.status = GameStatus.LIVE

    def reset_valid_moves(self):
        self.valid_moves = []

    def change_turn(self):
        self.reset_valid_moves()
        self.current_player = self.players.next()
        self.turn += 1