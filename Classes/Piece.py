from settings import BLOCK_SIZE


class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.image = None

    def getSquare(self):
        return self.col * 1 + self.row * 8

    def getRealXY(self):
        return self.col * BLOCK_SIZE, self.row * BLOCK_SIZE

