import pygame
from Classes.Button import Button
from Game import Game
from settings import WINDOW_HEIGHT, WINDOW_WIDTH


class Menu:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Main Menu")
        pygame.game_font = pygame.font.Font("Fonts/BebasNeue-Regular.ttf", 20)
        self.play_button = Button(50, 170, 200, 100, "Assets/play.png", 40)
        self.options_button = Button(50, 300, 200, 100, "Assets/options.png", 40)
        self.quit_button = Button(50, 430, 200, 100, "Assets/quit.png", 40)
        self.sound_button = Button(600, 600, 75, 75, "Assets/sound_on.png", 40)

    def draw(self):
        self.screen.fill((0, 204, 0))
        self.play_button.draw(self.screen)
        self.options_button.draw(self.screen)
        self.quit_button.draw(self.screen)
        self.sound_button.draw(self.screen)
        pygame.display.update()

    def checkButtons(self, pos):
        if self.play_button.rect.collidepoint(pos):
            gra = Game()
            gra.run()
