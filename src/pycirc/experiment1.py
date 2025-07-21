# Experiment1

import tkinter as tk
from tkmonkey import *
from test2 import calc

# global parameters
x0, y0 = 40, 10
sx, sy = 12, 8


def create_xymap(tubeshigh, rowsdeep):
  """ Create a list XY that maps tube index k to
      screen coordinates (x,y).
  """
  XY = []
  k = 0
  cols, rows = rowsdeep, 2*tubeshigh
  for r in range(rows):
    col0 = r % 2
    for c in range(col0, cols, 2):
      x = x0 + c*sx
      y = y0 + r*sy
      XY.append((x,y))
      k += 1
  return XY


def draw_tube(canvas, x, y):
  w = 3
  coords = x-w, y-w, x+w, y+w
  canvas.create_oval(coords, width=1, outline="black", fill="white")


def draw_tube_bank(canvas, tubeshigh, rowsdeep, nc):
  XY = create_xymap(tubeshigh, rowsdeep)
  circs = calc(tubeshigh, rowsdeep, nc)

  """
  # draw circuits (fast - no color or line width)
  for circ in circs:
    arr = []
    for k in circ:
      arr.append(XY[k])
    canvas.create_line(arr)
  """

  # draw circuits (alt color and line width)
  for i,circ in enumerate(circs):
    color = "tomato" if i % 2 == 0 else "cadetblue"
    x1, y1 = XY[circ[0]]
    for j in range(1, len(circ)):
      linewidth = 0 if j % 2 == 0 else 3
      x2, y2 = XY[circ[j]]
      coords = x1, y1, x2, y2
      canvas.create_line(coords, width=linewidth, fill=color)
      x1, y1 = x2, y2

  # draw tubes
  ntubes = tubeshigh * rowsdeep
  for k in range(ntubes):
    x, y = XY[k]
    draw_tube(canvas, x, y)


if __name__ == "__main__":
  root = tk.Tk()
  root.geometry("400x600+500+10")
  frame = tk.Frame(root)
  frame.pack(expand=True, fill="both")
  canvas = tk.Canvas(frame)
  canvas.pack(expand=True, fill="both")
  draw_tube_bank(canvas, 13, 5, 3)
  root.mainloop()
