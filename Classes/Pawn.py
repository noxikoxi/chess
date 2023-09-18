from pygame.image import load
from pygame import transform
from Classes.Piece import Piece
from settings import BLOCK_SIZE


class Pawn(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        temp = 'white_pawn.png' if color == 'white' else 'black_pawn.png'
        self.image = transform.scale(load(f'Assets/{temp}').convert_alpha(), (BLOCK_SIZE, BLOCK_SIZE))
        self.firstMove = True

    def getPossibleMoves(self):
        if self.color == 'white':
            if self.firstMove:
                return [(self.row - 1, self.col), (self.row - 2, self.col)]
            else:
                return [(self.row - 1, self.col)]
        else:
            if self.firstMove:
                return [(self.row + 1, self.col), (self.row + 2, self.col)]
            else:
                return [(self.row + 1, self.col)]

    def move(self, row, col):
        super().move(row, col)
        if self.firstMove:
            self.firstMove = False

