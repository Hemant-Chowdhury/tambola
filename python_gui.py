from tkinter import *

window = Tk()
window.title("Tumbola")


def myFunction():
    pass


label1 = Label(window, text="Text 1")
label2 = Label(window, text="Text 2")

btn = Button(window, text="Click me", command=myFunction)
btn.pack()

window.mainloop()
