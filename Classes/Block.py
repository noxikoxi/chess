from pygame import draw
from pygame import Rect
from pygame.image import load
from pygame.transform import scale


class Block:
    def __init__(self, row, col, color, settings, piece=None):
        self.rect = None
        self.row = row
        self.col = col
        self.piece = piece
        self.color = color
        self.naturalColor = color
        self.settings = settings
        self.updateRect()

    def glow(self):
        self.color = (0, 220, 32)
        self.updateRect()
        # self.active = True

    def danger(self):
        self.color = (240, 0, 50)
        self.updateRect()
        # self.active = True

    def resetColor(self):
        self.color = self.naturalColor
        self.updateRect()
        # self.active = False

    def updateRect(self):
        self.rect = Rect(int(self.settings.block_size * self.col), int(self.settings.block_size * self.row),
                         self.settings.block_size, self.settings.block_size)

    @staticmethod
    def getBoardIndexXY(x, y, offset, block_size):
        return int(((y - offset) // block_size) * 8 + ((x - offset) // block_size) * 1)

    @staticmethod
    def getBoardIndexRowCol(row, col):
        return col * 1 + row * 8


class ImageBlock:
    def __init__(self, x, y, color, settings, piece_name):
        asset_path = f'Assets/pieces/{color}_{piece_name}.png'
        self.x = x
        self.y = y
        self.piece_name = piece_name
        self.image = scale(load(asset_path).convert_alpha(), (settings.block_size - 10, settings.block_size - 10))
        self.rect = Rect(x + 2, y + 2, settings.block_size - 2, settings.block_size - 4)

    def draw(self, surface):
        draw.rect(surface, 'yellow', self.rect)
        surface.blit(self.image, (self.x + 5, self.y + 5))

