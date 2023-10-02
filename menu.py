import pygame
from Classes.Button import Button

pygame.init()

SCREEN_WIDTH = 700
SCREEN_LENGTH = 700
TEXT_COL = (204, 102, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_LENGTH))
pygame.display.set_caption("Main Menu")
pygame.game_font = pygame.font.Font("Fonts/BebasNeue-Regular.ttf", 20)

while True:
    MOUSE_POS = pygame.mouse.get_pos()

    screen.fill((0, 204, 0))
    PLAY_BUTTON = Button(50, 170, 200, 100, "Assets/play.png", 40)
    OPTIONS_BUTTON = Button(50, 300, 200, 100, "Assets/options.png", 40)
    QUIT_BUTTON = Button(50, 430, 200, 100, "Assets/quit.png", 40)
    SOUND_BUTTON = Button(600, 600, 75, 75, "Assets/sound_on.png", 40)
    PLAY_BUTTON.draw(screen)
    OPTIONS_BUTTON.draw(screen)
    QUIT_BUTTON.draw(screen)
    SOUND_BUTTON.draw(screen)
    pygame.display.update()

    for event in pygame.event.get():
        if pygame.event == pygame.QUIT:
            pygame.quit()

