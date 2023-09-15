import pygame
import sys

WINDOW_HEIGHT, WINDOW_WIDTH = 800, 800
BLOCK_SIZE = WINDOW_WIDTH / 8


class Block:
    def __init__(self, x, y, color, piece=None,):
        self.x = x
        self.y = y
        self.piece = piece
        self.color = color
        self.rect = pygame.Rect(int(BLOCK_SIZE*x), int(BLOCK_SIZE*y), BLOCK_SIZE, BLOCK_SIZE)


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Chess')

        self.board = []
        j = 0
        for i in range(64):
            self.board.append(Block(i % 8, j, 'GRAY' if (j+i) % 2 == 0 else (150, 120, 160)))
            if i % 8 == 7 and i != 0:
                j = j + 1

        for i in range(64):
            print(f'Block: x->{self.board[i].x}, y->{self.board[i].y}')

    def draw(self):
        for block in self.board:
            pygame.draw.rect(self.display_surface, block.color, block.rect)

    def run(self):
        while True:
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.draw()
            pygame.display.update()


if __name__ == "__main__":
    gra = Game()
    gra.run()
