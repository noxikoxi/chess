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

    # def removeMovesIfTied(self, board, player, enemy):
    #     for move in self.moves:
    #         block_piece = board[Block.getBoardIndexRowCol(move[0], move[1])].piece
    #         self.move(move[0], move[1], board)
    #
    #         if block_piece is not None:
    #             enemy.pieces.remove(block_piece)
    #
    #         enemy.updateMoves(self.board, player, attackingOnly=True)
    #
    #         if (king.row, king.col) not in enemy.attackingMoves:
    #             piece.moves.append(move)
    #
    #         if block_piece is not None:
    #             enemy.pieces.append(block_piece)
    #
    #         piece.move(pos[0], pos[1], self.board)
    #         self.board[Block.getBoardIndexRowCol(move[0], move[1])].piece = block_piece
    #
    #     enemy.updateMoves(self.board, player, attackingOnly=False)