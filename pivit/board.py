from .constants import RED, WHITE, DARKTILECOL, LIGHTTILECOL, STARTINGCOORDS, SQUARE_SIZE, FIELDWIDTH, FIELDHEIGHT
from .piece import Cell, Piece
from .players import Player, Players

class Board:
    def __init__(self, board_size, num_players):
        self.initialise_board(board_size)
        self.initialise_players(board_size, num_players)
        self.determine_offsets(board_size)
        self.create_board(board_size, num_players)

    def initialise_board(self, board_size):
        self.board = []
        self.rows = board_size
        self.cols = board_size

    def initialise_players(self, board_size, num_players):
        minions = (board_size - 2) * 4 // num_players
        self.players = Players([Player("Red", RED, minions), Player("White", WHITE, minions)])

    def determine_offsets(self, board_size):
        boardwidth = boardheight = SQUARE_SIZE * board_size
        self.horizontal_offset = (FIELDWIDTH - boardwidth)//2
        self.vertical_offset = (FIELDHEIGHT - boardheight)//2

    def is_edge_row(self, row):
        return row == self.rows - 1 or row == 0

    def is_edge_col(self, col):
        return col == self.cols - 1 or col == 0

    def tile_colour(self, row, col):
        if (row - col) % 2 == 0:
            return DARKTILECOL
        else:
            return LIGHTTILECOL

    def is_mastery_tile(self, row, col):
        return self.is_edge_row(row) and self.is_edge_col(col)

    def starts_lateral(self, row, col):
        return self.is_edge_col(col)

    def who_is_player(self, row, col, board_size, num_players):
        num_players_for_board_size = STARTINGCOORDS[board_size]
        players_for_board_size = num_players_for_board_size[num_players]
        
        for player in range(num_players):
            player_rows, player_cols = players_for_board_size[player]

            starting_col = self.is_edge_col(col) and row in player_rows
            starting_row = self.is_edge_row(row) and col in player_cols

            if starting_col or starting_row:
                return player
            else:
                pass

        return None

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

    def create_board(self, board_size, num_players):
        for row in range(self.rows):
            self.board.append([])
            for col in range(self.cols):

                tilecolour = self.tile_colour(row, col)
                masterytile = self.is_mastery_tile(row, col)
                lateral = self.starts_lateral(row, col)
                player_index = self.who_is_player(row, col, board_size, num_players)

                if player_index is None:
                    piece = None
                else:
                    player_name = self.players.names[player_index]
                    player = self.players[player_name]
                    piece = Piece(row, col, player, lateral)

                cell = Cell(row, col, tilecolour, masterytile, piece, self)

                self.board[row].append(cell)
        
    def draw(self, window):
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.board[row][col]
                cell.draw(window)

    def draw_valid_moves(self, window, moves):
        for move in moves:
            row, col = move
            cell = self.get_cell(row, col)
            cell.draw_valid_move_marker(window)

    def remove(self, piece):
        row, col = piece.row, piece.col
        cell = self.get_cell(row, col)
        cell.remove_piece()

        if piece is not None:
            piece.player.lose_piece(master=piece.master)
            self.players.update_active_number()

    def location_on_movement_axis(self, piece, shift_size, positive):
        shift = shift_size if positive else (-1 * shift_size)

        if piece.lateral:
            new_col = piece.col + shift
            if new_col >= self.cols or new_col < 0:
                return None
            return piece.row, new_col
        else:
            new_row = piece.row + shift
            if new_row >= self.rows or new_row < 0:
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