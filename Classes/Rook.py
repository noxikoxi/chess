from pygame.image import load
from pygame import transform
from Classes.Piece import Piece
from settings import BLOCK_SIZE

class Rook(Piece):

    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        temp = 'white_rook.png' if color == 'white' else 'black_rook.png'
        self.image = transform.scale(load(f'Assets/{temp}').convert_alpha(), (BLOCK_SIZE, BLOCK_SIZE))

