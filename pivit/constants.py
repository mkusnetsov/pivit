from enum import Enum

FIELDWIDTH, FIELDHEIGHT = 800, 800

PANEL_BOARD_PROPORTION = 0.25
WINWIDTH = int(FIELDWIDTH * (1 + PANEL_BOARD_PROPORTION))
WINHEIGHT = FIELDHEIGHT

PANELWIDTH = WINWIDTH - FIELDWIDTH
PANELHEIGHT = FIELDHEIGHT

MAX_BOARD_SIZE = 8
MAX_BOARD_FIELD_PROPORTION = 15/16
MAXBOARDDIM = int(FIELDWIDTH * MAX_BOARD_FIELD_PROPORTION)
SQUARE_SIZE = MAXBOARDDIM//MAX_BOARD_SIZE

# rgb
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128,128,128)

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

class GameStatus(Enum):
    LIVE = 0
    NOMINIONS = 1
    NOMINIONSTIE = 2
    ONEPLAYER = 3

class Colour(Enum):
    TILELIGHT = 0
    TILEDARK = 1
    PLAYERRED = 2
    PLAYERWHITE = 3

class GameConfig:
    def __init__(self):
        self.num_players = 2
        self.board_size = 8

    def set_num_players(self, num_players):
        self.num_players = num_players

    def set_board_size(self, board_size):
        self.board_size = board_size
