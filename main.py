import sys

import pygame
from menu import Menu
from settings import Settings, WHITE_WON, DRAW, BLACK_WON

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

        if event.type == WHITE_WON:
            menu.game_state = 'game_end'
            menu.showVictoryText('white')
        elif event.type == BLACK_WON:
            menu.game_state = 'game_end'
            menu.showVictoryText('black')
        elif event.type == DRAW:
            menu.game_state = 'game_end'
            menu.showVictoryText('draw')

        if menu.game_state == 'play':
            if event.type == pygame.MOUSEBUTTONUP:
                menu.game.checkMouse()

    menu.draw()
    pygame.display.update()
