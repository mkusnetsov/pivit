import pygame
from .constants import BLUE, GREY, SQUARE_SIZE

class GameRenderer:
    PADDING = 15
    OUTLINE = 2
    MAJORFACTOR = 0.9 # Length of the major axis of the diamond relative to the circle diameter
    MINORFACTOR = 0.5 # Length of the minor axis of the diamond relative to the major axis
    NEUTRALCOLOUR = GREY

    def __init__(self, window, horizontal_offset, vertical_offset):
        self.window = window
        self.horizontal_offset = horizontal_offset
        self.vertical_offset = vertical_offset

    def calc_corner_pos(self, row, col):
        cornerx = self.horizontal_offset + col * SQUARE_SIZE
        cornery = self.vertical_offset + row * SQUARE_SIZE
        return cornerx, cornery

    def calc_centre_pos(self, row, col):
        cornerx, cornery = self.calc_corner_pos(row, col)
        centrex = cornerx + SQUARE_SIZE // 2
        centrey = cornery + SQUARE_SIZE // 2
        return centrex, centrey

    def diamond_coords(self, radius, x, y, lateral):
        halfmajorlen = radius * self.MAJORFACTOR
        halfminorlen = halfmajorlen * self.MINORFACTOR

        if lateral:
            halfhorizontal = halfmajorlen
            halfvertical = halfminorlen
        else:
            halfhorizontal = halfminorlen
            halfvertical = halfmajorlen

        diamondcoords = [
            (x - halfhorizontal, y),
            (x, y + halfvertical),
            (x + halfhorizontal, y),
            (x, y - halfvertical),
        ]

        return diamondcoords
    
    def draw_piece(self, piece, x, y):
        if piece.master:
            bg_colour = piece.colour
            fg_colour = self.NEUTRALCOLOUR
        else:
            bg_colour = self.NEUTRALCOLOUR
            fg_colour = piece.colour

        radius = SQUARE_SIZE//2 - self.PADDING
        diamondcoords = self.diamond_coords(radius, x, y, piece.lateral)

        pygame.draw.circle(self.window, bg_colour, (x, y), radius + self.OUTLINE)
        pygame.draw.polygon(self.window, fg_colour, diamondcoords)

    def draw_tile(self, row, col, tilecolour):
        cornerx, cornery =  self.calc_corner_pos(row, col)
        rect = pygame.Rect(cornerx, cornery, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(self.window, tilecolour, rect)

    def draw_cell(self, cell):
        self.draw_tile(cell.row, cell.col, cell.tilecolour)
        if cell.piece is not None:
            centrex, centrey = self.calc_centre_pos(cell.row, cell.col)
            self.draw_piece(cell.piece, centrex, centrey)       

    def draw_board(self, board):
        for row in range(board.rows):
            for col in range(board.cols):
                cell = board.board[row][col]
                self.draw_cell(cell)

    def draw_valid_move_marker(self, window, row, col):
        centrex, centrey = self.calc_centre_pos(row, col)
        pygame.draw.circle(window, BLUE, (centrex, centrey), 15)

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            self.draw_valid_move_marker(self.window, row, col)