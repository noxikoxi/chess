from pygame.image import load
from pygame import transform
from Classes.Piece import Piece, returnValidMoves
from Classes.Block import Block
from settings import BLOCK_SIZE



class Rook(Piece):

    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        temp = 'white_rook.png' if color == 'white' else 'black_rook.png'
        self.image = transform.scale(load(f'Assets/{temp}').convert_alpha(), (BLOCK_SIZE, BLOCK_SIZE))

    def __checkOrthogonal(self, board):
        moves = []
        # N
        for i in range(1, 8):
            if returnValidMoves([(self.row - i, self.col)]):
                block = board[Block.getBoardIndexRowCol(self.row - i, self.col)]
                if block.piece is not None:
                    if block.piece.color != self.color:
                        moves = moves + [(self.row - i, self.col)]
                    break
                else:
                    moves = moves + [(self.row - i, self.col)]

        # E
        for i in range(1, 8):
            if returnValidMoves([(self.row, self.col + i)]):
                block = board[Block.getBoardIndexRowCol(self.row, self.col + i)]
                if block.piece is not None:
                    if block.piece.color != self.color:
                        moves = moves + [(self.row, self.col + i)]
                    break
                else:
                    moves = moves + [(self.row, self.col + i)]

        # S
        for i in range(1, 8):
            if returnValidMoves([(self.row + i, self.col)]):
                block = board[Block.getBoardIndexRowCol(self.row + i, self.col)]
                if block.piece is not None:
                    if block.piece.color != self.color:
                        moves = moves + [(self.row + i, self.col)]
                    break
                else:
                    moves = moves + [(self.row + i, self.col)]

        # W
        for i in range(1, 8):
            if returnValidMoves([(self.row, self.col - i)]):
                block = board[Block.getBoardIndexRowCol(self.row, self.col - i)]
                if block.piece is not None:
                    if block.piece.color != self.color:
                        moves = moves + [(self.row, self.col - i)]
                    break
                else:
                    moves = moves + [(self.row, self.col - i)]

        return moves

    def getPossibleMoves(self, board):
        return self.__checkOrthogonal(board)

