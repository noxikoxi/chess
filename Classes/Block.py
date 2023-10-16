from pygame import Rect


class Block:
    def __init__(self, row, col, color, settings, piece=None):
        self.rect = None
        self.row = row
        self.col = col
        self.piece = piece
        self.color = color
        self.naturalColor = color
        self.settings = settings
        self.updateRect()

    def glow(self):
        self.color = (0, 220, 32)
        self.updateRect()
        # self.active = True

    def danger(self):
        self.color = (240, 0, 50)
        self.updateRect()
        # self.active = True

    def resetColor(self):
        self.color = self.naturalColor
        self.updateRect()
        # self.active = False

    def updateRect(self):
        self.rect = Rect(int(self.settings.block_size * self.col), int(self.settings.block_size * self.row),
                         self.settings.block_size, self.settings.block_size)

    @staticmethod
    def getBoardIndexXY(x, y, offset, block_size):
        return int(((y - offset) // block_size) * 8 + ((x - offset) // block_size) * 1)

    @staticmethod
    def getBoardIndexRowCol(row, col):
        return col * 1 + row * 8