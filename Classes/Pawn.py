import pygame
from Classes.Piece import Piece


class Pawn(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color, None)
        temp = 'white_pawn.png' if color == 'white' else 'black_pawn.png'
        self.image = pygame.transform.scale(pygame.image.load(f'Assets/{temp}').convert_alpha(), (100, 100))
