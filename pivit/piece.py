import pygame
from .constants import SQUARE_SIZE, GREY, BLUE

class Cell:
    def __init__(self, row, col, tilecolour, masterytile, piece, hoffset, voffset):
        self.row = row
        self.col = col
        self.cornerx = 0
        self.cornery = 0
        self.centrex = 0
        self.centrey = 0
        self.vertical_offset = hoffset
        self.horizontal_offset = voffset
        self.calc_corner_pos()
        self.calc_centre_pos()
        self.tilecolour = tilecolour
        self.masterytile = masterytile
        self.piece = piece
        if self.piece is not None:
            self.piece.set_pos(self.row, self.col, self.centrex, self.centrey)

    def calc_corner_pos(self):
        self.cornerx = self.horizontal_offset + self.col * SQUARE_SIZE
        self.cornery = self.vertical_offset + self.row * SQUARE_SIZE

    def calc_centre_pos(self):
        self.centrex = self.cornerx + SQUARE_SIZE // 2
        self.centrey = self.cornery + SQUARE_SIZE // 2

    # def _draw_tile(self, window):
    #     rect = pygame.Rect(self.cornerx, self.cornery, SQUARE_SIZE, SQUARE_SIZE)
    #     pygame.draw.rect(window, self.tilecolour, rect)

    # def draw(self, window):
    #     self._draw_tile(window)
    #     if self.piece is not None:
    #         self.piece.draw(window)

    def draw_valid_move_marker(self, window):
        pygame.draw.circle(window, BLUE, (self.centrex, self.centrey), 15)

    def remove_piece(self):
        self.piece = None
    
    def add_piece(self, piece):
        self.piece = piece
        if self.piece is not None:
            self.piece.set_pos(self.row, self.col, self.centrex, self.centrey)
        

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
        self.lateral = lateral

    def set_pos(self, row, col, x, y):
        self.row = row
        self.col = col
        self.x = x
        self.y = y

    def pivot(self):
        self.lateral = not self.lateral

    def make_master(self, turn):
            self.master = True
            self.player.promote_piece(turn)

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
    
    def draw(self, window):
        if self.master:
            bg_colour = self.colour
            fg_colour = self.NEUTRALCOLOUR
        else:
            bg_colour = self.NEUTRALCOLOUR
            fg_colour = self.colour

        radius = SQUARE_SIZE//2 - self.PADDING
        diamondcoords = self.diamond_coords(radius)

        pygame.draw.circle(window, bg_colour, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.polygon(window, fg_colour, diamondcoords)

    def same_side(self, piece):
        if piece is None:
            return False
        else:
            return self.player == piece.player

    def __repr__(self):
        return str(self.player.name)