class Piece:
    def __init__(self, x, y, color, image):
        self.x = x
        self.y = y
        self.color = color
        self.image = image

    def getSquare(self):
        return self.x * 8 + self.y * 1
