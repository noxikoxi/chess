import pygame
from Classes.Button import Button
from Game import Game
from server import Server
from client import Client


def updateButtonsPos(screen, buttons, button_width):
    x = screen.get_width() / 2 - button_width / 2

    for button in buttons:
        button.rect.x = x
        button.x = x


class Options:
    def __init__(self, screen, settings):
        self.settings = settings
        button_size = self.settings.large_buttons_size
        buttons_x = screen.get_width() / 2 - self.settings.large_buttons_size[0] / 2

        self.option_1 = Button(buttons_x, 50, button_size[0], button_size[1], "Assets/buttons/600_600.png", 10)
        self.option_2 = Button(buttons_x, 200, button_size[0], button_size[1], "Assets/buttons/800_800.png", 10)
        self.option_3 = Button(buttons_x, 350, button_size[0], button_size[1], "Assets/buttons/1000_1000.png", 10)
        self.back_button = Button(buttons_x, 500, button_size[0], button_size[1], "Assets/buttons/back_button.png", 10)

        self.buttons = [self.option_1, self.option_2, self.option_3, self.back_button]

    def draw(self, screen):
        screen.fill((110, 160, 110))
        for button in self.buttons:
            button.draw(screen)
        pygame.display.update()

    def resize(self, screen):
        updateButtonsPos(screen, self.buttons, self.settings.large_buttons_size[0])


class Menu:
    def __init__(self, settings, isServer=True):
        pygame.init()
        pygame.font.init()
        self.settings = settings
        self.screen = pygame.display.set_mode((self.settings.window_width, self.settings.window_height))
        pygame.display.set_caption("Chess")
        self.font = pygame.font.Font("Fonts/BebasNeue-Regular.ttf", self.settings.font_size)
        self.isServer = isServer

        button_size = self.settings.large_buttons_size
        buttons_x = self.screen.get_width() / 2 - button_size[0] / 2
        buttons_top_margin = 50

        self.new_game = Button(buttons_x, buttons_top_margin,
                               button_size[0], button_size[1], "Assets/buttons/new_game_button.png", 40)
        self.continue_game = Button(buttons_x, self.new_game.rect.bottom + buttons_top_margin,
                                    button_size[0], button_size[1], "Assets/buttons/continue_button.png", 40)
        self.options_button = Button(buttons_x, self.continue_game.rect.bottom + buttons_top_margin,
                                     button_size[0], button_size[1], "Assets/buttons/options_button.png", 40)
        self.quit_button = Button(buttons_x, self.options_button.rect.bottom + buttons_top_margin,
                                  button_size[0], button_size[1], "Assets/buttons/exit_button.png", 40)

        # self.sound_button = Button(600, 600, 75, 75, "Assets/buttons/audio_button.png", 40)

        self.menu_buttons = [self.new_game, self.continue_game, self.options_button, self.quit_button]


        self.game_quit_button = Button(0, 0, self.settings.offset,
                                       self.settings.offset, "Assets/buttons/arrow_left_button.png", 40)

        self.game_state = 'menu'
        self.game = Game(self.screen, self.font, self.settings)
        self.options = Options(self.screen, self.settings)
        self.resize((self.settings.resizing_options[self.settings.picked_options][0],
                     self.settings.resizing_options[self.settings.picked_options][1]))

        self.game_back_to_menu_button = Button(buttons_x, self.screen.get_height() / 2 + 100,
                                               button_size[0], button_size[1], "Assets/buttons/menu_button.png", 40)
        self.save_score_sheet_button = Button(buttons_x, self.screen.get_height() / 2 + 250,
                                              90, 90, "Assets/buttons/save_pgn.png", 40)

        # SERVER
        if isServer:
            self.start_server = Button(0, 50, button_size[0], button_size[1], "Assets/buttons/start_server_button.png", 40)
            self.server = Server()
        else:
            self.client = Client()
            self.connect_button = Button(0, 50, button_size[0], button_size[1], "Assets/buttons/connect_button.png", 40)

    def resize(self, size_tuple):
        self.screen = pygame.display.set_mode((size_tuple[0], size_tuple[1]))
        self.options.resize(self.screen)
        self.game.game_font = pygame.font.Font("Fonts/BebasNeue-Regular.ttf", self.settings.font_size)
        self.game.resizeGameSurface(self.screen)

        updateButtonsPos(self.screen, self.menu_buttons, self.settings.large_buttons_size[0])
        self.game_quit_button.updateRect(0, 0, self.settings.offset, self.settings.offset)

    def showVictoryText(self, who):
        font = pygame.font.Font("Fonts/BebasNeue-Regular.ttf", self.settings.font_size + 25)

        if who == 'white':
            text = 'WHITE WON'
        elif who == 'black':
            text = 'BLACK WON'
        else:
            text = 'DRAW'

        self.screen.blit(font.render(f'{text}', True, 'yellow', ),
                         (self.game.gameSurface.get_width() / 2 - font.size(text)[0] / 2 + self.settings.offset,
                          self.game.gameSurface.get_height() / 2 - font.size(text)[
                              1] / 2 + self.settings.offset))

    def draw(self):
        if self.game_state == 'menu':
            self.screen.fill((90, 90, 90))
            if self.isServer:
                self.start_server.draw(self.screen)
            else:
                self.connect_button.draw(self.screen)
            for button in self.menu_buttons:
                button.draw(self.screen)
            # self.sound_button.draw(self.screen)
        elif self.game_state == 'options':
            self.options.draw(self.screen)
        elif self.game_state == 'play' or self.game_state == 'lan_play':
            self.screen.fill((0, 0, 0))
            self.game_quit_button.draw(self.screen)
            self.game.update()
            self.game.draw()
        elif self.game_state == 'server':
            self.screen.fill((64, 12, 67))
        elif self.game_state == 'game_end':
            self.game_back_to_menu_button.draw(self.screen)
            self.save_score_sheet_button.draw(self.screen)

    def checkButtons(self, pos):
        if self.game_state == 'menu':
            if self.new_game.isClicked(pos):
                self.game_state = 'play'
                self.game.reset()
                self.save_score_sheet_button.pressed = False
            elif self.continue_game.isClicked(pos):
                self.game_state = 'play'
            elif self.isServer and self.start_server.isClicked(pos):
                self.game_state = 'server'
                self.server.start_server()
                self.draw()
                pygame.display.update()
                self.server.wait_for_client()
                self.game_state = 'lan_play'
            elif not self.isServer and self.connect_button.isClicked(pos):
                self.client.connect_with_server()
                self.game_state = 'lan_play'
            elif self.options_button.isClicked(pos):
                self.game_state = 'options'
            elif self.quit_button.isClicked(pos):
                pygame.event.post(pygame.event.Event(pygame.QUIT))
        elif self.game_state == 'options':
            if self.options.back_button.isClicked(pos):
                self.game_state = 'menu'
            elif self.options.option_1.isClicked(pos):
                self.settings.changeSettings(0)
                self.resize((self.settings.resizing_options[self.settings.picked_options][0],
                             self.settings.resizing_options[self.settings.picked_options][1]))
            elif self.options.option_2.isClicked(pos):
                self.settings.changeSettings(1)
                self.resize((self.settings.resizing_options[self.settings.picked_options][0],
                             self.settings.resizing_options[self.settings.picked_options][1]))

            elif self.options.option_3.isClicked(pos):
                self.settings.changeSettings(2)
                self.resize((self.settings.resizing_options[self.settings.picked_options][0],
                             self.settings.resizing_options[self.settings.picked_options][1]))
        elif self.game_state == 'game_end':
            if self.save_score_sheet_button.isClicked(pos) and not self.save_score_sheet_button.pressed:
                self.game.score_sheet.saveSheet()
                self.save_score_sheet_button.pressed = True
            elif self.game_back_to_menu_button.isClicked(pos):
                self.game_state = 'menu'


