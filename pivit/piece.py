import pygame
from .constants import RED, WHITE, SQUARE_SIZE, GREY

class Cell:
    def __init__(self, row, col, tilecolour, masterytile, piece):
        self.row = row
        self.col = col
        self.tilecolour = tilecolour
        self.masterytile = masterytile
        self.piece = piece

    def _tile_rect(self):
        tilex = self.col * SQUARE_SIZE
        tiley = self.row * SQUARE_SIZE
        return pygame.Rect(tilex, tiley, SQUARE_SIZE, SQUARE_SIZE)

    def _draw_tile(self, win):
        pygame.draw.rect(win, self.tilecolour, self._tile_rect())

    def draw(self, win):
        self._draw_tile(win)
        if self.piece is not None:
            self.piece.draw(win)

    def remove_piece(self):
        self.piece = None
    
    def add_piece(self, piece):
        self.piece = piece
        

class Piece:
    PADDING = 15
    OUTLINE = 2
    MAJORFACTOR = 0.9 # Length of the major axis of the diamond relative to the circle diameter
    MINORFACTOR = 0.5 # Length of the minor axis of the diamond relative to the major axis
    NEUTRALCOLOUR = GREY

    def __init__(self, row, col, player, lateral):
        self.row = row
        self.col = col
        self.player = player
        self.colour = player.colour
        self.master = False
        self.x = 0
        self.y = 0
        self.calc_pos()
        self.lateral = lateral

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def pivot(self):
        self.lateral = not self.lateral

    def make_master(self):
        self.master = True

    def diamond_coords(self, radius):
        halfmajorlen = radius * self.MAJORFACTOR
        halfminorlen = halfmajorlen * self.MINORFACTOR

        if self.lateral:
            halfhorizontal = halfmajorlen
            halfvertical = halfminorlen
        else:
            halfhorizontal = halfminorlen
            halfvertical = halfmajorlen

        diamondcoords = [
            (self.x - halfhorizontal, self.y),
            (self.x, self.y + halfvertical),
            (self.x + halfhorizontal, self.y),
            (self.x, self.y - halfvertical),
        ]

        return diamondcoords
    
    def draw(self, win):
        if self.master:
            bg_colour = self.colour
            fg_colour = self.NEUTRALCOLOUR
        else:
            bg_colour = self.NEUTRALCOLOUR
            fg_colour = self.colour

        radius = SQUARE_SIZE//2 - self.PADDING
        diamondcoords = self.diamond_coords(radius)

        pygame.draw.circle(win, bg_colour, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.polygon(win, fg_colour, diamondcoords)

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()
        self.pivot()

    def same_side(self, piece):
        if piece is None:
            return False
        else:
            return self.player == piece.player

    def __repr__(self):
        return str(self.player.name)