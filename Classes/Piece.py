from settings import BLOCK_SIZE
from Classes.Block import Block


def checkValidRange(row, col):
    if 0 <= row <= 7 and 0 <= col <= 7:
        return True


def returnValidMoves(moves):
    return [x for x in moves if checkValidRange(x[0], x[1])]


def checkStackMoves(color, moves, board):
    return [x for x in moves if board[Block.getBoardIndexRowCol(x[0], x[1])].piece is None
            or board[Block.getBoardIndexRowCol(x[0], x[1])].piece.color != color]


class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.moves = []
        self.image = None
        self.movescount = 0

    def getSquare(self):
        return self.col * 1 + self.row * 8

    def getRealXY(self):
        return self.col * BLOCK_SIZE, self.row * BLOCK_SIZE

    def getPossibleMoves(self, board):
        return []

    def __changeBoard(self, row, col, oldRow, oldCol, board):
        board[Block.getBoardIndexRowCol(row, col)].piece = self
        board[Block.getBoardIndexRowCol(oldRow, oldCol)].piece = None

    def move(self, row, col, board):
        self.__changeBoard(row, col, self.row, self.col, board)
        self.row = row
        self.col = col
        self.movescount = self.movescount + 1
