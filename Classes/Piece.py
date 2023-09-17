BLOCK_SIZE = 100


class Piece:
    def __init__(self, row, col, color, image):
        self.row = row
        self.col = col
        self.color = color
        self.image = image

    def getSquare(self):
        return self.col * 8 + self.row * 1

    def getRealXY(self):
        return self.col * BLOCK_SIZE, self.row * BLOCK_SIZE
