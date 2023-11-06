import sys

import pygame
from menu import Menu
from settings import Settings, WHITE_WON, DRAW, BLACK_WON

settings = Settings()
menu = Menu(settings)

# Game loop
while True:

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

        if event.type == pygame.MOUSEBUTTONUP:
            if menu.game_state == 'play':
                pos = pygame.mouse.get_pos()
                if menu.game_quit_button.isClicked(pos):
                    menu.game_state = 'menu'
                else:
                    menu.game.checkMouse(pos)
            else:
                pos = pygame.mouse.get_pos()
                menu.checkButtons(pos)

    menu.draw()
    pygame.display.update()
