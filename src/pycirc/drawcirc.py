"""
Draw tube bank with tkinter.
"""

import tkinter as tk


class TubeBankForm(tk.Frame):

  """ Simple Tube Bank form.
      Draw tubes and circuit to tkinter canvas.
  """

  def __init__(self, master, tubeshigh, rowsdeep, paths, *args, **kwargs):
    self.master = master
    super().__init__(master, *args, **kwargs)
    self.pack(fill="both", expand=1)

    # create canvas for drawing
    self.canvas= tk.Canvas(self, bg="whitesmoke")
    self.canvas.pack(fill="both", expand=1)

    # draw circuit
    for path in paths:
      self.draw_circuit(path)

    # draw nodes
    self.draw_nodes(tubeshigh, rowsdeep)

  def XY(self, c, r):
    """ translate from (col,row) coords to
        screen (x,y) values.
    """
    x0, y0 = 20, 20
    sx, sy = 23, 27
    x = c * sx
    y = r * sy
    if c % 2 != 0:
      y += 0.5*sy
    return x0 + x, y0 + y

  def draw_node(self, c, r):
    """ draw node at grid position (c,r)
    """
    rad = 5
    x, y = self.XY(c, r)
    coords = x-rad, y-rad, x+rad, y+rad

    oval = self.canvas.create_oval(coords, width=1, outline="black", fill="white")
    #self.canvas.tag_bind(oval, "<Enter>", lambda e: self.show_tooltip(c, r))
    #self.canvas.tag_bind(oval, "<Leave>", lambda e: self.hide_tooltip())

  def show_tooltip(self, c, r):
    x, y = self.XY(c, r)
    k = idconv.rc2k((r, c))
    print(f"id={id}")
    self.tooltip = self.canvas.create_text(x, y + 10, text=str(idconv.rc2k((r, c))), fill="black")

  def hide_tooltip(self):
    self.canvas.delete(self.tooltip)    
    pass

  def draw_nodes(self, rows=6, cols=4):
    """ draw all nodes
    """
    for r in range(rows):
      for c in range(cols):
        self.draw_node(c, r)

  def draw_link(self, c1, r1, c2, r2):
    """ draw single link from grid pos 1 to 2
    """
    coords = self.XY(c1, r1), self.XY(c2, r2)
    self.canvas.create_line(coords, width=2, fill="gray")

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


# ----------------------------------------------------------------------

def draw_tubebank(tubeshigh, rowsdeep, paths):
  """ driver for tube bank form.
  """
  root = tk.Tk()
  root.title("TubeBank")
  root.geometry("340x600+900+20")

  circs = []
  for path in paths:
    if not path:
      continue
    circ = []
    for item in path:
      circ.append(idconv.k2rc(item))
    circs.append(circ)

  TubeBankForm(root, tubeshigh, rowsdeep, circs)

  root.mainloop()

