from typing import List

from PIL import Image, ImageDraw, ImageFont

from process import TicketProcess

BOX = 60
TITLE = 40
COLOR_BLACK = "#000000"
COLOR_WHITE = "#ffffff"

FONT_MEDIUM = ImageFont.truetype('tambola/image_builder/Lemonada/static/Lemonada-Medium.ttf', 22)
FONT_SMALL = ImageFont.truetype('tambola/image_builder/Nunito/Nunito-Bold.ttf', 19)


class TicketImageBuilder(object):
    """Ticket Image Generator using PIL"""

    def __init__(self, ticket_process: TicketProcess):
        self.ticket_process: TicketProcess = ticket_process
        self.ticket_img = Image.new("RGB", (BOX * 9, BOX * 3 + TITLE), COLOR_WHITE)
        self.draw = ImageDraw.Draw(self.ticket_img)
        self.create_header()
        self.fill_header()
        self.create_grid()
        self.fill_grid()

    def create_header(self):
        self.draw.rectangle([0, 0, self.ticket_img.size[0], TITLE], fill="#c7a4db")
        self.draw.line([0, TITLE, 0, 0, self.ticket_img.size[0], 0, self.ticket_img.size[0], TITLE], fill=COLOR_BLACK,
                       width=3)

    def fill_header(self):
        name = self.ticket_process.ticket.participant_name
        if len(name) > 20:
            name = name[:20] + '..'
        self.draw.text(xy=(10, 0), text=name, fill='#000000', font=FONT_MEDIUM)
        self.draw.text(xy=(BOX * 7 - 20, 0), text=f"id- {self.ticket_process.ticket.ticket_id}", fill=COLOR_BLACK,
                       font=FONT_MEDIUM)

    def create_grid(self):
        for col in range(0, 10):
            self.draw.line([BOX * col, TITLE, BOX * col, self.ticket_img.size[1]], fill=COLOR_BLACK, width=3)
        for row in range(0, 4):
            self.draw.line([0, TITLE + BOX * row, self.ticket_img.size[0], TITLE + BOX * row], fill=COLOR_BLACK,
                           width=3)

    def fill_grid(self):
        for row, num_list in enumerate(self.ticket_process.numbers):
            for col, number in enumerate(num_list):
                number_text = " " if number == 0 else str(number)
                self.draw.text(xy=(BOX * col + BOX // 4, TITLE + BOX * row + BOX // 4), text=number_text,
                               font=FONT_SMALL, fill=COLOR_BLACK)

    def get_ticket_image(self):
        return self.ticket_img


class TicketsImageBuilder:

    def __init__(self, ticket_process_list: List[TicketProcess]):
        ticket_images: List[Image] = list()
        for ticket_process in ticket_process_list:
            ticket_images.append(TicketImageBuilder(ticket_process).ticket_img)

        max_width = max([i.size[0] for i in ticket_images])
        total_height = sum([i.size[1] for i in ticket_images])

        self.full_ticket_image = Image.new('RGB', (max_width, total_height))
        y_offset = 0
        for img in ticket_images:
            self.full_ticket_image.paste(img, (0, y_offset))
            y_offset += img.size[1]

    def save(self, file_path):
        self.full_ticket_image.save(f"{file_path}")

