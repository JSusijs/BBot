import tkinter as tk

root = tk.Tk()
root.title("BBot")
root.geometry("400x300")

label = tk.Label(root, text="___", font=("Helvetica", 16))
label.pack(pady=50)


def on_button_click():
    label.config(text="button 2")


button = tk.Button(root, text="button", command=on_button_click, font=("Helvetica", 14))
button.pack()

btn = tk.Button(root, text="quit", command=root.destroy)
btn.pack()

root.mainloop()
