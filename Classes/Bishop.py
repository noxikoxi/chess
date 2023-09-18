from pygame.image import load
from pygame import transform
from Classes.Piece import Piece
from settings import BLOCK_SIZE


class Bishop(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        temp = 'white_bishop.png' if color == 'white' else 'black_bishop.png'
        self.image = transform.scale(load(f'Assets/{temp}').convert_alpha(), (BLOCK_SIZE, BLOCK_SIZE))
