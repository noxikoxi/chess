from Classes.Pawn import Pawn
from Classes.Queen import Queen, Rook, Bishop
from Classes.King import King
from Classes.Knight import Knight

ROW = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]


class Player:
    def __init__(self, color, time):
        self.pieces = []
        self.color = color
        self.points = 0
        self.time = time
        self.pieces = []
        self.possibleMoves = []
        self.attackingMoves = []

    def updateMoves(self, board, enemy, attackingOnly=False):
        if not attackingOnly:
            self.possibleMoves.clear()
        self.attackingMoves.clear()

        for piece in self.pieces:
            if isinstance(piece, Pawn):
                if not attackingOnly:
                    temp = piece.getPossibleMoves(board)
                self.attackingMoves += piece.getAttackedBlocks()
            elif isinstance(piece, King):
                if not attackingOnly:
                    temp = piece.getPossibleMoves(board, self, enemy)
                self.attackingMoves += piece.getAttackedBlocks(board)
            else:
                temp = piece.getPossibleMoves(board)
                self.attackingMoves += temp
            if not attackingOnly:
                piece.moves = temp
                self.possibleMoves += temp

    def resetPieces(self):
        self.pieces.clear()

    def fillPieces(self):
        if self.color == 'white':
            for i, piece in enumerate(ROW):
                self.pieces.append(piece(7, i, self.color))

            # King is on index 0
            self.pieces[0], self.pieces[4] = self.pieces[4], self.pieces[0]

            for i in range(8):
                self.pieces.append(Pawn(6, i, self.color))
        else:
            for i, piece in enumerate(ROW):
                self.pieces.append(piece(0, i, self.color))

            self.pieces[0], self.pieces[4] = self.pieces[4], self.pieces[0]

            for i in range(8):
                self.pieces.append(Pawn(1, i, self.color))
