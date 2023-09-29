from pygame import USEREVENT

OFFSET = 60
WINDOW_HEIGHT, WINDOW_WIDTH = 700, 700
BLOCK_SIZE = (WINDOW_WIDTH-OFFSET) / 8
BOARD_COLORS = ('gray', (150, 120, 160))
FONT_COLOR = (255, 255, 255)

PAWN_UPGRADE = USEREVENT + 0
CASTLING = USEREVENT + 1
ATTACK = USEREVENT + 2