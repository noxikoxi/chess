import sys

import pygame
from menu import Menu
from settings import Settings

settings = Settings()
menu = Menu(settings)

# Game loop
while True:

    if menu.game_state != 'play':
        menu.checkButtons()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            pygame.font.quit()
            sys.exit()

        if menu.game_state == 'play':
            if event.type == pygame.MOUSEBUTTONUP:
                menu.game.checkMouse()

    menu.draw()
    pygame.display.update()
