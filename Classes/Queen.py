from pygame.image import load
from pygame import transform
from Classes.Piece import Piece
from Classes.Rook import Rook
from Classes.Bishop import Bishop
from settings import BLOCK_SIZE


class Queen(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        temp = 'white_queen.png' if color == 'white' else 'black_queen.png'
        self.image = transform.scale(load(f'Assets/{temp}').convert_alpha(), (BLOCK_SIZE, BLOCK_SIZE))

    def getPossibleMoves(self):
        moves = []
        a1 = Rook(self.row, self.col, self.color)
        a2 = Bishop(self.row, self.col, self.color)
        moves = moves + Rook.getPossibleMoves(a1)
        moves = moves + Bishop.getPossibleMoves(a2)
        return moves