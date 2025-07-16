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
  STAGGERED: str = "staggered"
  INLINE: str = "inline"

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
  sy = 38  # more suitable for a neater plot
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

    # prepare ...
    self.tube_pos = defaultdict(list[int])
    self.generate_index()
    self.draw_end_plate()

    # Notes
    xy = {"x": 280, "y": 20}
    for note in ["6 rows deep", "14 tubes high", 
      "7 circuits", "12 tubes per circuit"]:
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
    self.tube_pos.clear()
    for r in range(rowsdeep):
      x = x0 + r * sx
      if staggered:
        dt = 0 if r % 2 == 0 else 0.5
      for t in range(tubeshigh):
        y = y0 + (t + dt) * sy
        k = r + t * rowsdeep
        self.tube_pos[k] = (x, y)

  def draw_end_plate(self):
    """ draw end-plate
    """    
    x0 = TubeBank.x0
    y0 = TubeBank.y0
    sx = TubeBank.sx
    sy = TubeBank.sy
    dt = 0.5 if self.staggered else 0
    x1 = x0 + sx*(self.rowsdeep - 1)
    y1 = y0 + sy*(self.tubeshigh - 1 + dt)
    g = sx/2
    coords = x0-g, y0-g, x1+g, y1+g
    self.canvas.create_rectangle(coords,
      fill=colors["endplate"])

  def draw_tubes(self):
    """ draw all tubes in bank
    """
    r = 5  # sized for looks, not proportional.
    for k, (x, y) in self.tube_pos.items():
      self.canvas.create_hexagon(x, y, r,
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
        cp = self.tube_pos[k]
        points.append(cp)

      # draw circ
      color = colors["circ1"] if i % 2 == 0 else colors["circ2"]
      self.canvas.create_line(points, width=3, fill=color)

  def calc_circ(self):

    circs = [(0,2,4,5,3,1,8,10,11,9,16,17),
      (6,7,12,14,13,15,20,22,21,23,28,29),
      (18,19,24,26,25,27,32,34,33,35,40,41),
      (30,31,36,38,37,39,44,46,45,47,52,53),
      (42,43,48,50,49,51,56,58,57,59,64,65),
      (54,55,60,62,61,63,68,70,69,71,76,77),
      (66,67,72,74,73,75,82,80,78,79,81,83)]

    return circs

if __name__ == "__main__":

  tubebank = TubeBank(title="CoilCirc", 
    tubeshigh=14, rowsdeep=6, pattern="staggered")
  circ = tubebank.calc_circ()
  tubebank.draw_circs(circ)
  tubebank.draw_tubes()
  tubebank.mainloop()
