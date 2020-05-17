from tkinter import *
from tkinter import messagebox
from board_gui import game_view
import database
ROW = 500
COL = 500

global main_view


class groups_view(object):
    """docstring for groups"""

    def __init__(self, master):
        super(groups_view, self).__init__()
        self.master = master
        self.main_label = Label(master, text="GROUPS", font="Helvetica 16 bold").pack()
        self.groups_frame = self.create_a_scrollable_groups_frame(height=ROW * 0.85)
        self.add_groups_frame = add_groups_frame(master, ROW * 0.1)
        self.add_groups_frame.pack(fill="both")

    def create_a_scrollable_groups_frame(self, height):
        scrollable_frame = Frame(self.master, relief=SUNKEN, bd=4)
        scrollable_frame.pack(fill="both")
        canvas = Canvas(scrollable_frame, bg='#ccff99', height=height)
        custom_frame = groups_frame(canvas)

        scrollbar = Scrollbar(scrollable_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        canvas.pack(fill='both')

        self.master.update()
        canvas.create_window((0, 0), window=custom_frame, anchor='nw', width=canvas.winfo_width() - 2)
        custom_frame.bind("<Configure>", lambda _: canvas.configure(scrollregion=canvas.bbox("all")))
        return custom_frame

    def add_in_groups_frame(self, group_name):
        self.groups_frame.add_group_in_frame(group(self.groups_frame, group_name))

    def delete_from_groups_frame(self, group_obj):
        self.groups_frame.delete_group_from_frame(group_obj)

    def open_board(self, group_name):
        game_view(self.master, group_name)


class add_groups_frame(Frame):
    """docstring for add_groups_frame"""

    def __init__(self, master, height):
        super(add_groups_frame, self).__init__(master, height=height)
        self.group_label = Label(self, text="Enter the new group name: ")
        self.group_name = Entry(self)
        self.add_group_button = Button(self, text="Add", padx=40, command=self.add_group_method)
        self.group_label.pack(side='left')
        self.group_name.pack(side='left')
        self.add_group_button.pack(side=RIGHT)

    def add_group_method(self):
        group_name = self.group_name.get()
        self.group_name.select_clear()
        if group_name == '':
            messagebox.showerror('Error', 'Please enter a group name')
            return
        try:
            database.groups_table.insert(group_name)
            main_view.add_in_groups_frame(group_name)
        except database.DatabaseOperationError:
            messagebox.showerror('Error', 'Unable to add ' + group_name)


class groups_frame(Frame):
    """docstring for groups_frame"""

    def __init__(self, master):
        super(groups_frame, self).__init__(master, borderwidth=2, bg='#ccff99')
        # self.pack_propagate(False)
        self.groups = set()
        self._init_group_view()

    def _init_group_view(self):
        list_group_names = database.groups_table.fetch_all()
        for name in list_group_names:
            self.groups.add(group(self, name))
        for group_obj in self.groups:
            group_obj.pack(fill=X)

    def delete_group_from_frame(self, group_obj):
        self.groups.remove(group_obj)
        group_obj.pack_forget()
        group_obj.destroy()

    def add_group_in_frame(self, group_obj):
        self.groups.add(group_obj)
        group_obj.pack(fill=X)


class group(LabelFrame):
    """docstring for group"""

    def __init__(self, master, group_name):
        super(group, self).__init__(master)
        self.group_name = group_name
        self.master = master
        self.group_name_label = Label(self, text=self.group_name)
        self.view_button = Button(self, text="View", command=self.view)
        self.delete_button = Button(self, text="Delete", command=self.delete)
        self.group_name_label.pack(side='left')
        self.delete_button.pack(side='right')
        self.view_button.pack(side='right')

    def delete(self):
        try:
            database.groups_table.delete(self.group_name)
            main_view.delete_from_groups_frame(self)
        except database.DatabaseOperationError:
            messagebox.showerror("Error", "Failed to delete " + self.group_name)

    def view(self):
        main_view.open_board(self.group_name)


master = Tk()
master.geometry(f'{ROW}x{COL}')
# master.resizable(False, False)
main_view = groups_view(master)
master.mainloop()
