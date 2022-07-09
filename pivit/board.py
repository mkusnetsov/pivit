from .constants import STARTINGCOORDS, Colour
from .piece import Cell, Piece
from .players import Player, Players

class Board:
    def __init__(self, board_size, num_players):
        self.initialise_board(board_size)
        self.initialise_players(board_size, num_players)
        self.create_board(board_size, num_players)

    def initialise_board(self, board_size):
        self.board = []
        self.rows = board_size
        self.cols = board_size

    def initialise_players(self, board_size, num_players):
        minions = (board_size - 2) * 4 // num_players
        self.players = Players([Player("Red", Colour.PLAYERRED, minions), Player("White", Colour.PLAYERWHITE, minions)])

    def is_edge_row(self, row):
        return row == self.rows - 1 or row == 0

    def is_edge_col(self, col):
        return col == self.cols - 1 or col == 0

    def tile_colour(self, row, col):
        if (row - col) % 2 == 0:
            return Colour.TILEDARK
        else:
            return Colour.TILELIGHT

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

                cell = Cell(row, col, tilecolour, masterytile, piece)

                self.board[row].append(cell)