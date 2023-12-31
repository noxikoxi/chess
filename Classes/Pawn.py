import pygame.event
from Classes.Piece import Piece, returnValidMoves, checkValidRange, Block
from settings import PAWN_UPGRADE


def checkIfFreeBlock(board, row, col, distance=1):
    if checkValidRange(row - distance, col) is not True:
        return None
    return board[Block.getBoardIndexRowCol(row - distance, col)].piece is None


def checkIfEnemy(board, color, row, col):
    if checkValidRange(row, col) is not True:
        return None
    return board[Block.getBoardIndexRowCol(row, col)].piece.color != color


class Pawn(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.image_path = 'white_pawn.png' if color == 'white' else 'black_pawn.png'
        self.doubleMoveTurn = -1

    def getPossibleMoves(self, board):
        moves = []
        if self.color == 'white':
            if checkIfFreeBlock(board, self.row, self.col):
                moves = moves + [(self.row - 1, self.col)]
                if self.row == 6 and checkIfFreeBlock(board, self.row, self.col, 2):
                    moves = moves + [(self.row - 2, self.col)]

            # Check if enemy in front of pawn
            if checkIfFreeBlock(board, self.row, self.col - 1) is False and checkIfEnemy(board, self.color, self.row - 1, self.col - 1):
                moves = moves + [(self.row - 1, self.col - 1)]
            if checkIfFreeBlock(board, self.row, self.col + 1) is False and checkIfEnemy(board, self.color, self.row - 1, self.col + 1):
                moves = moves + [(self.row - 1, self.col + 1)]

        # For black pawns
        else:
            if checkIfFreeBlock(board, self.row, self.col, distance=-1):
                moves = moves + [(self.row + 1, self.col)]
                if self.row == 1 and checkIfFreeBlock(board, self.row, self.col, distance=-2):
                    moves = moves + [(self.row + 2, self.col)]

            # Check if enemy in front of pawn
            if checkIfFreeBlock(board, self.row, self.col - 1, distance=-1) is False and checkIfEnemy(board, self.color, self.row + 1, self.col - 1):
                moves = moves + [(self.row + 1, self.col - 1)]
            if checkIfFreeBlock(board, self.row, self.col + 1, distance=-1) is False and checkIfEnemy(board, self.color, self.row + 1, self.col + 1):
                moves = moves + [(self.row + 1, self.col + 1)]

        return returnValidMoves(moves)

    def getAttackedBlocks(self):
        x = -1 if self.color == 'white' else 1

        return returnValidMoves([(self.row + x, self.col + x), (self.row + x, self.col - x)])

    def move(self, row, col, board):
        super().move(row, col, board)
        if self.color == 'white' and self.row == 0 or self.color == 'black' and self.row == 7:
            pygame.event.post(pygame.event.Event(PAWN_UPGRADE))


