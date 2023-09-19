import pygame.event
from pygame.image import load
from pygame import transform
from Classes.Piece import Piece, returnValidMoves
from settings import BLOCK_SIZE, PAWN_UPGRADE
from main import Block


def checkIfFreeBlock(board, row, col, distance=1):
    return board[Block.getBoardIndexRowCol(row - distance, col)].piece is None


def checkIfEnemy(board, color, row, col):
    return board[Block.getBoardIndexRowCol(row, col)].piece.color != color


class Pawn(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        temp = 'white_pawn.png' if color == 'white' else 'black_pawn.png'
        self.image = transform.scale(load(f'Assets/{temp}').convert_alpha(), (BLOCK_SIZE, BLOCK_SIZE))
        self.firstMove = True

    def getPossibleMoves(self, board):
        moves = []
        if self.color == 'white':
            if checkIfFreeBlock(board, self.row, self.col):
                moves = moves + [(self.row - 1, self.col)]
                if self.firstMove and checkIfFreeBlock(board, self.row, self.col, 2):
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
                if self.firstMove and checkIfFreeBlock(board, self.row, self.col, distance=-2):
                    moves = moves + [(self.row + 2, self.col)]

            # Check if enemy in front of pawn
            if checkIfFreeBlock(board, self.row, self.col - 1, distance=-1) is False and checkIfEnemy(board, self.color, self.row + 1, self.col - 1):
                moves = moves + [(self.row + 1, self.col - 1)]
            if checkIfFreeBlock(board, self.row, self.col + 1, distance=-1) is False and checkIfEnemy(board, self.color, self.row + 1, self.col + 1):
                moves = moves + [(self.row + 1, self.col + 1)]

        return returnValidMoves(moves)

    def move(self, row, col):
        super().move(row, col)
        if self.color == 'white' and self.row == 0 or self.color == 'black' and self.row == 7:
            pygame.event.post(pygame.event.Event(PAWN_UPGRADE))
        if self.firstMove:
            self.firstMove = False
