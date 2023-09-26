class ScoreSheet:
    pieces = {
        "Pawn": "",
        "Bishop": "B",
        "Queen": "Q",
        "Rook": "R",
        "Knight": "N",
        "King": "K",
        "True": "x",
        "False": ""
    }

    columns = {
        "0": "a",
        "1": "b",
        "2": "c",
        "3": "d",
        "4": "e",
        "5": "f",
        "6": "g",
        "7": "h",
    }

    rows = {
        "0": "8",
        "1": "7",
        "2": "6",
        "3": "5",
        "4": "4",
        "5": "3",
        "6": "2",
        "7": "1",
    }

    special = {
        "False" : "",
        "LongCastling": "O-O-O",
        "ShortCastling": "O-O",
        "Whitewin": "1-0",
        "Blackwin": "0-1",
        "Draw": "1/2-1/2",
        "Check": "+",
        "Checkmate": "#"
    }

    def __init__(self):
        self.sheet = []
        self.turns = 0

    def addMove(self, piece, row, column, attacked = False, special = False):
        if special is False or special == "Check":
            if attacked == True and piece.__class__.__name__ == "Pawn":
                notation = self.columns.get(str(piece.col)) + self.pieces.get(str(attacked)) + self.columns.get(str(column)) + self.rows.get(str(row))
            else:
                notation = self.pieces.get(piece.__class__.__name__) + self.pieces.get(str(attacked)) + self.columns.get(str(column)) + self.rows.get(str(row)) + self.special.get(str(special))
        elif special == "Promotion":
            notation = self.columns.get(str(column)) + self.rows.get(str(row)) + self.pieces.get(piece.__class__.__name__)
        elif special == "EnPassant":
            notation = self.columns.get(str(piece.col)) + self.pieces.get(str(attacked)) + self.columns.get(str(column)) + self.rows.get(str(row)) + " e.p."
        else:
            notation = self.special.get(str(special))
        self.sheet.append(notation)
        print(self.sheet)
        self.turns = self.turns + 1
