import pygame
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE, WIDTH
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.red_minions = self.white_minions = 12
        self.red_masters = self.white_masters = 0
        self.first_master = None
        self.first_capture = None
        self.create_board()
    
    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, RED, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def display_info(self, win):
        fontsize = 15
        font = pygame.font.Font(pygame.font.get_default_font(), fontsize)

        infostrings = [
            f"White Minions: {self.white_minions}",
            f"White Masters: {self.white_masters}",
            f"Red Minions: {self.red_minions}",
            f"Red Masters: {self.red_masters}"
            ]
        inforenders = [font.render(s, True, WHITE) for s in infostrings]

        for i in range(len(inforenders)):
            win.blit(inforenders[i], dest = (WIDTH + 10, 10 + (i * (fontsize + 15))))

    def is_corner(self, row, col):
        return (row == ROWS - 1 or row == 0) and (col == ROWS - 1 or col == 0)

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if self.is_corner(row, col):
            piece.make_master()
            if piece.colour == WHITE:
                self.white_masters += 1
                self.white_minions -= 1
                if self.first_master is None:
                    self.first_master = WHITE
            else:
                self.red_masters += 1 
                self.red_minions -= 1 
                if self.first_master is None:
                    self.first_master = RED

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col == 0 or col == COLS-1:
                    print(f"{col},{row}")
                    if row in [2, 5]:
                        self.board[row].append(Piece(row, col, RED, True))
                    elif row in [1, 3, 4, 6]:
                        self.board[row].append(Piece(row, col, WHITE, True))
                    else:
                        print(f"blank at: {col},{row}")
                        self.board[row].append(0)
                elif row == 0 or row == ROWS-1:
                    if col in [1, 3, 4, 6]:
                        self.board[row].append(Piece(row, col, RED, False))
                    elif col in [2, 5]:
                        self.board[row].append(Piece(row, col, WHITE, False))
                else:
                    self.board[row].append(0)
        
    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)
        self.display_info(win)
        

    def remove(self, piece):
        self.board[piece.row][piece.col] = 0
        if piece != 0:
            if piece.colour == RED and piece.master:
                self.red_masters -= 1
            elif piece.colour == WHITE and piece.master:
                self.white_masters -= 1
            if piece.colour == RED and not piece.master:
                self.red_minions -= 1
            elif piece.colour == WHITE and not piece.master:
                self.white_minions -= 1
    
    def winner(self):
        if self.red_minions + self.red_masters == 0:
            return WHITE
        elif self.white_minions + self.white_masters == 0:
            return RED
            
        if self.red_minions + self.white_minions == 0:
            if self.red_masters > self.white_masters:
                return RED
            elif self.red_masters < self.white_masters:
                return WHITE
            elif self.first_master is not None:
                return self.first_master
            else:
                return self.first_capture
        
        return None 

    def location_on_movement_axis(self, piece, shift_size, positive):
        shift = shift_size if positive else (-1 * shift_size)

        if piece.lateral:
            new_col = piece.col + shift
            if new_col >= COLS or new_col < 0:
                return None
            return piece.row, new_col
        else:
            new_row = piece.row + shift
            if new_row >= ROWS or new_row < 0:
                return None
            return new_row, piece.col

    def traverse_direction(self, piece, positive):
        moves = []
        shift_size = 1
        encountered_piece = False

        while not encountered_piece:
            current_coords = self.location_on_movement_axis(piece, shift_size, positive)
            if current_coords is None:
                break
            else:
                current_row, current_col = current_coords

            current_piece = self.get_piece(current_row, current_col)

            if current_piece != 0:
                encountered_piece = True
            encountered_own = piece.same_colour(current_piece)
            permissible_shift = (piece.master == True or shift_size % 2 != 0)

            if not encountered_own and permissible_shift:
                moves += [(current_row, current_col)]

            shift_size += 1
        
        return moves

    def get_valid_moves(self, piece):
        moves = self.traverse_direction(piece, True)
        moves = moves + self.traverse_direction(piece, False)
        return moves