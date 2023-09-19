from pygame.image import load
from pygame import transform
from Classes.Piece import Piece, returnValidMoves, checkStackMoves
from settings import BLOCK_SIZE


class King(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        temp = 'white_king.png' if color == 'white' else 'black_king.png'
        self.image = transform.scale(load(f'Assets/{temp}').convert_alpha(), (BLOCK_SIZE, BLOCK_SIZE))

    def getPossibleMoves(self, board):
        return checkStackMoves(self.color, returnValidMoves([(self.row + 1, self.col - 1), (self.row + 1, self.col),
                                                             (self.row + 1, self.col + 1), (self.row, self.col + 1),
                                                             (self.row - 1, self.col + 1), (self.row - 1, self.col),
                                                             (self.row - 1, self.col - 1), (self.row, self.col - 1)]),
                               board)
