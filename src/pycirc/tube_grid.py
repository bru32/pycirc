""" 
Module for plotting coil tube bank.
It includes methods to:
  - Generate a tube layout
  - Draw the tubes to a canvas
  - Draw the circuits
"""

__date__ = "16 July 2025"
__author__ = "Bruce Wernick"

from collections import defaultdict
from enum import StrEnum
import tkinter as tk
from tkinter import ttk
from tkmonkey import *
from pycirc import *

colors = {
  "canvas": "#f1eacd",
  "tube": "#ffffee",
  "endplate": "seashell2",
  "circ1": "cadet blue",
  "circ2": "tomato"}

class Pattern(StrEnum):
  STAGGERED = "staggered"
  INLINE = "inline"

def write_note(canvas, xy, text):
  x = xy["x"]
  y = xy["y"]
  xy["y"] += 30
  canvas.create_text(x, y, text=text, fill="black", 
    font=("Consolas", 14), justify="left", anchor="nw")

class TubeBank(tk.Tk):

  x0, y0 = 60, 40  # left and top margin for tube bank

  # sy = tube high 1½" = 3*25.4/2 = 38.1mm
  # sx = rows deep √(sy² - ½sy²) = sy*√(3/4) = 0.866*sy = 32.9946mm
  # sx, sy = 32.9946, 38.1  # typical 1/2" coil
  sy = 19  # more suitable for a neater plot
  sx = 33  # keep same proportion (0.866*30=25.98)

  def __init__(self, title="App", 
    size=(600, 600), xypos=(600, 10), icon=None,
    tubeshigh=14, rowsdeep=6, pattern="staggered"):
    super().__init__()

    self.width, self.height = size
    xpos, ypos = xypos
    self.geometry(f"{self.width}x{self.height}+{xpos}+{ypos}")

    # Container frame
    frame = ttk.Frame(self)
    frame.pack(expand=True, 
      fill="both", side="top", 
      padx=0, pady=0)

    # Drawing canvas for tube bank
    self.canvas = tk.Canvas(frame, 
      background=colors["canvas"],
      borderwidth=0, highlightthickness=0, 
      relief="flat")
    self.canvas.pack(expand=True, 
      fill="both", side="top",
      padx=0, pady=0)
    self.canvas.update()

    self.reset()

  def reset(self, 
    tubeshigh=14, rowsdeep=6, pattern="staggered"):

    if pattern.casefold() == "staggered":
      self.staggered = True
    else:
      self.staggered = False

    # Assign tube bank parameters
    self.tubeshigh = tubeshigh
    self.rowsdeep = rowsdeep

    self.title(f"Coil tube bank: {rowsdeep} row {tubeshigh} tubes high ({pattern})")

    self.canvas.delete("all")

    self.to_coord = defaultdict(lambda: (-1,-1))
    self.to_index = defaultdict(lambda: None)
    
    self.generate_index()

    self.draw_end_plate()

    # Notes
    xy = {"x": 280, "y": 20}
    for note in [
      "6 rows deep", 
      "14 tubes high", 
      "4 circuits", 
      "21 tubes/circ"]:
      write_note(self.canvas, xy, note)


  def generate_index(self):
    """ Generate tube index dictionary.
        tube_pos[k] = (x,y)
    """
    x0 = TubeBank.x0
    y0 = TubeBank.y0
    sx = TubeBank.sx
    sy = TubeBank.sy
    tubeshigh = self.tubeshigh
    rowsdeep = self.rowsdeep
    staggered = self.staggered
    
    self.to_coord.clear()
    self.to_index.clear()

    cols, rows = rowsdeep, 2*tubeshigh
    k = 0
    for r in range(rows):
      y = y0 + r * sy
      col0 = r % 2
      for c in range(col0, cols, 2):
        x = x0 + c * sx
        coord = (x,y)
        self.to_coord[k] = coord
        self.to_index[coord] = k
        k += 1

  def draw_end_plate(self):
    """ draw end-plate
    """    
    x0 = TubeBank.x0
    y0 = TubeBank.y0
    sx = TubeBank.sx
    sy = TubeBank.sy
    dt = 0.5 if self.staggered else 0
    x1 = x0 + sx*(self.rowsdeep - 1)
    y1 = y0 + 2*sy*(self.tubeshigh - 1 + dt)
    g = sx/2
    coords = x0-g, y0-g, x1+g, y1+g
    self.canvas.create_rectangle(coords,
      fill=colors["endplate"])

  def draw_tubes(self):
    """ draw all tubes in bank
    """
    r = 5  # sized for looks, not proportional.
    for k, (x, y) in self.to_coord.items():
      self.canvas.create_circle(x, y, r,
        width=1, outline="#555555",
        fill=colors["tube"])

      # Add tube label
      self.canvas.create_text(x+6, y-11, 
        text=f"{k}", font=("tahoma", 8),
        justify="center", anchor="center")

  def draw_circs(self, circs=[]):
    """ draw all circuits
    """
    for i, circ in enumerate(circs):
      points = []
      for k in circ:
        cp = self.to_coord[k]
        points.append(cp)

      # draw circ
      color = colors["circ1"] if i % 2 == 0 else colors["circ2"]
      self.canvas.create_line(points, width=3, fill=color)

  def calc_circ(self, nc):
    circs = calc(self.tubeshigh, self.rowsdeep, nc)
    return circs


if __name__ == "__main__":

  tubebank = TubeBank(title="CoilCirc", 
    tubeshigh=14, rowsdeep=6, pattern="staggered")
  circ = tubebank.calc_circ(2)
  tubebank.draw_circs(circ)
  tubebank.draw_tubes()
  tubebank.mainloop()
