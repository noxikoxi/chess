from pygame.image import load
from pygame import transform
from Classes.Piece import Piece, returnValidMoves, checkStackMoves
from settings import BLOCK_SIZE


class King(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        temp = 'white_king.png' if color == 'white' else 'black_king.png'
        self.image = transform.scale(load(f'Assets/{temp}').convert_alpha(), (BLOCK_SIZE, BLOCK_SIZE))

    def getPossibleMoves(self, board):
        moves = []
        if self.movescount == 0:
            moves = moves + self.checkCastling(board)

        moves = moves + checkStackMoves(self.color, returnValidMoves([(self.row + 1, self.col - 1), (self.row + 1, self.col),
                                                             (self.row + 1, self.col + 1), (self.row, self.col + 1),
                                                             (self.row - 1, self.col + 1), (self.row - 1, self.col),
                                                             (self.row - 1, self.col - 1), (self.row, self.col - 1)]),
                                                             board)

        return moves

    def move(self, row, col, board):
        tmp = (self.row, self.col)
        super().move(row, col)

        # Castling Scenario
        if abs((row + col) - (tmp[0] + tmp[1])) == 2:
            if row == 7 and col == 6:
                board[63].piece.move(7, 5)
            if row == 7 and col == 2:
                board[56].piece.move(7, 3)
            if row == 0 and col == 2:
                board[0].piece.move(0, 3)
            if row == 0 and col == 6:
                board[7].piece.move(0, 5)

    def checkCastling(self, board):
        moves = []
        if self.color == "white":
            # Check short Castling
            if board[61].piece is None and board[62].piece is None and board[63].piece.movescount == 0:
                moves = moves + [(7, 6)]
            # Check long Castling
            if board[59].piece is None and board[58].piece is None and board[57].piece is None and board[56].piece.movescount == 0:
                moves = moves + [(7, 2)]
            return moves

        else:
            # Check short Castling
            if board[5].piece is None and board[6].piece is None and board[7].piece.movescount == 0:
                moves = moves + [(0, 6)]
            # Check long Castling
            if board[1].piece is None and board[2].piece is None and board[3].piece is None and board[0].piece.movescount == 0:
                moves = moves + [(0, 2)]
            return moves
