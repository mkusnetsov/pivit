import pygame
from enum import Enum
from .constants import RED, WHITE, BLUE, FIELDWIDTH, FIELDHEIGHT, PANELWIDTH, PANELHEIGHT, SQUARE_SIZE
from .board import Board

class GameStatus(Enum):
    LIVE = 0
    NOMINIONS = 1
    NOMINIONSTIE = 2
    ONEPLAYER = 3

class GameRenderer:
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

    def draw_tile(self, row, col, tilecolour):
        cornerx, cornery =  self.calc_corner_pos(row, col)
        rect = pygame.Rect(cornerx, cornery, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(self.window, tilecolour, rect)

    def draw_cell(self, cell):
        self.draw_tile(cell.row, cell.col, cell.tilecolour)
        if cell.piece is not None:
            cell.piece.draw(self.window)       

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

class GameManager:
    def __init__(self, window, config):
        self.config = config
        self.determine_offsets(config.board_size)
        self.renderer = GameRenderer(window, self.horizontal_offset, self.vertical_offset)
        self.game = Game(config, self.horizontal_offset, self.vertical_offset)

    def determine_offsets(self, board_size):
        boardwidth = boardheight = SQUARE_SIZE * board_size
        self.horizontal_offset = (FIELDWIDTH - boardwidth)//2
        self.vertical_offset = (FIELDHEIGHT - boardheight)//2

    def update(self):
        self.renderer.draw_board(self.game.board)
        self.display_info(self.renderer.window)
        self.renderer.draw_valid_moves(self.game.valid_moves)
        pygame.display.update()

    def display_info(self, window):
        panelsurf = pygame.Surface((PANELWIDTH, PANELHEIGHT))
        panelsurf.fill(color=RED)

        fontsize = 15
        font = pygame.font.Font(pygame.font.get_default_font(), fontsize)

        turnstrings = [f"Current turn: {self.game.turn}", f"Current player: {self.game.current_player.name}"]
        minionstrings = [f"{name} Minions: {self.game.players[name].minions}" for name in self.game.players.names]
        mastersstrings = [f"{name} Masters: {self.game.players[name].masters}" for name in self.game.players.names]
        infostrings = turnstrings + [i for pair in zip(minionstrings, mastersstrings) for i in pair]

        inforenders = [font.render(s, True, WHITE) for s in infostrings]

        for i in range(len(inforenders)):
            panelsurf.blit(inforenders[i], dest = (10, 10 + (i * (fontsize + 15))))

        window.blit(panelsurf, dest = (FIELDWIDTH, 0))

    def get_row_col_from_mouse(self, pos):
        voffset = self.vertical_offset
        hoffset = self.horizontal_offset
        x, y = pos
        row = (y - voffset) // SQUARE_SIZE
        col = (x - hoffset) // SQUARE_SIZE
        return row, col

    def process_mouse_click(self, pos):
        row, col = self.get_row_col_from_mouse(pos)

        board_size = self.config.board_size
        if row < 0 or row >= board_size or col < 0 or col >= board_size:
            return

        self.game.select(row, col)

    def game_is_over(self):
        return self.game.status != GameStatus.LIVE

    def game_status_message(self):
        status = self.game.status
        if status == GameStatus.LIVE:
            return "The game is ongoing. There is no winner yet."

        winner = self.game.players.winner_if_game_over()

        if status == GameStatus.ONEPLAYER:
            return f"{winner} wins as the only remaining player"
        elif status == GameStatus.NOMINIONS:
            return f"{winner} wins as they have the largest number of masters"
        elif status == GameStatus.NOMINIONSTIE:
            return f"{winner} wins as they tie for the largest number of masters and earned their first master first"
        else:
            raise ValueError

class Game:
    def __init__(self, config, hoffset, voffset):
        self.board = Board(config.board_size, config.num_players, hoffset, voffset)
        self.players = self.board.players
        self.current_player = self.players.starting()
        self.turn = 1
        self.valid_moves = []
        self.status = GameStatus.LIVE
        self.selected = None

    def select(self, row, col):
        if self.selected:
            if self.is_valid_move(row, col):
                self.take_turn(row, col, self.turn)
            else:
                self.reselect(row, col)
        
        self.try_to_pick_piece(row, col)

    def unselect(self):
        self.selected = None
        self.valid_moves = []

    def reselect(self, row, col):
        self.unselect()
        self.select(row, col)      

    def location_on_movement_axis(self, piece, shift_size, positive):
        shift = shift_size if positive else (-1 * shift_size)

        if piece.lateral:
            new_col = piece.col + shift
            if new_col >= self.board.cols or new_col < 0:
                return None
            return piece.row, new_col
        else:
            new_row = piece.row + shift
            if new_row >= self.board.rows or new_row < 0:
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

            current_piece = self.board.get_piece(current_row, current_col)

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

    def is_valid_move(self, row, col):
        return (row, col) in self.valid_moves

    def take_turn(self, row, col, turn):
        self.move(self.selected, row, col, turn)
        self.complete_turn()

    def move(self, piece, row, col, turn):
        source_cell = self.board.get_cell(piece.row, piece.col)
        target_cell = self.board.get_cell(row, col)

        self.kill_piece(target_cell.piece)
        target_cell.add_piece(piece)
        source_cell.remove_piece()

        target_cell.piece.pivot()

        if self.board.is_mastery_tile(row, col):
            target_cell.piece.make_master(turn)

    def kill_piece(self, piece):
        if piece is None:
            return

        row, col = piece.row, piece.col
        cell = self.board.get_cell(row, col)
        cell.remove_piece()

        piece.player.lose_piece(master=piece.master)
        self.players.update_active_number()

    def try_to_pick_piece(self, row, col):
        piece = self.board.get_piece(row, col)
        if piece is not None and piece.player == self.current_player:
            self.selected = piece
            self.valid_moves = self.get_valid_moves(piece)

    def complete_turn(self):
        self.update_game_status()
        self.unselect()
        self.change_turn()

    def change_turn(self):
        self.current_player = self.players.next()
        self.turn += 1

    def update_game_status(self):
        if self.players.active_number == 1:
            self.status = GameStatus.ONEPLAYER
        elif self.players.no_minions_left():
            if self.players.master_tie():
                self.status = GameStatus.NOMINIONSTIE
            else:
                self.status = GameStatus.NOMINIONS
        else:
            self.status = GameStatus.LIVE