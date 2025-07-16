# tkinter Monkey patching

from math import sin, cos, radians
import tkinter as tk


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
  for i in range(6):
    a = radians(60*i)
    coords.append((x+r*cos(a), y+r*sin(a)))
  return self.create_polygon(coords, **kwargs)
tk.Canvas.create_hexagon = _create_hexagon

