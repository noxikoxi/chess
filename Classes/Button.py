import pygame


class Button:
    def __init__(self, x, y, width, height, image, font_size):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.image.load(image)
        self.font_size = font_size
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
