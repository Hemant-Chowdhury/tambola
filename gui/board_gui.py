from tkinter import *
from tkinter import messagebox
import database
import operations


HEIGHT = 700
PARTICIPANTS_FRAME_WIDTH = 300
TICKETS_FRAME_WIDTH = 300
BOARDS_FRAME_WIDTH = 650

green_background = '#ccff99'
blue_background = '#b3e6ff'

group_name = None
main_view_object = None
participants_frame_object = None
tickets_frame_object = None
boards_frame_object = None


class game_view(Toplevel):
    """docstring for game_view"""

    def __init__(self, master, group):
        super(game_view, self).__init__(master)
        global group_name
        group_name = group
        global main_view_object
        main_view_object = self
        self.main_label = Label(self, text=group, font="Helvetica 16 bold").pack()
        self.participants_frame = self.create_a_scrollable_frame(frame_type=participants_frame, width=PARTICIPANTS_FRAME_WIDTH, height=HEIGHT)
        global participants_frame_object
        participants_frame_object = self.participants_frame
        self.tickets_frame = self.create_a_scrollable_frame(frame_type=tickets_frame, width=TICKETS_FRAME_WIDTH, height=HEIGHT)
        global tickets_frame_object
        tickets_frame_object = self.tickets_frame
        self.boards_frame = self.create_a_scrollable_frame(frame_type=boards_frame, width=BOARDS_FRAME_WIDTH, height=HEIGHT)
        global boards_frame_object
        boards_frame_object = self.boards_frame

    def create_a_scrollable_frame(self, frame_type, height, width):
        scrollable_frame = Frame(self, relief=SUNKEN, bd=4, height=height, width=width)
        scrollable_frame.pack_propagate(False)
        scrollable_frame.pack(fill='y', side='left')
        canvas = Canvas(scrollable_frame, bg=green_background, height=height, width=width)
        custom_frame = frame_type(canvas)

        scrollbar = Scrollbar(scrollable_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        canvas.pack(fill='both')

        canvas.create_window((0, 0), window=custom_frame, anchor='nw', width=width - 20)
        custom_frame.bind("<Configure>", lambda _: canvas.configure(scrollregion=canvas.bbox("all")))
        return custom_frame


class participants_frame(Frame):
    """docstring for participants_frame"""

    def __init__(self, master):
        super(participants_frame, self).__init__(master, bg=green_background)
        Label(self, text='Participants', bg=blue_background).pack(fill='x')
        add_participant_labelframe = LabelFrame(self, text='Add participant', bg=green_background)
        self.add_participant_entry = Entry(add_participant_labelframe)
        self.add_participant_button = Button(add_participant_labelframe, text='Add', bg='green', command=self.add_participant_method)
        self.add_participant_entry.pack(side='left')
        self.add_participant_button.pack(side='right')
        add_participant_labelframe.pack(pady='5', padx='10')
        Label(self, text='', bg=blue_background).pack(fill='x')
        self.participants = list()
        self.init_participants()

    def init_participants(self):
        participants_list = database.participants_table.fetch_participants_in_a_group(group_name=group_name)
        for participant_name in participants_list:
            self.add_participant_in_frame(participant_name)

    def add_participant_method(self):
        participant_name = self.add_participant_entry.get()
        if participant_name == '':
            messagebox.showerror('Error', 'Please enter a participant name')
            return
        try:
            database.participants_table.insert(group_name=group_name, participant_name=participant_name)
            self.add_participant_in_frame(participant_name)
        except database.DatabaseOperationError:
            messagebox.showerror('Error', f'Unable to add {participant_name} in {group_name}')

    def add_participant_in_frame(self, participant_name):
        new_participant_view = participant_view(self, participant_name=participant_name)
        new_participant_view.pack(fill='x')
        self.participants.append(new_participant_view)

    def remove_participant_from_frame(self, participant_view_object):
        participant_view_object.pack_forget()
        participant_view_object.destroy()
        self.participants.remove(participant_view_object)


class participant_view(LabelFrame):
    """docstring for add_participant_view"""

    def __init__(self, master, participant_name):
        super().__init__(master)
        self.participant_name = participant_name
        self.participant_button = Button(
            self,
            text=participant_name,
            width=15,
            justify='left',
            command=lambda: tickets_frame_object.refresh_tickets(participant_name))
        self.participant_button.pack(side='left')
        self.remove_button = Button(self, text='Remove', command=self.remove)
        self.remove_button.pack(side='right')
        self.add_ticket_button = Button(self, text='+', command=self.add_ticket)
        self.add_ticket_button.pack(side='right')

    def remove(self):
        try:
            response = messagebox.askquestion('Remove participant', f'Are you sure you want to remove {self.participant_name} from {group_name}')
            if response == 'yes':
                database.participants_table.delete(group_name=group_name, participant_name=self.participant_name)
                participants_frame_object.remove_participant_from_frame(self)
        except database.DatabaseOperationError:
            messagebox.showerror('Error', 'Unable to remove participant, please try again')

    def add_ticket(self):
        new_ticket = operations.generator.get_new_ticket(group_name=group_name, participant_name=self.participant_name)
        if tickets_frame_object.participant_name == self.participant_name:
            tickets_frame_object.create_and_include_ticket_view_in_list(new_ticket)


class tickets_frame(Frame):
    """docstring for tickets_frame"""

    def __init__(self, master):
        super(tickets_frame, self).__init__(master, bg=green_background)
        Label(self, text='Tickets', bg=blue_background).pack(fill='x')
        self.participant_name = ''
        self.participant_label = Label(self, text=self.participant_name, bg=green_background)
        self.tickets_view_objects = list()

    def refresh_tickets(self, participant_name):
        self.participant_label.pack_forget()
        for view_obj in self.tickets_view_objects:
            view_obj.pack_forget()
            view_obj.destroy()
        self.tickets_view_objects.clear()

        self.participant_name = participant_name
        if participant_name == '':
            return

        self.participant_label.configure(text=self.participant_name)
        self.participant_label.pack(fill='x')

        tickets = database.tickets_table.fetch_tickets_of_a_participant_in_a_group(
            participant_name=participant_name,
            group_name=group_name)
        for ticket in tickets:
            self.create_and_include_ticket_view_in_list(ticket)

    def create_and_include_ticket_view_in_list(self, ticket_object):
        ticket_view_object = ticket_view(self, ticket_object)
        ticket_view_object.pack(fill='x')
        self.tickets_view_objects.append(ticket_view_object)


class ticket_view(LabelFrame):
    """docstring for ticket_view"""

    def __init__(self, master, ticket_object):
        super(ticket_view, self).__init__(master, bd=2, relief='groove', padx=3)
        self.ticket_object = ticket_object
        Label(self, text=ticket_object.participant_name, width=32).grid(sticky='n', columnspan=9)
        Label(self, text=f'Ticket number: {ticket_object.id}').grid(sticky='n', columnspan=9)
        self.numbers = list()
        self.init_numbers()
        self.pack_numbers()

    def init_numbers(self):
        for row in self.ticket_object.numbers:
            row_of_lables = list()
            for number in row:
                text = ' ' if number == 0 else str(number)
                row_of_lables.append(Label(self, text=text, borderwidth=2, relief="groove", font='Helvetica 16 bold'))
            self.numbers.append(row_of_lables)

    def pack_numbers(self):
        for row, row_list in enumerate(self.numbers):
            for col, label in enumerate(row_list):
                label.grid(row=row + 2, column=col, sticky='news')


class boards_frame(Frame):
    """docstring for boards_frame"""

    def __init__(self, master):
        super(boards_frame, self).__init__(master, bg=green_background)
        self.grid_rowconfigure(0, weight=1)
        Label(self, text='Board', bg=blue_background, width=77).grid(sticky='we', columnspan=10)
        self.numbers = list()
        self.init_numbers()
        self.pack_numbers()
        Label(self, text='', bg=blue_background).grid(sticky='we', columnspan=10)
        self.next_number_button = Button(self, text='Next Number')
        self.start_pause_button = Button(self, text='New Game', command=self.new_game_method)
        self.next_number_label = Label(self, text='89', borderwidth=2, relief="groove", font='Helvetica 16 bold')
        self.start_pause_button.grid(row=12, column=0, columnspan=5, sticky='nws')
        self.next_number_button.grid(row=12, column=5, columnspan=3, sticky='nes')
        self.next_number_label.grid(row=12, column=8, sticky='news', columnspan=2)
        self.next_number_label.config(bg='red', fg='white')
        self.board = None
        self.init_board()
        # self.init_board_state()

    def init_numbers(self):
        for row in range(1, 10):
            row_list = list()
            for col in range(1, 11):
                row_list.append(Label(self, text=str((row - 1) * 10 + col), borderwidth=2, relief="groove", font='Helvetica 16 bold', height=3, width=3))
            self.numbers.append(row_list)

    def pack_numbers(self):
        for row, row_list in enumerate(self.numbers):
            for col, number_label in enumerate(row_list):
                # print(row + 20, col)
                number_label.grid(row=row + 1, column=col, sticky='news')

    def init_board(self):
        self.board = database.boards_table.fetch_board(group_name)

    def init_board_state(self):
        pass

    def get_next_number(self):
        pass

    def new_game_method(self):
        if self.board is not None:
            response = messagebox.askquestion('New Game', 'Are you sure you want to start a new game? All the tickets will be deleted and board will be cleaned.')
            if response != 'yes':
                return
            operations.clear.group_data(group_name)
            self.board = None
        try:
            self.board = operations.generator.get_new_board(group_name)
        except Exception as e:
            raise e
            messagebox.showerror('Error', 'Unable to start new game, try again')
