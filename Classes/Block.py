from pygame import Rect
from settings import BLOCK_SIZE, OFFSET

class Block:
    def __init__(self, row, col, color, piece=None,):
        self.row = row
        self.col = col
        self.piece = piece
        self.color = color
        self.naturalColor = color
        # self.active = False
        self.__updateRect()

    def glow(self):
        self.color = (0, 220, 32)
        self.__updateRect()
        # self.active = True

    def danger(self):
        self.color = (240, 0, 50)
        self.__updateRect()
        # self.active = True

    def resetColor(self):
        self.color = self.naturalColor
        self.__updateRect()
        # self.active = False

    def __updateRect(self):
        self.rect = Rect(int(BLOCK_SIZE * self.col), int(BLOCK_SIZE * self.row), BLOCK_SIZE, BLOCK_SIZE)

    @staticmethod
    def getBoardIndexXY(x, y):
        return int(((y - OFFSET) // BLOCK_SIZE) * 8 + ((x - OFFSET) // BLOCK_SIZE) * 1)

    @staticmethod
    def getBoardIndexRowCol(row, col):
        return col * 1 + row * 8