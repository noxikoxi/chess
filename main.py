import pygame
import sys
from Classes.Players import *
from Classes.Block import Block
from settings import BLOCK_SIZE, WINDOW_HEIGHT, WINDOW_WIDTH, BOARD_COLORS, FONT_COLOR, OFFSET

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.gameSurface = pygame.Surface((WINDOW_WIDTH-OFFSET, WINDOW_HEIGHT-OFFSET))
        self.turns = 0
        self.selectedPiece = None  # Only one piece may be active at one time

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
            if selected_block.piece is None and self.selectedPiece is None:
                pass
            elif selected_block.piece is not None and self.selectedPiece is None:  # Select
                # Select a piece
                selected_block.glow()
                self.selectedPiece = selected_block.piece
                self.__showPossibleMoves()
            elif selected_block.piece == self.selectedPiece:  # Undo select and reset colors
                selected_block.resetColor()
                self.__showPossibleMoves(reset=True)
                self.selectedPiece = None
            elif self.selectedPiece is not None:  # make a move
                moves = self.selectedPiece.getPossibleMoves(self.board)

                if (selected_block.row, selected_block.col) in moves:  # make a move
                    # Reset active blocks
                    self.board[Block.getBoardIndexRowCol(self.selectedPiece.row, self.selectedPiece.col)].resetColor()
                    self.__showPossibleMoves(reset=True)

                    if selected_block.piece is not None and selected_block.piece.color != self.selectedPiece.color: # attack
                        if selected_block.piece.color == 'white':
                            self.player.pieces.remove(selected_block.piece)
                        else:
                            self.player2.pieces.remove(selected_block.piece)
                    # Change Piece pos in board
                    self.__changeBoard(self.selectedPiece, selected_block.row, selected_block.col,
                                       self.selectedPiece.row, self.selectedPiece.col)
                    # Move
                    self.selectedPiece.move(selected_block.row, selected_block.col)
                    self.selectedPiece = None

    def __changeBoard(self, piece, row, col, oldRow, oldCol):
        self.board[Block.getBoardIndexRowCol(row, col)].piece = piece
        self.board[Block.getBoardIndexRowCol(oldRow, oldCol)].piece = None

    def __showPossibleMoves(self, reset=False):
        moves = self.selectedPiece.getPossibleMoves(self.board)

        for move in moves:
            block = self.board[Block.getBoardIndexRowCol(move[0], move[1])]
            if reset:
                block.resetColor()
            else:
                if block.piece is not None:
                    if block.piece.color != self.selectedPiece.col:
                        print(block.piece.color)
                        print(self.selectedPiece.color)
                        block.danger()
                else:
                    block.glow()

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
