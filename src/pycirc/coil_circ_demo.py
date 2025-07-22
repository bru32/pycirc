""" pycirc demo
"""

__author__ = "Bruce Wernick"
__date__ = "22 July 2025"

import tkinter as tk
from pycirc import *


root = tk.Tk()
root.geometry("400x600+500+10")

frame = tk.Frame(root)
frame.pack(expand=True, fill="both")

canvas = tk.Canvas(frame)
canvas.pack(expand=True, fill="both")

tubeshigh = 14
rowsdeep = 6
nc = 4
circs = calc_circs(tubeshigh, rowsdeep, nc)
XY = create_xymap(tubeshigh, rowsdeep)
draw_circuits(canvas, XY, circs)
draw_tube_bank(canvas, XY)

root.mainloop()
