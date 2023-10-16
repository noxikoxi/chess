from Classes.Piece import Piece
from Classes.Rook import Rook
from Classes.Bishop import Bishop


class Queen(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.image_path  = 'white_queen.png' if color == 'white' else 'black_queen.png'

    def getPossibleMoves(self, board):
        a1 = Rook(self.row, self.col, self.color)
        a2 = Bishop(self.row, self.col, self.color)
        moves = Rook.getPossibleMoves(a1, board)
        moves = moves + Bishop.getPossibleMoves(a2, board)
        return moves
