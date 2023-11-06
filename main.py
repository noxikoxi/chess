import sys

import pygame
from menu import Menu
from settings import Settings, WHITE_WON, DRAW, BLACK_WON, WHITE_MOVE, BLACK_MOVE

if not 1 < len(sys.argv) < 3:
    print(f'Error\nUsage: python main.py [server/client]')
    sys.exit()

if sys.argv[1] == 'server':
    isServer = True
else:
    isServer = False

settings = Settings()
menu = Menu(settings, isServer)

firstMove = True


# Game loop
while True:
    if not isServer and firstMove and menu.game.score_sheet.turns % 2 == 0 and menu.client.isConnected:
        move = menu.client.waitForData()
        menu.game.makeMove(move)
        firstMove = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            pygame.font.quit()
            if menu.isServer:
                del menu.server
            else:
                del menu.client
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

        if menu.game_state == 'lan_play':
            if event.type == WHITE_MOVE:
                menu.server.sendData(menu.game.lastMove)
                print('data was sent')
                move = menu.server.waitForData()
                menu.game.makeMove(move)
            elif event.type == BLACK_MOVE:
                menu.client.sendData(menu.game.lastMove)
                print('data was sent')
                move = menu.client.waitForData()
                menu.game.makeMove(move)

        if event.type == pygame.MOUSEBUTTONUP:
            if menu.game_state == 'play' or menu.game_state == 'lan_play':
                pos = pygame.mouse.get_pos()
                if menu.game_quit_button.isClicked(pos):
                    menu.game_state = 'menu'
                if menu.game_state == 'lan_play':
                    if isServer and menu.game.score_sheet.turns % 2 == 0:
                        menu.game.checkMouse(pos)
                    elif not isServer and menu.game.score_sheet.turns % 2 == 1:
                        menu.game.checkMouse(pos)
                else:
                    menu.game.checkMouse(pos)
            else:
                pos = pygame.mouse.get_pos()
                menu.checkButtons(pos)

    menu.draw()
    pygame.display.update()


