# from tkinter import *

# root = Tk()
# root.geometry('500x500')

# for r in range(10):
#     root.rowconfigure(r, weight=1)
# for c in range(5):
#     root.columnconfigure(c, weight=1)

# frame_left = Frame(root, bg="red")
# frame_right = Frame(root, bg="blue")
# frame_left.grid(row=0, column=0, columnspan=2, rowspan=10, sticky=N + W + E + S)
# frame_right.grid(row=0, column=2, columnspan=3, rowspan=10, sticky=N + W + E + S)
# left_frame_scrollbar = Scrollbar(frame_left, orient=VERTICAL)

# listbox = Listbox(frame_left, yscrollcommand=left_frame_scrollbar)
# listbox.insert("end", "group1")

# # Configure scrollbar
# left_frame_scrollbar.config(command=listbox.yview)
# left_frame_scrollbar.pack(side=RIGHT, fill=Y)
# listbox.pack(fill=X)


# def add_group():
#     listbox.insert("end", "bhjb")


# def delete_group():
#     listbox.delete("anchor")


# b = Button(frame_right, text='New group', command=add_group)
# b.pack()
# d = Button(frame_right, text='Delete', command=delete_group)
# d.pack()
# root.mainloop()


# Creating a new window -> Toplevel()
# Open file -> filedialog.askopenfilename(initialdir='', title='', filetypes=(("png files", "*.png"),("all files", "*.*")))


# from PIL import ImageTk, Image

# my_image = ImageTk.PhotoImage(Image.open('Image_file_name'))
# my_image_label = Label(image=my_image).pack()


# options = list()
# clicked = StringVar()
# clicked.set(options[0])
# drop = OptionMenu(root, clicked, *options)
# drop.pack()

# to get the selection = clicked.get()


# from tkinter import ttk, Tk, Frame

# root = Tk()

# my_notebook = ttk.Notebook(root)
# my_notebook.pack()


# my_frame1 = Frame(my_notebook, width=500, height=500, bg='blue')
# my_frame2 = Frame(my_notebook, width=500, height=500, bg='red')

# my_frame1.pack(fill="both")
# my_frame2.pack(fill="both")

# my_notebook.add(my_frame1, text="blue")
# my_notebook.add(my_frame2, text="red")


# root.mainloop()


# bttn_image = PhotoImage("image_src")
