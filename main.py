import pygame
import sys
from Classes.Players import Player
from settings import BLOCK_SIZE, WINDOW_HEIGHT, WINDOW_WIDTH, BOARD_COLORS, FONT_COLOR, OFFSET


class Block:
    def __init__(self, row, col, color, piece=None,):
        self.row = row
        self.col = col
        self.piece = piece
        self.color = color
        self.__updateRect()

    def glow(self):
        self.color = (0, 220, 32)
        self.__updateRect()

    def danger(self):
        self.color = (240, 0, 50)
        self.__updateRect()

    def __updateRect(self):
        self.rect = pygame.Rect(int(BLOCK_SIZE * self.col), int(BLOCK_SIZE * self.row), BLOCK_SIZE, BLOCK_SIZE)


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.gameSurface = pygame.Surface((WINDOW_WIDTH-OFFSET, WINDOW_HEIGHT-OFFSET))
        self.turns = 0

        pygame.display.set_caption('Chess')
        self.game_font = pygame.font.Font("Fonts/BebasNeue-Regular.ttf", 70)

        self.board = []
        row = 0
        for col in range(64):
            self.board.append(Block(row, col % 8, BOARD_COLORS[0] if (row+col) % 2 == 0 else BOARD_COLORS[1]))
            if col % 8 == 7 and col != 0:
                row += 1

        self.player = Player('white', 0)
        self.player2 = Player('black', 0)

    def reset(self):
        self.player.fillPieces()
        self.player2.fillPieces()
        self.turns = 0

    def draw(self):
        # background
        for block in self.board:
            pygame.draw.rect(self.gameSurface, block.color, block.rect)
        # Text
        for i in range(8):
            self.display_surface.blit(self.game_font.render(f'{i+1}', False, FONT_COLOR),
                                      (OFFSET/4, i * BLOCK_SIZE + OFFSET + 10))
        for i, text in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']):
            self.display_surface.blit(self.game_font.render(f'{text}', False, FONT_COLOR),
                                      (i * BLOCK_SIZE + OFFSET + BLOCK_SIZE/2 - 15, -10))
        # Pieces
        for piece in self.player.pieces:
            self.gameSurface.blit(piece.image, piece.getRealXY())

        for piece in self.player2.pieces:
            self.gameSurface.blit(piece.image, piece.getRealXY())

        self.display_surface.blit(self.gameSurface, (OFFSET, OFFSET))

    def run(self):
        while True:
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    pygame.font.quit()
                    sys.exit()
            self.draw()
            pygame.display.update()


if __name__ == "__main__":
    gra = Game()
    gra.reset()
    gra.run()
