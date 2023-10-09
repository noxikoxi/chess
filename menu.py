import pygame
from Classes.Button import Button
from Game import Game
from settings import WINDOW_HEIGHT, WINDOW_WIDTH, FONT_SIZE, RESIZING_OPTIONS


class Options:
    def __init__(self, screen, font):
        self.screen = screen
        self.back_button = Button(screen.get_width() / 2 - 100, 50, 200, 100, "Assets/quit.png", 10)
        self.resize_button = Button(screen.get_width() / 2 - 100, 200, 200, 100, "Assets/play.png", 10)

    def draw(self):
        self.screen.fill((40, 120, 20))
        self.back_button.draw(self.screen)
        self.resize_button.draw(self.screen)
        pygame.display.update()


class Menu:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Chess")
        self.font = pygame.font.Font("Fonts/BebasNeue-Regular.ttf", FONT_SIZE)
        self.play_button = Button(50, 170, 200, 100, "Assets/play.png", 40)
        self.options_button = Button(50, 300, 200, 100, "Assets/options.png", 40)
        self.quit_button = Button(50, 430, 200, 100, "Assets/quit.png", 40)
        self.sound_button = Button(600, 600, 75, 75, "Assets/sound_on.png", 40)

        self.game_state = 'menu'
        self.game = Game(self.screen, self.font)
        self.options = Options(self.screen, self.font)

    def resize(self, size_tuple):
        self.screen = pygame.display.set_mode((size_tuple[0], size_tuple[1]))

    def draw(self):
        if self.game_state == 'menu':
            self.screen.fill((0, 204, 0))
            self.play_button.draw(self.screen)
            self.options_button.draw(self.screen)
            self.quit_button.draw(self.screen)
            self.sound_button.draw(self.screen)
        elif self.game_state == 'options':
            self.options.draw()
        elif self.game_state == 'play':
            self.screen.fill((0, 0, 0))
            self.game.draw()
            self.game.update()

    def checkButtons(self):
        pos = pygame.mouse.get_pos()

        if self.game_state == 'menu':
            if self.play_button.isClicked(pos):
                self.game_state = 'play'
            elif self.options_button.isClicked(pos):
                self.game_state = 'options'
            elif self.quit_button.isClicked(pos):
                pygame.event.post(pygame.event.Event(pygame.QUIT))
        elif self.game_state == 'options':
            if self.options.back_button.isClicked(pos):
                self.game_state = 'menu'
            elif self.options.resize_button.isClicked(pos):
                self.resize(RESIZING_OPTIONS[1])
