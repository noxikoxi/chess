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
        self.naturalColor = color
        self.active = False
        self.__updateRect()

    def glow(self):
        self.color = (0, 220, 32)
        self.__updateRect()
        self.active = True

    def danger(self):
        self.color = (240, 0, 50)
        self.__updateRect()
        self.active = True

    def resetColor(self):
        self.color = self.naturalColor
        self.__updateRect()
        self.active = False

    def __updateRect(self):
        self.rect = pygame.Rect(int(BLOCK_SIZE * self.col), int(BLOCK_SIZE * self.row), BLOCK_SIZE, BLOCK_SIZE)

    @staticmethod
    def getBoardIndexXY(x, y):
        return int(((y - OFFSET) // BLOCK_SIZE) * 8 + ((x - OFFSET) // BLOCK_SIZE) * 1)

    @staticmethod
    def getBoardIndexRowCol(row, col):
        return col * 1 + row * 8


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.gameSurface = pygame.Surface((WINDOW_WIDTH-OFFSET, WINDOW_HEIGHT-OFFSET))
        self.turns = 0
        self.selectedPiece = None  # Only one block may be active at one time

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

        # Connect pieces with blocks
        for piece in self.player.pieces:
            self.board[piece.getSquare()].piece = piece

        for piece in self.player2.pieces:
            self.board[piece.getSquare()].piece = piece

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

    def checkMouse(self):
        mouse_pos = pygame.mouse.get_pos()

        # mouse cursor is in game board
        if OFFSET <= mouse_pos[0] < WINDOW_WIDTH and OFFSET <= mouse_pos[1] < WINDOW_HEIGHT:
            selected_block = self.board[Block.getBoardIndexXY(mouse_pos[0], mouse_pos[1])]

            if selected_block.piece is not None:  # Block has a piece
                print("selected")
                if selected_block.active:  # Reset colors
                    selected_block.resetColor()
                    self.__showPossibleMoves()
                    self.selectedPiece = None
                elif self.selectedPiece is None:  # Block is not active, and we don't have selected piece
                    selected_block.glow()
                    self.selectedPiece = selected_block.piece
                    self.__showPossibleMoves()
            elif self.selectedPiece is not None:
                moves = self.selectedPiece.getPossibleMoves()
                if (selected_block.row, selected_block.col) in moves:  # make a move
                    # print(f'PIECE -> {self.selectedPiece.row},{self.selectedPiece.col}')
                    # print(f'BLOCK -> {selected_block.row},{selected_block.col}')

                    # Reset active blocks
                    self.board[Block.getBoardIndexRowCol(self.selectedPiece.row, self.selectedPiece.col)].resetColor()
                    self.__showPossibleMoves()
                    # Change Piece pos in board
                    self.__changeBoard(self.selectedPiece, selected_block.row, selected_block.col,
                                       self.selectedPiece.row, self.selectedPiece.col)
                    # Move
                    self.selectedPiece.move(selected_block.row, selected_block.col)
                    self.selectedPiece = None

    def __changeBoard(self, piece, row, col, oldRow, oldCol):
        self.board[Block.getBoardIndexRowCol(row, col)].piece = piece
        self.board[Block.getBoardIndexRowCol(oldRow, oldCol)].piece = None
        # print(row, col ,oldRow, oldCol)
        # print(f'NEW -> {Block.getBoardIndexRowCol(row, col)}')
        # print(f'OLD -> {Block.getBoardIndexRowCol(oldRow, oldCol)}')

    def __showPossibleMoves(self):
        for move in self.selectedPiece.getPossibleMoves():  # Check if move is valid
            if 7 < move[0] < 0 or 7 < move[1] < 0:
                continue
            block = self.board[Block.getBoardIndexRowCol(move[0], move[1])]

            if block.piece is not None:
                if self.turns == 0:
                    if block.piece.color == 'black' and not block.active:
                        block.danger()
                    else:
                        block.resetColor()
            elif not block.active:
                block.glow()
            else:
                block.resetColor()

    def update(self):
        pass

    def run(self):
        while True:
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    pygame.font.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONUP:
                    self.checkMouse()

            self.update()
            self.draw()
            pygame.display.update()


if __name__ == "__main__":
    gra = Game()
    gra.reset()
    gra.run()
