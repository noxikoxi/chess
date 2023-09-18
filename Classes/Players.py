from Classes.Pawn import Pawn
from Classes.Rook import Rook
from Classes.Queen import Queen
from Classes.King import King
from Classes.Bishop import Bishop
from Classes.Knight import Knight

ROW = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]


class Player:
    def __init__(self, color, time):
        self.pieces = []
        self.color = color
        self.points = 0
        self.time = time
        self.pieces = []

    def fillPieces(self):
        if self.color == 'white':
            for i in range(8):
                self.pieces.append(Pawn(6, i, self.color))

            for i, piece in enumerate(ROW):
                self.pieces.append(piece(7, i, self.color))
        else:
            for i in range(8):
                self.pieces.append(Pawn(1, i, self.color))

            for i, piece in enumerate(ROW):
                self.pieces.append(piece(0, i, self.color))

