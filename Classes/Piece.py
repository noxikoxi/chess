from settings import BLOCK_SIZE
from Classes.Block import Block


def returnValidMoves(moves):
    return [x for x in moves if 0 <= x[0] <= 7 and 0 <= x[1] <= 7]


def checkIfFriendlyPieceInMoves(piece, board, moves):

    for move in moves:
        block_piece = board[Block.getBoardIndexRowCol(move[0], move[1])].piece
        if block_piece:
            if piece.color == block_piece.color:
                moves.remove(move)
    return moves


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
