from pygame.image import load
from pygame import transform
from Classes.Piece import Piece, returnValidMoves
from settings import BLOCK_SIZE
from main import Block

class Bishop(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        temp = 'white_bishop.png' if color == 'white' else 'black_bishop.png'
        self.image = transform.scale(load(f'Assets/{temp}').convert_alpha(), (BLOCK_SIZE, BLOCK_SIZE))

    def __checkDiagonal(self, board):
        moves = []
        #NE
        for i in range(1, 8):
            if returnValidMoves([(self.row - i, self.col + i)]):
                block = board[Block.getBoardIndexRowCol(self.row - i, self.col + i)]
                if block.piece is not None:
                    if block.piece.color != self.color:
                        moves = moves + [(self.row - i, self.col + i)]
                    break
                else:
                    moves = moves + [(self.row - i, self.col + i)]

        #ES
        for i in range(1, 8):
            if returnValidMoves([(self.row + i, self.col + i)]):
                block = board[Block.getBoardIndexRowCol(self.row + i, self.col + i)]
                if block.piece is not None:
                    if block.piece.color != self.color:
                        moves = moves + [(self.row + i, self.col + i)]
                    break
                else:
                    moves = moves + [(self.row + i, self.col + i)]

        #SW
        for i in range(1, 8):
            if returnValidMoves([(self.row + i, self.col - i)]):
                block = board[Block.getBoardIndexRowCol(self.row + i, self.col - i)]
                if block.piece is not None:
                    if block.piece.color != self.color:
                        moves = moves + [(self.row + i, self.col - i)]
                    break
                else:
                    moves = moves + [(self.row + i, self.col - i)]

        #WN
        for i in range(1, 8):
            if returnValidMoves([(self.row - i, self.col - i)]):
                block = board[Block.getBoardIndexRowCol(self.row - i, self.col - i)]
                if block.piece is not None:
                    if block.piece.color != self.color:
                        moves = moves + [(self.row - i, self.col - i)]
                    break
                else:
                    moves = moves + [(self.row - i, self.col - i)]

        return moves


    def getPossibleMoves(self, board):
       return self.__checkDiagonal(board)