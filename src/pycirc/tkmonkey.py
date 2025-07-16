# tkinter Monkey patching

import tkinter as tk


def _create_circle(self, x, y, r, **kwargs):
  return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle

def _create_square(self, x, y, r, **kwargs):
  return self.create_rectangle(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_square = _create_square
