import pygame
from .constants import RED, WHITE, FIELDWIDTH, PANELWIDTH, PANELHEIGHT, SQUARE_SIZE
from .board import Board

class Game:
    def __init__(self, win, config):
        self._init(config)
        self.win = win
    
    def update(self):
        self.board.draw(self.win)
        self.display_info(self.win)
        self.board.draw_valid_moves(self.win, self.valid_moves)
        pygame.display.update()

    def _init(self, config):
        self.selected = None
        self.board_size = config.board_size
        self.board = Board(config.board_size, config.num_players)
        self.players = self.board.players
        self.current_player = self.players.starting()
        self.turn = 1
        self.valid_moves = []

    def winner(self):
        winner = self.board.winner()
        return winner

    def reset(self):
        self._init()

    def reset_valid_moves(self):
        self.valid_moves = []

    def get_row_col_from_mouse(self, pos):
        voffset = self.board.vertical_offset
        hoffset = self.board.horizontal_offset
        x, y = pos
        row = (y - voffset) // SQUARE_SIZE
        col = (x - hoffset) // SQUARE_SIZE
        return row, col

    def process_mouse_click(self, pos):
        row, col = self.get_row_col_from_mouse(pos)
        self.select(row, col)

    def select(self, row, col):
        if row < 0 or row >= self.board_size or col < 0 or col >= self.board_size:
            return False

        if self.selected:
            result = self._move(row, col, self.turn)
            if not result:
                self.selected = None
                self.reset_valid_moves()
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        if piece is not None and piece.player == self.current_player:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
            
        return False

    def _move(self, row, col, turn):
        piece = self.board.get_piece(row, col)
        if self.selected and (row, col) in self.valid_moves:
            if piece is not None:
                self.board.remove(piece)
            self.board.move(self.selected, row, col, turn)
            self.change_turn()
        else:
            return False

        return True

    def change_turn(self):
        self.reset_valid_moves()
        self.current_player = self.players.next()
        self.turn += 1

    def display_info(self, win):
        panelsurf = pygame.Surface((PANELWIDTH, PANELHEIGHT))
        panelsurf.fill(color=RED)

        fontsize = 15
        font = pygame.font.Font(pygame.font.get_default_font(), fontsize)

        turnstrings = [f"Current turn: {self.turn}", f"Current player: {self.current_player.name}"]
        minionstrings = [f"{name} Minions: {self.players[name].minions}" for name in self.players.names]
        mastersstrings = [f"{name} Masters: {self.players[name].masters}" for name in self.players.names]
        infostrings = turnstrings + [i for pair in zip(minionstrings, mastersstrings) for i in pair]

        inforenders = [font.render(s, True, WHITE) for s in infostrings]

        for i in range(len(inforenders)):
            panelsurf.blit(inforenders[i], dest = (10, 10 + (i * (fontsize + 15))))

        win.blit(panelsurf, dest = (FIELDWIDTH, 0))