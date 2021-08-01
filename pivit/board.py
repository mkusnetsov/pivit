from .constants import ROWS, RED, COLS, WHITE, DARKTILECOL, LIGHTTILECOL
from .piece import Cell, Piece
from .players import Player, Players

class Board:
    def __init__(self, board_size, num_players):
        print(f"Board size: {board_size}")
        self.board = []
        self.players = Players([Player("Red", RED), Player("White", WHITE)])
        self.red_minions = self.white_minions = 12
        self.red_masters = self.white_masters = 0
        self.create_board()

    def is_mastery_tile(self, row, col):
        return (row == ROWS - 1 or row == 0) and (col == ROWS - 1 or col == 0)

    def starts_lateral(self, row, col):
        return col == 0 or col == COLS-1

    def is_starting_white(self, row, col):
        if col == 0 or col == COLS-1:
            if row in [1, 3, 4, 6]:
                return True
        elif row == 0 or row == ROWS-1:
            if col in [2, 5]:
                return True
        return False

    def is_starting_red(self, row, col):
        if col == 0 or col == COLS-1:
            if row in [2, 5]:
                return True
        elif row == 0 or row == ROWS-1:
            if col in [1, 3, 4, 6]:
                return True
        return False

    def get_cell(self, row, col):
        return self.board[row][col]

    def get_piece(self, row, col):
        cell = self.get_cell(row, col)
        return cell.piece

    def move(self, piece, row, col, turn):
        source_cell = self.get_cell(piece.row, piece.col)
        target_cell = self.get_cell(row, col)

        target_cell.add_piece(piece)
        source_cell.remove_piece()

        target_cell.piece.pivot()

        if self.is_mastery_tile(row, col):
            target_cell.piece.make_master(turn)

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if (row - col) % 2 == 0:
                    tilecolour = DARKTILECOL
                else:
                    tilecolour = LIGHTTILECOL

                masterytile = self.is_mastery_tile(row, col)

                if self.is_starting_white(row, col):
                    if self.starts_lateral(row, col):
                        piece = Piece(row, col, self.players["White"], True)
                    else:
                        piece = Piece(row, col, self.players["White"], False)
                elif self.is_starting_red(row, col):
                    if self.starts_lateral(row, col):
                        piece = Piece(row, col, self.players["Red"], True)
                    else:
                        piece = Piece(row, col, self.players["Red"], False)
                else:
                    piece = None

                self.board[row].append(Cell(row, col, tilecolour, masterytile, piece))
        
    def draw(self, win):
        for row in range(ROWS):
            for col in range(COLS):
                cell = self.board[row][col]
                cell.draw(win)

    def draw_valid_moves(self, win, moves):
        for move in moves:
            row, col = move
            cell = self.get_cell(row, col)
            cell.draw_valid_move_marker(win)

    def remove(self, piece):
        row, col = piece.row, piece.col
        cell = self.get_cell(row, col)
        cell.remove_piece()

        if piece is not None:
            if piece.master:
                piece.player.lose_piece(master=True)
            else:
                piece.player.lose_piece(master=False)
            self.players.update_active_number()
    
    def game_is_over(self):
        if self.players.active_number == 1:
            return True
        elif self.players.no_minions_left():
            return True
        else:
            return False

    def winner(self):
        if self.game_is_over():
            return self.players.winner_if_game_over()
        
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

            if current_piece is not None:
                encountered_piece = True
            encountered_own = piece.same_side(current_piece)
            permissible_shift = (piece.master == True or shift_size % 2 != 0)

            if not encountered_own and permissible_shift:
                moves += [(current_row, current_col)]

            shift_size += 1
        
        return moves

    def get_valid_moves(self, piece):
        moves = self.traverse_direction(piece, True)
        moves = moves + self.traverse_direction(piece, False)
        return moves