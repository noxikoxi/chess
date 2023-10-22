import pygame.event
from Classes.Piece import Piece, returnValidMoves, checkStackMoves
from Classes.Block import Block
from Classes.Rook import Rook
from settings import CASTLING


class King(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.image_path = 'white_king.png' if color == 'white' else 'black_king.png'

    def getPossibleMoves(self, board, player, enemy):
        moves = []
        if self.movescount == 0:
                moves = moves + self.checkCastling(board, enemy)

        moves = moves + self.getAttackedBlocks(board)

        attackedBlocks = enemy.attackingMoves
        possibleMoves = []

        pos = (self.row, self.col)
        # Check if king will be safe after move
        for move in moves:
            if move not in attackedBlocks:
                block_piece = board[Block.getBoardIndexRowCol(move[0], move[1])].piece
                self.move(move[0], move[1], board)
                enemy.updateMoves(board, player, attackingOnly=True)

                if (self.row, self.col) not in attackedBlocks:
                    possibleMoves.append(move)

                self.move(pos[0], pos[1], board)
                board[Block.getBoardIndexRowCol(move[0], move[1])].piece = block_piece

        enemy.updateMoves(board, player, attackingOnly=True)

        return possibleMoves

    def move(self, row, col, board):
        tmp = (self.row, self.col)
        super().move(row, col, board)

        # Castling Scenario
        if abs(col - tmp[1]) == 2:
            pygame.event.post(pygame.event.Event(CASTLING))

    def getAttackedBlocks(self, board):
        return checkStackMoves(self.color,
                               returnValidMoves([(self.row + 1, self.col - 1), (self.row + 1, self.col),
                                                 (self.row + 1, self.col + 1), (self.row, self.col + 1),
                                                 (self.row - 1, self.col + 1), (self.row - 1, self.col),
                                                 (self.row - 1, self.col - 1), (self.row, self.col - 1)]),
                               board)

    def checkCastling(self, board, enemy):
        moves = []
        if self.color == "white":
            # Check short Castling
            if (board[61].piece is None and board[62].piece is None and isinstance(board[63].piece, Rook) and
                    board[63].piece.movescount == 0 and (7, 5) not in enemy.possibleMoves):
                moves = moves + [(7, 6)]
            # Check long Castling
            if (board[59].piece is None and board[58].piece is None and board[57].piece is None and
                    isinstance(board[56].piece, Rook) and board[56].piece.movescount == 0
                    and (7, 3) not in enemy.possibleMoves):
                moves = moves + [(7, 2)]

            return moves

        else:
            # Check short Castling
            if (board[5].piece is None and board[6].piece is None and isinstance(board[7].piece, Rook) and
                    board[7].piece.movescount == 0 and (0, 5) not in enemy.possibleMoves):
                moves = moves + [(0, 6)]
            # Check long Castling
            if (board[1].piece is None and board[2].piece is None and board[3].piece is None and
                    isinstance(board[0].piece, Rook) and board[0].piece.movescount == 0
                    and (0, 3) not in enemy.possibleMoves):
                moves = moves + [(0, 2)]

            return moves
