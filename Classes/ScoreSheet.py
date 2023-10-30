import datetime
import os

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
        "Checkmate": "#"
    }

    def __init__(self):
        self.sheet = []
        self.turns = 0

    def reset(self):
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
        self.turns = self.turns + 1

    def checked(self, option = "Checked"):
        if option == "Checked":
            tmp = self.sheet[-1]
            tmp += "+"
            self.sheet[- 1] = tmp

        else:
            self.sheet.append(self.special.get(str(option)))

    def displayPGN(self):
        pgn = ""
        count_moves = 1
        count_lines = 1
        for move in self.sheet:

            if count_moves % 2 == 1:
                pgn += f"{count_lines}. "
            pgn += move + " "

            if count_moves % 2 == 0:
                pgn += "\n"
                count_lines += 1

            count_moves += 1

        return pgn + '\n'

    def saveSheet(self):
        current_directory = os.getcwd()
        os.makedirs(f"{current_directory}/Saved Games", exist_ok=True)
        time = datetime.datetime.now()
        file_name = time.strftime("chess_game_%d%m%Y_%H%M%S.pgn")
        file_path = f'{current_directory}/Saved Games/{file_name}'
        with open(file_path, "w") as file:
            file.write(self.displayPGN())
        print(f"Game score sheet has been saved in a file named {file_name}")
