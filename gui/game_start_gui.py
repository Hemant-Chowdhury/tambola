from tkinter import Tk, messagebox, Label, Canvas, Scrollbar, Frame, LabelFrame, Button, Entry
from typing import List

from process import game_process, GroupProcess, ProcessError
from gui.group_gui import GroupWindow

import os

ROW = 500
COL = 500


class GroupsView(object):
    """docstring for groups"""

    def __init__(self, master):
        super(GroupsView, self).__init__()
        self.master = master
        self.main_label = Label(master, text="GROUPS", font="Helvetica 16 bold").pack()
        self.groups_frame = self.create_a_scrollable_groups_frame(height=ROW * 0.85)
        self.add_groups_frame = AddGroupsFrame(master, ROW * 0.1)
        self.add_groups_frame.pack(fill="both")

    def create_a_scrollable_groups_frame(self, height):
        scrollable_frame = Frame(self.master,
                                 relief='sunken',
                                 bd=4)
        scrollable_frame.pack(fill="both")
        canvas = Canvas(scrollable_frame,
                        bg='#ccff99',
                        height=height)
        custom_frame = AllGroupsFrame(canvas)

        scrollbar = Scrollbar(scrollable_frame,
                              orient="vertical",
                              command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        canvas.pack(fill='both')

        self.master.update()
        canvas.create_window((0, 0),
                             window=custom_frame,
                             anchor='nw',
                             width=canvas.winfo_width() - 2)
        custom_frame.bind("<Configure>", lambda _: canvas.configure(scrollregion=canvas.bbox("all")))
        return custom_frame

    def add_in_groups_frame(self, group_process: GroupProcess):
        self.groups_frame.add_group_in_frame(GroupLabelFrame(self.groups_frame, group_process))

    def open_group(self, group_process):
        GroupWindow(self.master, group_process)


class AddGroupsFrame(Frame):
    """docstring for add_groups_frame"""

    def __init__(self, master, height):
        super(AddGroupsFrame, self).__init__(master, height=height)
        self.group_label = Label(self, text="Enter the new group name: ")
        self.group_name = Entry(self)
        self.add_group_button = Button(self, text="Add", padx=40, command=self.add_group_method)
        self.group_label.pack(side='left')
        self.group_name.pack(side='left')
        self.add_group_button.pack(side='right')

    def add_group_method(self):
        group_name = self.group_name.get()
        self.group_name.select_clear()
        try:
            new_game_process = game_process.create_new_group(group_name)
            main_view.add_in_groups_frame(new_game_process)
        except ProcessError as e:
            messagebox.showerror('Error', e)


class GroupLabelFrame(LabelFrame):
    """docstring for GroupLabelFrame"""

    def __init__(self, master, group_process: GroupProcess):
        super(GroupLabelFrame, self).__init__(master)
        self.group_process = group_process
        self.master = master
        self.group_name_label = Label(self, text=self.group_process.group.group_name)
        self.view_button = Button(self, text=" Open ", command=self.view)
        self.delete_button = Button(self, text="Delete", command=self.delete_group)
        self.group_name_label.pack(side='left')
        self.delete_button.pack(side='right')
        self.view_button.pack(side='right')

    def delete_group(self):
        response = messagebox.askquestion("Delete group",
                                          f'Are you sure you want to delete {self.group_process.group.group_name}',
                                          default='no')
        if response == 'no':
            return
        game_process.delete_group(self.group_process)
        self.master.delete_group_from_frame(self)

    def view(self):
        main_view.open_group(self.group_process)


class AllGroupsFrame(Frame):
    """docstring for all_groups_frame"""

    def __init__(self, master):
        super(AllGroupsFrame, self).__init__(master, borderwidth=2, bg='#ccff99')
        # self.pack_propagate(False)
        self.groups: List[GroupLabelFrame] = list()
        self._init_group_view()

    def _init_group_view(self):
        list_group_process = game_process.group_process_list
        for group_process in list_group_process:
            self.groups.append(GroupLabelFrame(self, group_process))

        for group_obj in self.groups:
            group_obj.pack(fill='x')

    def delete_group_from_frame(self, group_label_frame_obj: GroupLabelFrame):
        self.groups.remove(group_label_frame_obj)
        group_label_frame_obj.pack_forget()
        group_label_frame_obj.destroy()

    def add_group_in_frame(self, group_label_frame_obj: GroupLabelFrame):
        self.groups.append(group_label_frame_obj)
        group_label_frame_obj.pack(fill='x')


ROOT = Tk()
ROOT.title("Tambola")
ROOT.iconbitmap(os.path.abspath(os.path.join('tambola', 'resources', 'icon.ico')))

ROOT.geometry(f'{ROW}x{COL}')
main_view = GroupsView(ROOT)
ROOT.mainloop()

# TODO Add logger throughout the code
