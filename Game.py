import pygame

from Classes.Block import Block, ImageBlock
from Classes.Players import *
from Classes.ScoreSheet import ScoreSheet
from settings import *


class PromotionBox:
    def __init__(self, screen, settings, selectedPiece):
        self.blocks = None
        self.screen = screen
        self.settings = settings
        self.selectedPiece = selectedPiece

        self.upgradeSurface = pygame.Surface((self.settings.block_size * 4, self.settings.block_size))
        self.upgradeSurface_realX = self.screen.get_width() / 2 - self.upgradeSurface.get_width() / 2
        self.upgradeSurface_realY = self.screen.get_height() / 2 - self.upgradeSurface.get_height() / 2

        self.__updateBlocks('white')

    def draw(self):
        for i in range(len(self.blocks)):
            self.blocks[i].draw(self.upgradeSurface)

        self.screen.blit(self.upgradeSurface, (self.upgradeSurface_realX, self.upgradeSurface_realY))

    def updateSelectedPiece(self, selectedPiece):
        self.selectedPiece = selectedPiece
        self.__updateBlocks(self.selectedPiece.color)

    def __updateBlocks(self, color):
        self.blocks = [ImageBlock(0, 0, color, self.settings, 'queen'),
                       ImageBlock(self.settings.block_size, 0, color, self.settings, 'rook'),
                       ImageBlock(2 * self.settings.block_size - 1, 0, color, self.settings, 'knight'),
                       ImageBlock(3 * self.settings.block_size - 1, 0, color, self.settings, 'bishop'), ]

    def checkMouse(self):
        pos = pygame.mouse.get_pos()
        pos = (pos[0] - self.upgradeSurface_realX, pos[1] - self.upgradeSurface_realY)

        for block in self.blocks:
            if block.rect.collidepoint(pos):
                match block.piece_name:
                    case 'rook':
                        piece = Rook
                    case 'queen':
                        piece = Queen
                    case 'bishop':
                        piece = Bishop
                    case 'knight':
                        piece = Knight
                    case _:
                        piece = Pawn
                return piece
        return None

    def resizeBox(self):
        self.upgradeSurface = pygame.Surface((self.settings.block_size * 4, self.settings.block_size))
        self.upgradeSurface_realX = self.screen.get_width() / 2 - self.upgradeSurface.get_width() / 2
        self.upgradeSurface_realY = self.screen.get_height() / 2 - self.upgradeSurface.get_height() / 2


class Game:
    def __init__(self, screen, font, settings):
        self.settings = settings
        pygame.mixer.pre_init(44100, -16, 2, 512)
        self.score_sheet = ScoreSheet()
        self.display_surface = screen
        self.gameSurface = pygame.Surface((screen.get_width() - self.settings.offset,
                                           screen.get_height() - self.settings.offset))
        self.selectedPiece = None  # Only one piece may be active at time

        # Promotion
        self.pawnUpgradeBoardBlock = False  # If true only pawnUpgrade options may be pressed
        self.promotionBox = PromotionBox(self.display_surface, settings, self.selectedPiece)

        # Sounds
        self.moveSound = pygame.mixer.Sound('Sounds/piece_move.wav')
        self.checkSound = pygame.mixer.Sound('Sounds/king_check.wav')
        self.castlingSound = pygame.mixer.Sound('Sounds/castling.wav')
        self.pieceTakenSound = pygame.mixer.Sound('Sounds/piece_taken.wav')

        self.game_font = font

        self.board = []
        row = 0
        for col in range(64):
            self.board.append(Block(row, col % 8, BOARD_COLORS[0] if (row + col) % 2 == 0 else BOARD_COLORS[1],
                                    self.settings))
            if col % 8 == 7 and col != 0:
                row += 1

        self.player = Player('white', 0)
        self.player2 = Player('black', 0)

        self.reset()
        self.update()

    def __loadPieceAssets(self):
        for piece in self.player2.pieces + self.player.pieces:
            piece.loadImage(self.settings.block_size)

    def resizeGameSurface(self, surface):
        self.display_surface = surface
        self.gameSurface = pygame.Surface((self.display_surface.get_width() - self.settings.offset,
                                           self.display_surface.get_height() - self.settings.offset))

        # Pieces
        self.__loadPieceAssets()

        for block in self.board:
            block.updateRect()

        self.promotionBox.resizeBox()

        self.draw()

    def reset(self):
        self.player.resetPieces()
        self.player2.resetPieces()

        self.player.fillPieces()
        self.player2.fillPieces()
        self.score_sheet.reset()

        # load assets
        self.__loadPieceAssets()

        # reset connections with pieces
        for block in self.board:
            block.piece = None

        # Connect pieces with blocks
        for piece in self.player.pieces:
            self.board[piece.getSquare()].piece = piece

        for piece in self.player2.pieces:
            self.board[piece.getSquare()].piece = piece

    def changeGameSettings(self, settings):
        self.settings = settings

    def castling(self):
        if self.selectedPiece.color == 'white':
            if self.selectedPiece.col == 6:  # short castling
                self.board[63].piece.move(7, 5, self.board)
                self.score_sheet.addMove(self.selectedPiece, 0, 0, False, "ShortCastling")
            else:  # long castling
                self.board[56].piece.move(7, 3, self.board)
                self.score_sheet.addMove(self.selectedPiece, 0, 0, False, "LongCastling")
        else:  # black king
            if self.selectedPiece.col == 6:  # short castling
                self.board[7].piece.move(0, 5, self.board)
                self.score_sheet.addMove(self.selectedPiece, 0, 0, False, "ShortCastling")
            else:  # long castling
                self.board[0].piece.move(0, 3, self.board)
                self.score_sheet.addMove(self.selectedPiece, 0, 0, False, "LongCastling")

    def draw(self):
        # background
        for block in self.board:
            pygame.draw.rect(self.gameSurface, block.color, block.rect)
        # Text
        # calculated only once
        number_x = self.settings.offset / 2 - self.game_font.size('8')[0] / 2
        text_y = (self.settings.offset - self.game_font.size('H')[1]) / 2 + 3

        for i in range(8):
            self.display_surface.blit(self.game_font.render(f'{8 - i}', True, FONT_COLOR),
                                      (number_x, (i + 0.5) * self.settings.block_size + self.settings.offset -
                                       self.game_font.size('8')[1] / 2))
        for i, text in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']):
            self.display_surface.blit(self.game_font.render(text, True, FONT_COLOR),
                                      ((i + 0.5) * self.settings.block_size + self.settings.offset -
                                       self.game_font.size(text)[0] / 2, text_y))
        # Pieces
        for piece in self.player.pieces:
            self.gameSurface.blit(piece.image, piece.getRealXY(self.settings.block_size))

        for piece in self.player2.pieces:
            self.gameSurface.blit(piece.image, piece.getRealXY(self.settings.block_size))

        self.display_surface.blit(self.gameSurface, (self.settings.offset, self.settings.offset))

        if self.pawnUpgradeBoardBlock:
            self.promotionBox.draw()

    def checkEnPassant(self):

        piece1 = self.board[Block.getBoardIndexRowCol(self.selectedPiece.row,
                                                      self.selectedPiece.col - 1)].piece if self.selectedPiece.col > 0 else None
        piece2 = self.board[Block.getBoardIndexRowCol(self.selectedPiece.row,
                                                      self.selectedPiece.col + 1)].piece if self.selectedPiece.col < 7 else None
        if isinstance(piece1,
                      Pawn) and piece1.color != self.selectedPiece.color and self.score_sheet.turns - piece1.doubleMoveTurn == 1:
            return piece1
        elif isinstance(piece2,
                        Pawn) and piece2.color != self.selectedPiece.color and self.score_sheet.turns - piece2.doubleMoveTurn == 1:
            return piece2
        else:
            return None

    def returnEnPassantMove(self):
        piece = self.checkEnPassant()
        if piece is None:
            return None

        if piece.col == self.selectedPiece.col - 1:  # left move
            if self.selectedPiece.color == 'white':
                additional_move = (self.selectedPiece.row - 1, self.selectedPiece.col - 1)
            else:
                additional_move = (self.selectedPiece.row + 1, self.selectedPiece.col - 1)
        else:  # right move
            if self.selectedPiece.color == 'white':
                additional_move = (self.selectedPiece.row - 1, self.selectedPiece.col + 1)
            else:
                additional_move = (self.selectedPiece.row + 1, self.selectedPiece.col + 1)

        return additional_move

    def checkedPossibleMoves(self, player, enemy):
        for piece in player.pieces:
            piece.moves.clear()

        king = player.pieces[0]
        king.moves = king.getPossibleMoves(self.board, self, enemy)

        for piece in player.pieces:
            if isinstance(piece, King):
                continue

            pos = (piece.row, piece.col)  # old position

            for move in piece.getPossibleMoves(self.board):
                block_piece = self.board[Block.getBoardIndexRowCol(move[0], move[1])].piece
                piece.move(move[0], move[1], self.board)

                if block_piece is not None:
                    enemy.pieces.remove(block_piece)

                enemy.updateMoves(self.board, player, attackingOnly=True)

                if (king.row, king.col) not in enemy.attackingMoves:
                    piece.moves.append(move)

                if block_piece is not None:
                    enemy.pieces.append(block_piece)

                piece.move(pos[0], pos[1], self.board)
                self.board[Block.getBoardIndexRowCol(move[0], move[1])].piece = block_piece

        enemy.updateMoves(self.board, player, attackingOnly=False)

    def isChecked(self):
        if self.score_sheet.turns % 2 == 0:  # White Turn
            if (self.player.pieces[0].row, self.player.pieces[0].col) in self.player2.possibleMoves:
                print("Check White")
                return True

        else:  # Black Turn
            if (self.player2.pieces[0].row, self.player2.pieces[0].col) in self.player.possibleMoves:
                print("Check Black")
                return True

        return False

    def countMoves(self, player):
        x = 0
        for piece in player.pieces:
            x += len(piece.moves)
        return x

    # Checks if there is a draw, or checkmate

    def checkIfEnd(self):
        # White Turn
        if self.countMoves(self.player) == 0:
            if self.isChecked():
                self.score_sheet.checked("Blackwin")
                pygame.event.post(pygame.event.Event(BLACK_WON))
                return "Black Win"
            else:
                self.score_sheet.checked("Draw")
                pygame.event.post(pygame.event.Event(DRAW))
                return "Stalemate"

        # Black Turn
        if self.countMoves(self.player2) == 0:
            if self.isChecked():
                self.score_sheet.checked("Whitewin")
                pygame.event.post(pygame.event.Event(WHITE_WON))
                return "White Win"
            else:
                self.score_sheet.checked("Draw")
                pygame.event.post(pygame.event.Event(DRAW))
                return "Stalemate"

        # If both White and Black have possible moves

        # Checking for Insufficient Material
        if self.checkInsufficientMaterial(self.player, self.player2):
            self.score_sheet.checked("Draw")
            pygame.event.post(pygame.event.Event(DRAW))
            return "Insufficient Material"

        return None

    def checkInsufficientMaterial(self, white, black):
        white_count = len(white.pieces)
        black_count = len(black.pieces)

        # King vs King scenario
        if white_count == 1 and black_count == 1:
            return True

        elif white_count == 1 and black_count == 2:
            if any(isinstance(x, Bishop) for x in black.pieces) or any(isinstance(x, Knight) for x in black.pieces):
                return True

        elif white_count == 2 and black_count == 1:
            if any(isinstance(x, Bishop) for x in white.pieces) or any(isinstance(x, Knight) for x in white.pieces):
                return True

        elif white_count == 2 and black_count == 2:
            white_index = None
            black_index = None
            for index, piece in enumerate(white.pieces):
                if isinstance(piece, Bishop):
                    white_index = index

            for index, piece in enumerate(black.pieces):
                if isinstance(piece, Bishop):
                    black_index = index

            if white_index is not None and black_index is not None:
                x = (white.pieces[white_index].row + white.pieces[white_index].column) % 2
                y = (black.pieces[black_index].row + black.pieces[black_index].column) % 2
                if x == y:
                    return True

            return None

    def checkMouse(self, mouse_pos):
        if self.pawnUpgradeBoardBlock:
            piece = self.promotionBox.checkMouse()
            if piece is not None:
                temp = piece(self.promotionBox.selectedPiece.row, self.promotionBox.selectedPiece.col,
                             self.promotionBox.selectedPiece.color)
                self.score_sheet.addMove(temp, self.promotionBox.selectedPiece.row, self.promotionBox.selectedPiece.col,
                                         False, "Promotion")
                self.board[Block.getBoardIndexRowCol(self.promotionBox.selectedPiece.row,
                                                     self.promotionBox.selectedPiece.col)].piece = temp
                if self.promotionBox.selectedPiece.color == 'white':
                    player = self.player
                else:
                    player = self.player2

                player.pieces.remove(self.promotionBox.selectedPiece)
                temp.loadImage(self.settings.block_size)
                player.pieces.append(temp)
                self.pawnUpgradeBoardBlock = False

                self.update()

                if self.isChecked():
                    pygame.mixer.Sound.play(self.checkSound)
                    self.score_sheet.checked()
        # mouse cursor is in game board
        elif self.settings.offset <= mouse_pos[0] < self.settings.window_width and self.settings.offset <= mouse_pos[
            1] < self.settings.window_height:
            selected_block = self.board[
                Block.getBoardIndexXY(mouse_pos[0], mouse_pos[1], self.settings.offset, self.settings.block_size)]
            if selected_block.piece is not None:
                # Check Turn
                if self.score_sheet.turns % 2 == 0 and selected_block.piece in self.player2.pieces and self.selectedPiece is None:
                    return
                elif self.score_sheet.turns % 2 == 1 and selected_block.piece in self.player.pieces and self.selectedPiece is None:
                    return

            if selected_block.piece is None and self.selectedPiece is None:
                pass
            elif selected_block.piece is not None and self.selectedPiece is None:  # Select
                # Select a piece
                selected_block.glow()
                self.selectedPiece = selected_block.piece
                self.__showPossibleMoves(moves=self.selectedPiece.moves)
            elif selected_block.piece == self.selectedPiece:  # Undo select and reset colors
                selected_block.resetColor()
                self.__showPossibleMoves(moves=self.selectedPiece.moves, reset=True)
                self.selectedPiece = None
            elif self.selectedPiece is not None:  # make a move
                moves = self.selectedPiece.moves

                if isinstance(self.selectedPiece, Pawn):
                    if abs(selected_block.row - self.selectedPiece.row) == 2:
                        self.selectedPiece.doubleMoveTurn = self.score_sheet.turns
                    if self.returnEnPassantMove() is not None:
                        moves.append(self.returnEnPassantMove())

                if (selected_block.row, selected_block.col) in moves:  # make a move
                    # Reset active blocks
                    self.board[Block.getBoardIndexRowCol(self.selectedPiece.row, self.selectedPiece.col)].resetColor()
                    self.__showPossibleMoves(moves=self.selectedPiece.moves, reset=True)

                    # En Passant
                    if (selected_block.row, selected_block.col) == (self.returnEnPassantMove()):
                        pygame.event.post(pygame.event.Event(EN_PASSANT))
                        if self.selectedPiece.color == 'white':
                            self.player2.pieces.remove(self.board[Block.getBoardIndexRowCol(selected_block.row + 1,
                                                                                            selected_block.col)].piece)
                            self.board[
                                Block.getBoardIndexRowCol(selected_block.row + 1, selected_block.col)].piece = None
                            self.score_sheet.addMove(self.selectedPiece, selected_block.row, selected_block.col, True,
                                                     "EnPassant")
                        elif self.selectedPiece.color == 'black':
                            self.player.pieces.remove(self.board[Block.getBoardIndexRowCol(selected_block.row - 1,
                                                                                           selected_block.col)].piece)
                            self.board[
                                Block.getBoardIndexRowCol(selected_block.row - 1, selected_block.col)].piece = None
                            self.score_sheet.addMove(self.selectedPiece, selected_block.row, selected_block.col, True,
                                                     "EnPassant")
                    elif selected_block.piece is not None and selected_block.piece.color != self.selectedPiece.color:  # attack
                        if selected_block.row != 0 and selected_block.row != 7:
                            pygame.event.post(pygame.event.Event(ATTACK))
                        if selected_block.piece.color == 'white':
                            self.player.pieces.remove(selected_block.piece)
                        else:
                            self.player2.pieces.remove(selected_block.piece)

                    # Move
                    self.selectedPiece.move(selected_block.row, selected_block.col, self.board)
                    print(selected_block.row)

                    event = pygame.event.poll()
                    if event.type == pygame.NOEVENT:
                        self.score_sheet.addMove(self.selectedPiece, selected_block.row, selected_block.col)
                    elif event.type == PAWN_UPGRADE:
                        self.pawnUpgradeBoardBlock = True
                        self.promotionBox.updateSelectedPiece(self.selectedPiece)
                    elif event.type == CASTLING:
                        self.castling()
                    elif event.type == ATTACK:
                        self.score_sheet.addMove(self.selectedPiece, selected_block.row, selected_block.col, True)
                    elif event.type == EN_PASSANT:
                        pass

                    self.update()

                    if self.isChecked():
                        pygame.mixer.Sound.play(self.checkSound)
                        self.score_sheet.checked()
                    elif self.score_sheet.sheet[-1] == "O-O" or self.score_sheet.sheet[-1] == "O-O-O":
                        pygame.mixer.Sound.play(self.castlingSound)
                    elif self.score_sheet.sheet[-1][1] == 'x':
                        pygame.mixer.Sound.play(self.pieceTakenSound)
                    else:
                        pygame.mixer.Sound.play(self.moveSound)

                    # Update MovesCount
                    self.selectedPiece.movescount += 1
                    self.selectedPiece = None
                    # print(self.score_sheet.turns)

                    _ = self.checkIfEnd()

                    print(self.score_sheet.displayPGN())

    def __showPossibleMoves(self, moves, reset=False):
        # En Passant
        if isinstance(self.selectedPiece, Pawn):
            piece = self.returnEnPassantMove()
            if piece is not None:
                block = self.board[Block.getBoardIndexRowCol(piece[0], piece[1])]
                if reset:
                    block.resetColor()
                else:
                    block.danger()

        for move in moves:
            block = self.board[Block.getBoardIndexRowCol(move[0], move[1])]
            if reset:
                block.resetColor()
            else:
                if block.piece is not None:
                    if block.piece.color != self.selectedPiece.col:
                        block.danger()
                else:
                    block.glow()

    def update(self):
        self.player2.updateMoves(self.board, self.player)
        self.player.updateMoves(self.board, self.player2)
        if self.score_sheet.turns % 2 == 0:
            self.checkedPossibleMoves(player=self.player, enemy=self.player2)
        else:
            self.checkedPossibleMoves(player=self.player2, enemy=self.player)
