import pygame
from Classes.Button import Button
from Game import Game


class Options:
    def __init__(self, screen):
        self.option_1 = Button(screen.get_width() / 2 - 100, 50, 200, 100, "Assets/window_option1.png", 10)
        self.option_2 = Button(screen.get_width() / 2 - 100, 200, 200, 100, "Assets/window_option2.png", 10)
        self.option_3 = Button(screen.get_width() / 2 - 100, 350, 200, 100, "Assets/window_option3.png", 10)
        self.back_button = Button(screen.get_width() / 2 - 100, 500, 200, 100, "Assets/quit.png", 10)

    def draw(self, screen):
        screen.fill((40, 120, 20))
        self.option_1.draw(screen)
        self.option_2.draw(screen)
        self.option_3.draw(screen)
        self.back_button.draw(screen)
        pygame.display.update()

    def resize(self, screen):
        width = screen.get_width()
        button_width = 200
        self.option_1.updateRect(width / 2 - button_width/2, 50, button_width, 100)
        self.option_2.updateRect(width / 2 - button_width/2, 200, button_width, 100)
        self.option_3.updateRect(width / 2 - button_width/2, 350, button_width, 100)
        self.back_button.updateRect(width / 2 - button_width/2, 500, button_width, 100)


class Menu:
    def __init__(self, settings):
        pygame.init()
        pygame.font.init()
        self.settings = settings
        self.screen = pygame.display.set_mode((self.settings.window_width, self.settings.window_height))
        pygame.display.set_caption("Chess")

        self.font = pygame.font.Font("Fonts/BebasNeue-Regular.ttf", self.settings.font_size)
        self.play_button = Button(50, 170, 200, 100, "Assets/play.png", 40)
        self.options_button = Button(50, 300, 200, 100, "Assets/options.png", 40)
        self.quit_button = Button(50, 430, 200, 100, "Assets/quit.png", 40)
        self.sound_button = Button(600, 600, 75, 75, "Assets/sound_on.png", 40)
        # self.game_quit_button = Button(10, 10, self.settings.block_size - 20, self.settings.block_size-20)

        self.game_state = 'menu'
        self.game = Game(self.screen, self.font, self.settings)
        self.options = Options(self.screen)
        self.resize((self.settings.resizing_options[self.settings.picked_options][0],
                     self.settings.resizing_options[self.settings.picked_options][1]))

    def resize(self, size_tuple):
        self.screen = pygame.display.set_mode((size_tuple[0], size_tuple[1]))
        self.options.resize(self.screen)
        self.game.game_font = pygame.font.Font("Fonts/BebasNeue-Regular.ttf", self.settings.font_size)
        self.game.resizeGameSurface(self.screen)

    def draw(self):
        if self.game_state == 'menu':
            self.screen.fill((0, 204, 0))
            self.play_button.draw(self.screen)
            self.options_button.draw(self.screen)
            self.quit_button.draw(self.screen)
            self.sound_button.draw(self.screen)
        elif self.game_state == 'options':
            self.options.draw(self.screen)
        elif self.game_state == 'play':
            self.game.changeGameSettings(self.settings)
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
            elif self.options.option_1.isClicked(pos):
                self.resize((self.settings.resizing_options[self.settings.picked_options][0],
                            self.settings.resizing_options[self.settings.picked_options][1]))
                self.settings.changeSettings(0)
            elif self.options.option_2.isClicked(pos):
                self.resize((self.settings.resizing_options[self.settings.picked_options][0],
                            self.settings.resizing_options[self.settings.picked_options][1]))
                self.settings.changeSettings(1)
            elif self.options.option_3.isClicked(pos):
                self.resize((self.settings.resizing_options[self.settings.picked_options][0],
                            self.settings.resizing_options[self.settings.picked_options][1]))
                self.settings.changeSettings(2)
