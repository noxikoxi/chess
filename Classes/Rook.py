from pygame.image import load
from pygame import transform
from Classes.Piece import Piece
from settings import BLOCK_SIZE
from main import Block


class Rook(Piece):

    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        temp = 'white_rook.png' if color == 'white' else 'black_rook.png'
        self.image = transform.scale(load(f'Assets/{temp}').convert_alpha(), (BLOCK_SIZE, BLOCK_SIZE))

    def __checkOrthogonal(self, board):
        moves = []
        # N
        for i in range(1, 8):
            if 0 <= self.row - i <= 7 and 0 <= self.col <= 7:
                block = board[Block.getBoardIndexRowCol(self.row - i, self.col)]
                if block.piece is not None:
                    if block.piece.color != self.color:
                        moves = moves + [(self.row - i, self.col)]
                    elif block.piece.color == self.color:
                        break
                else:
                    moves = moves + [(self.row - i, self.col)]

        # E
        for i in range(1, 8):
            if 0 <= self.row <= 7 and 0 <= self.col + i <= 7:
                block = board[Block.getBoardIndexRowCol(self.row, self.col + i)]
                if block.piece is not None:
                    if block.piece.color != self.color:
                        moves = moves + [(self.row, self.col + i)]
                    elif block.piece.color == self.color:
                        break
                else:
                    moves = moves + [(self.row, self.col + i)]

        # S
        for i in range(1, 8):
            if 0 <= self.row + i <= 7 and 0 <= self.col <= 7:
                block = board[Block.getBoardIndexRowCol(self.row + i, self.col)]
                if block.piece is not None:
                    if block.piece.color != self.color:
                        moves = moves + [(self.row + i, self.col)]
                    elif block.piece.color == self.color:
                        break
                else:
                    moves = moves + [(self.row + i, self.col)]

        # W
        for i in range(1, 8):
            if 0 <= self.row <= 7 and 0 <= self.col - i <= 7:
                block = board[Block.getBoardIndexRowCol(self.row, self.col - i)]
                if block.piece is not None:
                    if block.piece.color != self.color:
                        moves = moves + [(self.row, self.col - i)]
                    elif block.piece.color == self.color:
                        break
                else:
                    moves = moves + [(self.row, self.col - i)]

        return moves

    def getPossibleMoves(self, board):
        return self.__checkOrthogonal(board)

