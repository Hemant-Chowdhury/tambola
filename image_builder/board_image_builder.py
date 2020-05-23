from PIL import Image, ImageDraw, ImageFont
from process import BoardProcess
import os

BOX = 50
COLOR_BLACK = "#000000"
COLOR_WHITE = "#ffffff"
COLOR_RED = "#ff0066"


FONT_MEDIUM = ImageFont.truetype(os.path.join('tambola', 'image_builder', 'Lemonada', 'static', 'Lemonada-Medium.ttf'), 22)
FONT_SMALL = ImageFont.truetype(os.path.join('tambola', 'image_builder', 'Nunito', 'Nunito-SemiBold.ttf'), 19)


class BoardImageBuilder(object):
    """Board image builder using PIL"""

    def __init__(self, board_process: BoardProcess):
        self.board_process = board_process
        self.board_img = Image.new("RGB", (BOX * 10, BOX * 10), COLOR_WHITE)
        self.draw = ImageDraw.Draw(self.board_img)
        self.fill_grid()
        self.make_grid_lines()
        self.fill_text()

    def make_grid_lines(self):
        for row in range(0, 11):
            self.draw.line([BOX * row, 0, BOX * row, BOX * 9], fill=COLOR_BLACK, width=3)
        for col in range(0, 10):
            self.draw.line([0, BOX * col, self.board_img.size[0], BOX * col], fill=COLOR_BLACK, width=3)

    def fill_grid(self):
        for i in range(0, 10):
            for j in range(0, 9):
                number = j*10 + i + 1
                if number in self.board_process.get_checked_numbers():
                    self.draw.rectangle([BOX * i, BOX * j, BOX * (i+1), BOX * (j+1)], fill=COLOR_RED)
                    self.draw.text(xy=(BOX * i + 15, BOX * j + 12), text=str(number), fill=COLOR_WHITE, font=FONT_SMALL)
                else:
                    self.draw.text(xy=(BOX * i + 15, BOX * j + 12), text=str(number), fill=COLOR_BLACK, font=FONT_SMALL)

    def fill_text(self):
        self.draw.text(xy=(BOX * 4, BOX * 9 + 10), text=f'Total: {self.board_process.board.pointer}', fill=COLOR_BLACK, font=FONT_SMALL)

    def save_image(self, file_path: str):
        self.board_img.save(file_path)
