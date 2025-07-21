"""
tkinter Monkey patching to create various standard
shapes that can be called exactly like create_rectangle.
  - create_circle
  - create_square
  - create_diamond
  - reate_hexagon
  - create_triangle
"""

__author__ = "Bruce Wernick"
__date__ = "19 July 2025"


from math import sin, cos, radians
import tkinter as tk


def _create_tube(self, x, y, r=3, **kwargs):
  return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_tube = _create_tube

def _create_circle(self, x, y, r, **kwargs):
  return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle

def _create_square(self, x, y, r, **kwargs):
  return self.create_rectangle(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_square = _create_square

def _create_diamond(self, x, y, r, **kwargs):
  coords = x-r, y, x, y-r, x+r, y, x, y+r, x-r, y
  return self.create_polygon(coords, **kwargs)
tk.Canvas.create_diamond = _create_diamond

def _create_hexagon(self, x, y, r, **kwargs):
  coords = []
  for i in range(7):
    a = radians(60*i)
    coords.append((x+r*cos(a), y+r*sin(a)))
  return self.create_polygon(coords, **kwargs)
tk.Canvas.create_hexagon = _create_hexagon

def _create_triangle(self, x, y, r, **kwargs):
  coords = [x-r,y-r,x+r,y,x-r,y+r,x-r,y-r]
  return self.create_polygon(coords, **kwargs)
tk.Canvas.create_triangle = _create_triangle


def _create_alt_line(self, arr, color1="red", color2="green", **kwargs):
  """ create alternating line on canvas.
  """
  a = arr[0]
  for i in range(1, len(arr)):
    color = color1 if i % 2 == 0 else color2
    b = arr[i]
    self.create_line(a, b, fill=color, **kwargs)
    a = b
tk.Canvas.create_alt_line = _create_alt_line


if __name__ == "__main__":

  # check of they work...
  root = tk.Tk()
  canvas = tk.Canvas(root, width=640)
  canvas.pack()
  opts = {"fill":"red", "outline": "black", "width":2}
  canvas.create_circle(100, 100, 40, **opts)
  canvas.create_square(210, 100, 40, **opts)
  canvas.create_diamond(320, 100, 40, **opts)
  canvas.create_hexagon(430, 100, 40, **opts)
  canvas.create_triangle(540, 100, 40, **opts)
  root.mainloop()