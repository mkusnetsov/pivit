

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

STARTINGCOORDS = {
    6: {
        2: {
            0: [[2, 4], [1, 3]],
            1: [[1, 3], [2, 4]]
        }
    },

    8: {
        2: {
            0: ([2, 5], [1, 3, 4, 6]),
            1: ([1, 3, 4, 6], [2, 5])
        },

        3: {
            0: ([3, 6], [1, 4]),
            1: ([2, 5], [2, 5]),
            2: ([1, 4], [3, 6]),
        },

        4: {
            0: ([3], [1, 5]),
            1: ([4], [2, 6]),
            2: ([1, 5], [3]),
            3: ([2, 6], [4])
        }
    }
}

class GameConfig:
    def __init__(self):
        self.num_players = 2
        self.board_size = 8

    def set_num_players(self, num_players):
        self.num_players = num_players

    def set_board_size(self, board_size):
        self.board_size = board_size
