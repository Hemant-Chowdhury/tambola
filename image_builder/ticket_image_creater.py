from PIL import Image, ImageDraw, ImageFont

from process import TicketProcess

BOX = 60
TITLE = 40
COLOR_BLACK = "#000000"
COLOR_WHITE = "#ffffff"

FONT_MEDIUM = ImageFont.truetype('image_builder/Lemonada/static/Lemonada-Medium.ttf', 22)
FONT_SMALL = ImageFont.truetype('image_builder/Nunito/Nunito-Bold.ttf', 19)


class TicketImageGenerator(object):
    """Ticket Image Generator using PIL"""

    def __init__(self, ticket_process: TicketProcess):
        self.ticket_process: TicketProcess = ticket_process
        self.ticket_img = Image.new("RGB", (BOX * 9, BOX * 3 + TITLE), COLOR_WHITE)
        self.draw = ImageDraw.Draw(self.ticket_img)
        self.create_header()
        self.fill_header()
        self.create_grid()
        self.fill_grid()
        self.ticket_img.show()
    
    def create_header(self):
        self.draw.rectangle([0, 0, self.ticket_img.size[0], TITLE], fill="#c7a4db")
        self.draw.line([0, TITLE, 0, 0, self.ticket_img.size[0], 0, self.ticket_img.size[0], TITLE], fill=COLOR_BLACK, width=3)
        
    def fill_header(self):
        name = self.ticket_process.ticket.participant_name
        if len(name) > 20:
            name = name[:20] + '..'
        self.draw.text(xy=(10, 0), text=name, fill='#000000', font=FONT_MEDIUM)
        self.draw.text(xy=(BOX * 7 - 20, 0), text=f"id- {self.ticket_process.ticket.ticket_id}", fill=COLOR_BLACK, font=FONT_MEDIUM)
    
    def create_grid(self):
        for col in range(0, 10):
            self.draw.line([BOX * col, TITLE, BOX * col, self.ticket_img.size[1]], fill=COLOR_BLACK, width=3)
        for row in range(0, 4):
            self.draw.line([0, TITLE + BOX * row, self.ticket_img.size[0], TITLE + BOX * row], fill=COLOR_BLACK, width=3)

    def fill_grid(self):
        for row, num_list in enumerate(self.ticket_process.numbers):
            for col, number in enumerate(num_list):
                self.draw.text(xy=(BOX*col + BOX//4, TITLE+BOX*row + BOX//4), text=str(number), font=FONT_SMALL, fill=COLOR_BLACK)
