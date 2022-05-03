class Cell:
    def __init__(self, row, col, tilecolour, masterytile, piece):
        self.row = row
        self.col = col
        self.tilecolour = tilecolour
        self.masterytile = masterytile
        self.piece = piece
        if self.piece is not None:
            self.piece.set_pos(self.row, self.col)

    def remove_piece(self):
        self.piece = None
    
    def add_piece(self, piece):
        self.piece = piece
        if self.piece is not None:
            self.piece.set_pos(self.row, self.col)
        

class Piece:
    def __init__(self, row, col, player, lateral):
        self.row = row
        self.col = col
        self.player = player
        self.colour = player.colour
        self.master = False
        self.lateral = lateral

    def set_pos(self, row, col):
        self.row = row
        self.col = col

    def pivot(self):
        self.lateral = not self.lateral

    def make_master(self, turn):
            self.master = True
            self.player.promote_piece(turn)

    def same_side(self, piece):
        if piece is None:
            return False
        else:
            return self.player == piece.player

    def __repr__(self):
        return str(self.player.name)