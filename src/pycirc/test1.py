import tkinter as tk
from random import randint, randbytes
from tkmonkey import *
from urand import randpoint

root = tk.Tk()
canvas = tk.Canvas(root, width=256, height=256)
canvas.pack(expand=True, fill="both", padx=5, pady=5)
arr = [randpoint(0, 256) for _ in range(200)]
#canvas.create_line(arr, width=2, fill="black", joinstyle="round", capstyle="round")
canvas.create_alt_line(arr, "tomato", "cadet blue", width=2)
root.mainloop()
