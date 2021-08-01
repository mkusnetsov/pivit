

FIELDWIDTH, FIELDHEIGHT = 800, 800

WINWIDTH = int(FIELDWIDTH * 1.25)
WINHEIGHT = FIELDHEIGHT

PANELWIDTH = WINWIDTH - FIELDWIDTH
PANELHEIGHT = FIELDHEIGHT

BOARDWIDTH, BOARDHEIGHT = int(FIELDWIDTH / 16 * 15), int(FIELDHEIGHT / 16 * 15)
HORIZONTALOFFSET, VERTICALOFFSET = (FIELDWIDTH - BOARDWIDTH)//2, (FIELDHEIGHT - BOARDHEIGHT)//2

ROWS, COLS = 8, 8
SQUARE_SIZE = BOARDWIDTH//COLS

# rgb
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128,128,128)

DARKTILECOL = RED
LIGHTTILECOL = WHITE

class GameConfig:
    def __init__(self):
        self.num_players = 2
        self.board_size = 8

    def set_num_players(self, num_players):
        self.num_players = num_players

    def set_board_size(self, board_size):
        self.board_size = board_size
