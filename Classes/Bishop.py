from pygame.image import load
from pygame import transform
from Classes.Piece import Piece
from settings import BLOCK_SIZE


class Bishop(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        temp = 'white_bishop.png' if color == 'white' else 'black_bishop.png'
        self.image = transform.scale(load(f'Assets/{temp}').convert_alpha(), (BLOCK_SIZE, BLOCK_SIZE))

    def getPossibleMoves(self):
        moves = []
        for x in range(16):
            moves.append((self.row - 8 + x, self.col - 8 + x))
            moves.append((self.row - 8 + x, self.col + 8 - x))
        return moves
