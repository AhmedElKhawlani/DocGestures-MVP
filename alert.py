#!/usr/bin/python3

from tkinter import *


def alert(title, message):
    warning = Tk()
    warning.title(title)
    warning.resizable(width=False, height=False)

    label_warning = Label(warning, text=message)
    label_warning.grid(column=1, row=2)

    label_adjust1 = Label(warning, text=" " * 20)
    label_adjust1.grid(column=0, row=2)
    label_adjust2 = Label(warning, text=" " * 20)
    label_adjust2.grid(column=2, row=2)
    label_adjust3 = Label(warning, text=" " * 20)
    label_adjust3.grid(column=0, row=3)
    label_adjust4 = Label(warning, text=" " * 20)
    label_adjust4.grid(column=0, row=0)

    warning.mainloop()
