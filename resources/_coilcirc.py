# Coil circuit application
# Bruce Wernick
# 20 July 2025

import tkinter as tk
from tkinter import ttk
from tkmonkey import *
from pycirc import *


class EntryFrame(ttk.Frame):
  def __init__(self, parent, label_text, entry_var, *args, **kwargs):
    super().__init__(parent, *args, **kwargs)

    self.columnconfigure(0, weight=1, uniform="a")
    self.columnconfigure(1, weight=1, uniform="a")

    label = ttk.Label(self, text=label_text)
    label.grid(row=0, column=0, sticky="news")

    edit = ttk.Entry(self, width=12, text="Enter value", textvariable=entry_var)
    edit.grid(row=0, column=1, sticky="news")


class TubePlate(tk.Canvas):
  x0, y0 = 18, 18
  sx, sy = 16, 18
  def __init__(self, parent, *args, **kwargs):
    super().__init__(parent, *args, **kwargs)

  def XY(self, c, r):
    """ translate from (col,row) coords to
        screen (x,y) values.
    """
    x0, y0 = 18, 18
    sx, sy = 16, 18
    x = c * sx
    y = r * sy
    if c % 2 != 0:
      y += 0.5*sy
    return x0 + x, y0 + y

  def draw_circuit(self, arr):
    """ draw circuit from array of grid pos
    """
    coords = [self.XY(item[1],item[0]//2) for item in arr]
    for i in range(len(coords)-1):
      c1, r1 = coords[i]
      c2, r2 = coords[i+1]
      if i % 2 == 0:
        self.canvas.create_line(c1, r1, c2, r2, width=1, fill="tomato")
      else:
        self.canvas.create_line(c1, r1, c2, r2, width=1.5, fill="#069")

  def paint(self, nth, rows, nc, paths):
    x0, y0 = TubePlate.x0, TubePlate.y0
    sx, sy = TubePlate.sx, TubePlate.sy
    self.delete("all")

    # draw circuits
    circs = []
    for path in paths:
      if not path:
        continue
      circ = []
      for item in path:
        circ.append(Map.k2rc(item))
      circs.append(circ)


    # draw tube-bank
    for c in range(rows):
      x = x0 + c*sx
      dr = 0 if c % 2 == 0 else 0.5
      for r in range(nth):
        y = y0 + (r + dr)*sy
        self.create_tube(x, y)


class MainForm(tk.Tk):
  def __init__(self):
    super().__init__()
    self.geometry("600x400")
    self.title("Coil Circuit")

    # Create some styles so we can see the effects
    self.style = ttk.Style()
    self.style.theme_use("clam")

    # container frame for input
    frame0 = ttk.Frame(self, width=150)
    frame0.pack(side="left", expand=False, fill="both")

    # define input variables
    self.var1 = tk.IntVar(self, value=14)
    self.var2 = tk.IntVar(self, value=6)
    self.var3 = tk.IntVar(self, value=4)

    entry1 = EntryFrame(frame0, "Tubes high", self.var1)
    entry1.pack(pady=10)
    entry2 = EntryFrame(frame0, "Rows deep", self.var2)
    entry2.pack(pady=5)
    entry3 = EntryFrame(frame0, "N Circuits", self.var3)
    entry3.pack(pady=5)

    button1 = ttk.Button(frame0, text="Solve", command=self.do_circ)
    button1.pack(pady=10)

    self.canvas = TubePlate(self, background="white",
      border=1, highlightthickness=1,
      highlightcolor="red", highlightbackground="grey",
      relief="ridge")
    self.canvas.pack(side="left", expand=True, fill="both")
    self.canvas.update()

  def do_circ(self):
    nth = self.var1.get()
    rows = self.var2.get()
    nc = self.var3.get()
    #print(f"{nth=}, {rows=}, {nc=}")
    circs = calc(nth, rows, nc)
    self.canvas.paint(nth, rows, nc, circs)


if __name__ == "__main__":
  app = MainForm()
  app.mainloop()
