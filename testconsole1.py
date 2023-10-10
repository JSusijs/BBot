from tkinter import *
from tkinter import ttk

root = Tk()
root.title("BBot")
root.geometry("400x400")
frm = ttk.Frame(root, padding=100)
frm.grid()
ttk.Label(frm, text="text").grid(column=0, row=0)

ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=1)

root.mainloop()
