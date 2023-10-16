import pygame


class Button:
    def __init__(self, x, y, width, height, image, font_size):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.original_image = image
        self.image = pygame.transform.scale(pygame.image.load(self.original_image).convert_alpha(), (width, height))
        self.font_size = font_size
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.clicked = False

    def isClicked(self, pos):
        return True if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] else False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def updateRect(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.image = pygame.transform.scale(pygame.image.load(self.original_image).convert_alpha(), (width, height))


