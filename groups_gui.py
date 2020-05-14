from tkinter import *
from tkinter import messagebox
import database
ROW = 500
COL = 500
ROWSPAN = 10
COLSPAN = 10

global main_view


class groups_view(object):
    """docstring for groups"""

    def __init__(self, master):
        super(groups_view, self).__init__()
        self.master = master
        self.main_label = Label(master, text="GROUPS", font="Helvetica 16 bold").pack()
        self.groups_frame = groups_frame(master, ROW * 0.9)
        self.add_groups_frame = add_group_frame(master, ROW * 0.1)
        self.groups_frame.pack(fill="both")
        self.add_groups_frame.pack(fill="both")

    def add_in_groups_frame(self, group_name):
        self.groups_frame.add_group_in_frame(group(self.groups_frame, group_name))

    def delete_from_groups_frame(self, group_obj):
        self.groups_frame.delete_group_from_frame(group_obj)


class add_group_frame(Frame):
    """docstring for add_group_frame"""

    def __init__(self, master, height):
        super(add_group_frame, self).__init__(master, height=height)
        self.group_label = Label(self, text="Enter the group name: ")
        self.group_name = Entry(self)
        self.add_group_button = Button(self, text="Add", padx=40, command=self.add_group_method)
        self.group_label.pack(side=LEFT)
        self.group_name.pack(side=LEFT)
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

    def __init__(self, master, height):
        super(groups_frame, self).__init__(master, relief=SUNKEN, height=height, borderwidth=4, bg='#ccff99')
        self.pack_propagate(False)
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
        self.group_name_label.pack(side=LEFT)
        self.delete_button.pack(side=RIGHT)
        self.view_button.pack(side=RIGHT)

    def delete(self):
        try:
            database.groups_table.delete(self.group_name)
            main_view.delete_from_groups_frame(self)
        except database.DatabaseOperationError:
            messagebox.showerror("Error", "Failed to delete " + self.group_name)

    def view(self):
        pass


master = Tk()
master.geometry(f'{ROW}x{COL}')
for r in range(ROW):
    master.rowconfigure(r, weight=1)
for c in range(COL):
    master.columnconfigure(c, weight=1)
main_view = groups_view(master)
master.mainloop()
