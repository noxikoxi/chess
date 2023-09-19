from settings import BLOCK_SIZE
from Classes.Block import Block


def returnValidMoves(moves):
    return [x for x in moves if 0 <= x[0] <= 7 and 0 <= x[1] <= 7]


def checkStackMoves(color, moves, board):
    return [x for x in moves if board[Block.getBoardIndexRowCol(x[0], x[1])].piece is None
            or board[Block.getBoardIndexRowCol(x[0], x[1])].piece.color != color]


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

    def getPossibleMoves(self, board):
        return []

    def move(self, row, col):
        self.row = row
        self.col = col
