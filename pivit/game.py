import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE, ROWS, COLS, FIELDWIDTH, PANELWIDTH, PANELHEIGHT, VERTICALOFFSET, HORIZONTALOFFSET
from .board import Board

class Game:
    def __init__(self, win):
        self._init()
        self.win = win
    
    def update(self):
        self.board.draw(self.win)
        self.display_info(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
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

    def select(self, row, col):
        if row < 0 or row >= ROWS or col < 0 or col >= COLS:
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

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (HORIZONTALOFFSET + col * SQUARE_SIZE + SQUARE_SIZE//2, VERTICALOFFSET + row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

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