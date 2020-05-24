import tempfile
import os
from tkinter import *
from tkinter import messagebox, filedialog
from typing import List, Optional
from image_builder import ticket_image_builder, board_image_builder

from process import GroupProcess, ParticipantProcess, TicketProcess, ParticipantProcessError, BoardProcess, \
    BoardProcessError, GroupProcessError

PARTICIPANTS_FRAME_WIDTH = 300
TICKETS_FRAME_WIDTH = 350
BOARDS_FRAME_WIDTH = 650

COLOR_GREEN = '#ccff99'
COLOR_BLUE = '#b3e6ff'

start_window_height = 800
active_group_process: Optional[GroupProcess] = None
main_group_window = None


class GroupWindow(Toplevel):
    """docstring for GroupWindow"""

    def __init__(self, master, group_process_obj: GroupProcess):
        super(GroupWindow, self).__init__(master)
        self.title(group_process_obj.group.group_name)
        self.iconbitmap(os.path.abspath(os.path.join('tambola', 'resources', 'icon.ico')))
        global start_window_height
        start_window_height = min(start_window_height, self.winfo_screenheight() - 200)
        global active_group_process
        active_group_process = group_process_obj
        global main_group_window
        main_group_window = self
        self.main_label = Label(self, text=group_process_obj.group.group_name, font="Helvetica 16 bold").pack()
        self.participants_frame = self.create_a_scrollable_frame(
            frame_type=AllParticipantsFrame,
            width=PARTICIPANTS_FRAME_WIDTH,
            height=start_window_height)
        self.tickets_frame = self.create_a_scrollable_frame(
            frame_type=TicketsFrame,
            width=TICKETS_FRAME_WIDTH,
            height=start_window_height)
        self.boards_frame = self.create_a_scrollable_frame(
            frame_type=BoardFrame,
            width=BOARDS_FRAME_WIDTH,
            height=start_window_height)

    def create_a_scrollable_frame(self, frame_type, height, width):
        scrollable_frame = Frame(self,
                                 relief=SUNKEN,
                                 bd=4,
                                 height=height,
                                 width=width)
        scrollable_frame.pack_propagate(False)
        scrollable_frame.pack(fill='y', side='left')
        canvas = Canvas(scrollable_frame,
                        bg=COLOR_GREEN,
                        height=height,
                        width=width)
        custom_frame = frame_type(canvas)

        scrollbar = Scrollbar(scrollable_frame,
                              orient="vertical",
                              command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        canvas.pack(fill='both')

        canvas.create_window((0, 0),
                             window=custom_frame,
                             anchor='nw',
                             width=width - 20)
        custom_frame.bind("<Configure>", lambda _: canvas.configure(scrollregion=canvas.bbox("all")))
        return custom_frame


class InterFrameCalls:

    def __init__(self):
        pass

    @staticmethod
    def refresh_ticket_frame(participant_process: Optional[ParticipantProcess] = None):
        main_group_window.tickets_frame.refresh_tickets(participant_process)

    @staticmethod
    def refresh_ticket_frame_if_participant_in_focus(participant_process: ParticipantProcess):
        main_group_window.tickets_frame.refresh_ticket_frame_if_participant_in_focus(participant_process)

    @staticmethod
    def add_ticket_in_ticket_frame_if_participant_in_focus(new_ticket_process):
        main_group_window.tickets_frame.update_ticket_view_if_participant_in_focus(new_ticket_process)

    @staticmethod
    def check_new_number_present_in_tickets(number):
        main_group_window.tickets_frame.mark_number_in_tickets_if_present(number)

    @staticmethod
    def get_checked_board_numbers() -> List[int]:
        return main_group_window.boards_frame.board_process.get_checked_numbers()


class ParticipantLabelFrame(LabelFrame):
    """docstring for ParticipantLabelFrame"""

    def __init__(self, master, participant_process: ParticipantProcess):
        super().__init__(master)
        self.master = master
        self.participant_process: ParticipantProcess = participant_process
        self.participant_label = Button(
            self,
            width=18,
            text=participant_process.participant.participant_name,
            justify='left',
            command=lambda: InterFrameCalls.refresh_ticket_frame(self.participant_process))
        self.participant_label.grid(row=0, column=0, columnspan=5)
        self.remove_button = Button(self, text='Remove', command=self.remove)
        self.remove_button.grid(row=0, column=5, sticky='e', columnspan=3)
        self.number_of_tickets_label = Label(self,
                                             text=f'Tickets: {len(self.participant_process.ticket_process_list)}')
        self.number_of_tickets_label.grid(row=1, column=0, columnspan=3, sticky='w')
        self.add_ticket_button = Button(self, text='+', command=self.add_ticket)
        self.add_ticket_button.grid(row=1, column=3, columnspan=1, sticky='w')
        self.share_tickets_button = Button(self, text='Share tickets', command=self.share_ticket)
        self.share_tickets_button.grid(row=1, column=4, columnspan=4, sticky='news')

    def remove(self):
        try:
            response = messagebox.askquestion(
                'Remove participant',
                f'Are you sure you want to remove '
                f'{self.participant_process.participant.participant_name} '
                f'from {active_group_process.group.group_name}')
            if response == 'yes':
                active_group_process.remove_participant(self.participant_process)
                InterFrameCalls.refresh_ticket_frame_if_participant_in_focus(self.participant_process)
                self.master.remove_participant_from_frame(self)
        except GroupProcessError as e:
            messagebox.showerror('Error', e)

    def add_ticket(self):
        new_ticket_process = self.participant_process.add_ticket()
        self.number_of_tickets_label.config(text=f'Tickets: {len(self.participant_process.ticket_process_list)}')
        InterFrameCalls.add_ticket_in_ticket_frame_if_participant_in_focus(new_ticket_process)

    def share_ticket(self):
        if len(self.participant_process.ticket_process_list) == 0:
            messagebox.showinfo("Share Ticket", "Please add at least one ticket to share!")
            return
        name = self.participant_process.participant.participant_name + "_tickets"
        file = filedialog.asksaveasfile(
            initialfile=name,
            title='Save Ticket',
            defaultextension='.png',
            filetypes=[('PNG file', '*.png')]
            )
        ticket_image_builder.TicketsImageBuilder(self.participant_process.ticket_process_list).save(file.name)


class AllParticipantsFrame(Frame):
    """docstring for AllParticipantsFrame"""

    def __init__(self, master):
        super(AllParticipantsFrame, self).__init__(master, bg=COLOR_GREEN)
        Label(self, text='Participants', bg=COLOR_BLUE).pack(fill='x')
        add_participant_labelframe = LabelFrame(self,
                                                text='Add participant',
                                                bg=COLOR_GREEN)
        self.add_participant_entry = Entry(add_participant_labelframe)
        self.add_participant_button = Button(add_participant_labelframe,
                                             text='Add',
                                             command=self.add_participant_method)
        self.add_participant_entry.pack(side='left')
        self.add_participant_button.pack(side='right')
        add_participant_labelframe.pack(pady='5', padx='10')
        Label(self, text='', bg=COLOR_BLUE).pack(fill='x')
        self.participant_view_objects: List[ParticipantLabelFrame] = list()
        self.init_participants()

    def init_participants(self):
        for participant_process in active_group_process.participant_process_list:
            self.add_participant_in_frame(participant_process)

    def add_participant_method(self):
        participant_name = self.add_participant_entry.get()
        if participant_name == '':
            messagebox.showerror('Error', 'Please enter a participant name')
            return
        try:
            new_participant_process = active_group_process.add_participant(participant_name)
            self.add_participant_in_frame(new_participant_process)
        except ParticipantProcessError as e:
            messagebox.showerror('Error', e)

    def add_participant_in_frame(self, participant_process: ParticipantProcess):
        new_participant_view = ParticipantLabelFrame(self, participant_process=participant_process)
        new_participant_view.bind("<Button-1>", lambda _: InterFrameCalls.refresh_ticket_frame(participant_process))
        self.participant_view_objects.append(new_participant_view)
        new_participant_view.pack(fill='x', padx=2)

    def remove_participant_from_frame(self, participant_view_object):
        participant_view_object.pack_forget()
        participant_view_object.destroy()
        self.participant_view_objects.remove(participant_view_object)


class TicketsFrame(Frame):
    """docstring for TicketsFrame"""

    def __init__(self, master):
        super(TicketsFrame, self).__init__(master, bg=COLOR_GREEN)
        Label(self, text='Tickets', bg=COLOR_BLUE).pack(fill='x')
        self.participant_process: Optional[ParticipantProcess] = None
        self.participant_label = Label(self, text='', bg=COLOR_GREEN)
        self.tickets_view_objects: List[TicketLabelFrame] = list()

    def refresh_tickets(self, participant_process: Optional[ParticipantProcess] = None):
        self.participant_label.pack_forget()
        for view_obj in self.tickets_view_objects:
            view_obj.pack_forget()
            view_obj.destroy()
        self.tickets_view_objects.clear()

        self.participant_process = participant_process
        if self.participant_process is None:
            self.participant_label.configure(text='')
            return

        self.participant_label.configure(text=self.participant_process.participant.participant_name)
        self.participant_label.pack(fill='x')

        for ticket_process_obj in self.participant_process.ticket_process_list:
            self.create_and_include_ticket_view_in_list(ticket_process_obj)

    def create_and_include_ticket_view_in_list(self, ticket_process_obj: TicketProcess):
        ticket_view_object = TicketLabelFrame(self, ticket_process_obj)
        self.tickets_view_objects.append(ticket_view_object)
        ticket_view_object.pack(fill='x', padx=3)

    def update_ticket_view_if_participant_in_focus(self, new_ticket_process: TicketProcess):
        if self.participant_process is None:
            return
        if new_ticket_process.get_participant() != self.participant_process.participant:
            return
        self.create_and_include_ticket_view_in_list(new_ticket_process)

    def mark_number_in_tickets_if_present(self, number):
        for ticket_view_obj in self.tickets_view_objects:
            try:
                row, col = ticket_view_obj.ticket_process.locate_number(number)
                ticket_view_obj.mark_number(row=row, col=col)
            except TypeError:
                pass

    def refresh_ticket_frame_if_participant_in_focus(self, participant_process: ParticipantProcess):
        if participant_process.participant == self.participant_process.participant:
            self.refresh_tickets()


class TicketLabelFrame(LabelFrame):
    """docstring for TicketLabelFrame"""

    def __init__(self, master, ticket_process: TicketProcess):
        super(TicketLabelFrame, self).__init__(master, bg=COLOR_BLUE)
        self.ticket_process: TicketProcess = ticket_process
        Label(self,
              text=self.ticket_process.ticket.participant_name,
              bg=COLOR_BLUE,
              width=39
              ).grid(sticky='new', columnspan=9)
        Label(self,
              text=f'Ticket number: {self.ticket_process.ticket.ticket_id}',
              bg=COLOR_BLUE,
              ).grid(sticky='new', columnspan=9)
        self.number_labels: List[List[Label]] = list()
        self._init_numbers()
        self._pack_numbers()
        self._mark_already_checked_numbers()

    def _init_numbers(self):
        for row in self.ticket_process.numbers:
            row_of_labels: List[Label] = list()
            for number in row:
                text = ' ' if number == 0 else str(number)
                number_label = Label(self, text=text, borderwidth=2, relief="groove", font='Helvetica 17 bold', padx=1)
                row_of_labels.append(number_label)
            self.number_labels.append(row_of_labels)

    def _pack_numbers(self):
        for row, row_list in enumerate(self.number_labels):
            for col, label in enumerate(row_list):
                label.grid(row=row + 2, column=col, sticky='news')

    def _mark_already_checked_numbers(self):
        checked_numbers = InterFrameCalls.get_checked_board_numbers()
        for row, row_list in enumerate(self.ticket_process.numbers):
            for col, number in enumerate(row_list):
                if number in checked_numbers:
                    self.mark_number(row, col)

    def mark_number(self, row, col):
        self.number_labels[row][col].config(bg='red', fg='white')


class BoardFrame(Frame):
    """docstring for BoardFrame"""

    def __init__(self, master):
        super(BoardFrame, self).__init__(master, bg=COLOR_GREEN)
        self.board_process: BoardProcess = active_group_process.board_process
        self.grid_rowconfigure(0, weight=1)
        Label(self, text='Board', bg=COLOR_BLUE, width=77).grid(sticky='we', columnspan=10)
        self.numbers_label: List[List[Label]] = list()
        self._init_board_numbers()

        Label(self, text='', bg=COLOR_BLUE).grid(sticky='we', columnspan=10)
        self.next_number_button = Button(self,
                                         text='Next Number',
                                         command=self.get_next_number)
        self.start_new_game_button = Button(self,
                                            text='Start New Game',
                                            command=self.new_game_method)
        self.share_board_button = Button(self,
                                         text='Share board',
                                         command=self.share_board)
        self.next_number_label = Label(self,
                                       text='',
                                       borderwidth=2,
                                       relief="groove",
                                       font='Helvetica 24 bold',
                                       bg='red', fg='white')
        self.start_new_game_button.grid(row=12, column=0, columnspan=3, sticky='nws')
        self.share_board_button.grid(row=12, column=2, columnspan=2)
        self.next_number_button.grid(row=12, column=6, columnspan=2, sticky='nes')
        self.next_number_label.grid(row=12, column=8, sticky='news', columnspan=2)

        self._init_board_state()
        self.sequence_label_manager = self.BoardDataViewer(self, row=13)

    def _init_board_numbers(self):
        for row in range(1, 10):
            row_list = list()
            for col in range(1, 11):
                row_list.append(Label(self,
                                      text=str((row - 1) * 10 + col),
                                      borderwidth=2, relief="groove",
                                      font='Helvetica 24 bold',
                                      width=3))
            self.numbers_label.append(row_list)
        for row, row_list in enumerate(self.numbers_label):
            for col, number_label in enumerate(row_list):
                number_label.grid(row=row + 1, column=col, sticky='news')

    def _init_board_state(self):
        for number in self.board_process.get_checked_numbers():
            self.mark_number_in_board(number)
        if self.board_process.board.pointer == 0:
            self.start_new_game_button.config(state=DISABLED)

    def _init_sequence_numbers(self):
        self.sequence_labels = [Label(self, text='', fg='white', font='Helvetica 16 bold') for _ in range(6)]

    def mark_number_in_board(self, number: int):
        number -= 1
        row = number // 10
        col = number % 10
        self.numbers_label[row][col].config(bg='blue', fg='white')

    def get_next_number(self):
        try:
            number = self.board_process.get_next_number()
        except BoardProcessError as e:
            messagebox.showerror("No next number", e)
            return
        self.next_number_label.config(text=str(number))
        self.mark_number_in_board(number)
        if self.board_process.board.pointer == 1:
            self.enable_start_new_game_button()
        InterFrameCalls.check_new_number_present_in_tickets(number)
        self.sequence_label_manager.insert_new_number_in_sequence()

    def new_game_method(self):
        response = messagebox.askquestion('New Game', 'Are you sure you want to start a new game? '
                                                      'All the tickets will be deleted and board will be cleaned.')
        if response != 'yes':
            return
        try:
            active_group_process.refresh_group_variables()
            self.remove_all_marked_numbers()
            InterFrameCalls.refresh_ticket_frame()
            self.start_new_game_button.config(state=DISABLED)
            self.sequence_label_manager.refresh_sequence()
        except GroupProcessError as e:
            messagebox.showerror('Error', e)

    def remove_all_marked_numbers(self):
        for row, row_list in enumerate(self.numbers_label):
            for col, number_label in enumerate(row_list):
                number_label.config(bg='white', fg='black')

    def enable_start_new_game_button(self):
        self.start_new_game_button.config(state=NORMAL)

    def share_board(self):
        name = "board"
        file = filedialog.asksaveasfile(
            initialfile=f'{name}_snapshot_till_{self.board_process.board.pointer}_numbers_called',
            title='Share Board',
            defaultextension='.png',
            filetypes=[('PNG files', '*.png')])
        board_image_builder.BoardImageBuilder(self.board_process).save_image(file.name)

    class BoardDataViewer:
        """docstring for Board data viewer"""

        def __init__(self, master, row):
            self.master: BoardFrame = master
            self.window = 6
            self.starting_pointer = max(0, self.master.board_process.board.pointer - self.window)
            self.sequence_labels: List[Label] = [Label(master, text='', bg=COLOR_GREEN) for _ in range(6)]
            for column, label in enumerate(self.sequence_labels, 1):
                label.grid(row=row, column=column)
            self.prev_label_button = Button(master, text='<<', command=self.prev_button)
            self.next_label_button = Button(master, text='>>', command=self.next_button)
            self.prev_label_button.grid(row=row, column=0, sticky='news')
            self.next_label_button.grid(row=row, column=7, sticky='news')
            self.number_of_numbers_called_label = Label(master,
                                                        text=f'',
                                                        bg=COLOR_GREEN)
            self.number_of_numbers_called_label.grid(row=row, column=8, columnspan=2)
            self.show_total_numbers_called()
            self.set_new_view()

        def set_new_view(self):
            checked_numbers = self.master.board_process.get_checked_numbers()
            for index, label in enumerate(self.sequence_labels, self.starting_pointer):
                if index < self.master.board_process.board.pointer - 1:
                    label.config(fg=f"#{99-index:02d}00{index:02d}")
                    label.config(text=f'{checked_numbers[index]}->', bd=2, relief='flat')
                elif index == self.master.board_process.board.pointer - 1:
                    label.config(fg=f'#{99-index:02d}00{index:02d}')
                    label.config(text=f'{checked_numbers[index]}->', bd=2, relief='solid')
                else:
                    label.config(bg=COLOR_GREEN, text='', bd=0)
            if self.starting_pointer == 0:
                self.prev_label_button.config(state=DISABLED)
            else:
                self.prev_label_button.config(state=NORMAL)
            if self.starting_pointer + self.window < self.master.board_process.board.pointer:
                self.next_label_button.config(state=NORMAL)
            else:
                self.next_label_button.config(state=DISABLED)

        def prev_button(self):
            self.starting_pointer = max(0, self.starting_pointer-1)
            self.set_new_view()

        def next_button(self):
            self.starting_pointer = min(max(0, self.master.board_process.board.pointer - self.window),
                                        self.starting_pointer + 1)
            self.set_new_view()

        def insert_new_number_in_sequence(self):
            self.starting_pointer = max(0, self.master.board_process.board.pointer - self.window)
            self.set_new_view()
            self.show_total_numbers_called()

        def refresh_sequence(self):
            self.starting_pointer = 0
            self.set_new_view()
            self.show_total_numbers_called()

        def show_total_numbers_called(self):
            if self.master.board_process.board.pointer != 0:
                self.number_of_numbers_called_label.config(text=f'Total: {self.master.board_process.board.pointer}')
            else:
                self.number_of_numbers_called_label.config(text=f'Lets Play!')
