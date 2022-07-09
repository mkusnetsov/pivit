import pygame
from .constants import RED, WHITE, BLUE, GREY, SQUARE_SIZE,  FIELDWIDTH, PANELWIDTH, PANELHEIGHT, Colour

class GameRenderer:
    PADDING = 15
    OUTLINE = 2
    MAJORFACTOR = 0.9 # Length of the major axis of the diamond relative to the circle diameter
    MINORFACTOR = 0.5 # Length of the minor axis of the diamond relative to the major axis
    NEUTRALCOLOUR = GREY
    DARKTILECOL = RED
    LIGHTTILECOL = WHITE
    REDPLAYERCOL = RED
    WHITEPLATERCOL = WHITE
    INFOPANELCOL = RED
    INFOFONTCOL = WHITE
    TILECOLS = {Colour.TILEDARK: DARKTILECOL, Colour.TILELIGHT: LIGHTTILECOL}
    PLAYERCOLS = {Colour.PLAYERRED: REDPLAYERCOL, Colour.PLAYERWHITE: WHITEPLATERCOL}

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
            bg_colour = self.PLAYERCOLS[piece.colour]
            fg_colour = self.NEUTRALCOLOUR
        else:
            bg_colour = self.NEUTRALCOLOUR
            fg_colour = self.PLAYERCOLS[piece.colour]

        radius = SQUARE_SIZE//2 - self.PADDING
        diamondcoords = self.diamond_coords(radius, x, y, piece.lateral)

        pygame.draw.circle(self.window, bg_colour, (x, y), radius + self.OUTLINE)
        pygame.draw.polygon(self.window, fg_colour, diamondcoords)

    def draw_tile(self, row, col, tilecolour):
        cornerx, cornery =  self.calc_corner_pos(row, col)
        rect = pygame.Rect(cornerx, cornery, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(self.window, self.TILECOLS[tilecolour], rect)

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

    def display_info(self, game):
        panelsurf = pygame.Surface((PANELWIDTH, PANELHEIGHT))
        panelsurf.fill(color=self.INFOPANELCOL)

        fontsize = 15
        font = pygame.font.Font(pygame.font.get_default_font(), fontsize)

        turnstrings = [f"Current turn: {game.turn}", f"Current player: {game.current_player.name}"]
        minionstrings = [f"{name} Minions: {game.players[name].minions}" for name in game.players.names]
        mastersstrings = [f"{name} Masters: {game.players[name].masters}" for name in game.players.names]
        infostrings = turnstrings + [i for pair in zip(minionstrings, mastersstrings) for i in pair]

        inforenders = [font.render(s, True, self.INFOFONTCOL) for s in infostrings]

        for i in range(len(inforenders)):
            panelsurf.blit(inforenders[i], dest = (10, 10 + (i * (fontsize + 15))))

        self.window.blit(panelsurf, dest = (FIELDWIDTH, 0))