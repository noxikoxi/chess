import sys

import pygame
from menu import Menu

pygame.init()
pygame.font.init()
menu = Menu()

menu.draw()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            pygame.font.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            menu.checkButtons(mouse_pos)

