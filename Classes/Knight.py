from Classes.Piece import Piece, returnValidMoves, checkStackMoves


class Knight(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.image_path = 'white_knight.png' if color == 'white' else 'black_knight.png'

    def getPossibleMoves(self, board):
        return checkStackMoves(self.color, returnValidMoves([(self.row + 2, self.col + 1), (self.row + 2, self.col - 1), (self.row - 2, self.col + 1),
                                 (self.row - 2, self.col - 1), (self.row + 1, self.col + 2), (self.row + 1, self.col - 2),
                                 (self.row - 1, self.col + 2), (self.row - 1, self.col - 2)]), board)
