from pygame import USEREVENT
import os


class Settings:
    def __init__(self):
        self.file_name = "settings.txt"
        self.resizing_options = [[600, 600, 50, 55], [800, 800, 60, 70], [1000, 1000, 60, 70]]
        self.large_buttons_size = [200, 100]  # [width, height]
        self.square_buttons_size = [50, 50]  # [width, height]
        self.picked_options = 1
        current_directory = os.getcwd()
        if not os.path.exists(f"{current_directory}/{self.file_name}"):
            print("hmmm")
            with open(self.file_name, "w") as file:
                file.write("1")
        else:
            with open(self.file_name, "r") as file:
                self.picked_options = int(file.read())
        self.updateSettings()

    def updateSettings(self):
        self.window_height, self.window_width, self.offset, self.font_size = self.resizing_options[self.picked_options]
        self.block_size = (self.window_width - self.offset) / 8

    def changeSettings(self, choice):
        self.picked_options = choice
        with open(self.file_name, "w") as file:
            file.write(f"{choice}")
        self.updateSettings()


BOARD_COLORS = ('gray', (150, 120, 160))
FONT_COLOR = (255, 255, 255)

PAWN_UPGRADE = USEREVENT + 0
CASTLING = USEREVENT + 1
ATTACK = USEREVENT + 2
EN_PASSANT = USEREVENT + 3
WHITE_WON = USEREVENT + 4
BLACK_WON = USEREVENT + 5
DRAW = USEREVENT + 6

