from Classes.Pawn import Pawn


class Player:
    def __init__(self, color, time):
        self.pieces = []
        self.color = color
        self.points = 0
        self.time = time
        self.pieces = []

    def fillPieces(self):
        for i in range(8):
            self.pieces.append(Pawn(1, i, self.color))
