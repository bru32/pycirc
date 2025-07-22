""" Staggered tube pattern circuit drawing tool.
"""

__author__ = "Bruce Wernick"
__date__ = "22 July 2025"

from enum import StrEnum


__all__ = ["DrawingStyle", "create_xymap",
           "draw_circuits", "draw_tube_bank"]

# global parameters
x0, y0 = 40, 10 # x and y position of top left tube
sx, sy = 12, 8  # x and y scale factors


class DrawingStyle(StrEnum):
  BASIC = "basic"
  NICE = "nice"
  @classmethod
  def _missing_(cls, value):
    value = value.lower()
    for member in cls:
      if member == value:
        return member
    return None


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


def draw_circuits(canvas, XY, circs, style=DrawingStyle.NICE):
  """ Draw the circuits.
      style = basic or nice
  """

  if style == DrawingStyle.NICE:

    # draw circuits with nice appearance:
    # - alternating color and line width.

    for i,circ in enumerate(circs):
      color = "tomato" if i % 2 == 0 else "cadetblue"
      x1, y1 = XY[circ[0]]
      for j in range(1, len(circ)):
        linewidth = 0 if j % 2 == 0 else 3
        x2, y2 = XY[circ[j]]
        coords = x1, y1, x2, y2
        canvas.create_line(coords, width=linewidth, fill=color)
        x1, y1 = x2, y2

  else:

    # draw circuits fast with basic styling:
    # - no color or line width.

    for circ in circs:
      arr = []
      for k in circ:
        arr.append(XY[k])
      canvas.create_line(arr, width=1, fill="black")


def draw_tube(canvas, x, y):
  """ Draw a single tube at (x,y) screen coordinates.
  """
  w = 3
  coords = x-w, y-w, x+w, y+w
  canvas.create_oval(coords, width=1, outline="black", fill="white")


def draw_tube_bank(canvas, XY):
  """ Draw all tubes.
  """
  for x,y in XY:
    draw_tube(canvas, x, y)

