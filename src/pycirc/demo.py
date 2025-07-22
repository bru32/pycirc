""" 
pycirc demo.
The circuit calculation returns lists of tube id's. 
These can be used to draw on any canvas.  The example 
below demonstrates the use of a tkinter canvas.
"""

__author__ = "Bruce Wernick"
__date__ = "22 July 2025"

import tkinter as tk
from pycirc import *


root = tk.Tk()
root.title("pycirc demo")

canvas = tk.Canvas(root)
canvas.pack(expand=True, fill="both")

tubeshigh = 14
rowsdeep = 6
nc = 4

circs = calc_circs(tubeshigh, rowsdeep, nc)

XY = create_xymap(tubeshigh, rowsdeep)
draw_circuits(canvas, XY, circs)
draw_tube_bank(canvas, XY)

root.mainloop()
