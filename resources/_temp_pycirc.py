"""
Coil TubeBank Circuiting Tools.
  - based on Hamiltonian Path from start node.
  - graph adj is arranged to be in a "preferred" order.
"""

__author__ = "Bruce Wernick"
__date__ = "18 July 2025"

import sys
import math
from collections import defaultdict
from itertools import islice
from functools import reduce
import tkinter as tk

class Map:
  """ Map between coords (Row,Col) and tube id (k)
      for a staggered tube bank.
  """
  # lookup dicts
  arr = [] # list of coords
  obj = defaultdict(lambda: None)  # maps coord to index

  @classmethod
  def set_size(cls, tubeshigh, rowsdeep):

    cls.arr.clear()
    cls.obj.clear()

    cols, rows = rowsdeep, 2*tubeshigh
    k = 0
    for r in range(rows):
      col0 = r % 2
      for c in range(col0, cols, 2):
        coord = (r, c)
        cls.arr.append(coord)
        cls.obj[coord] = k
        k += 1

  @classmethod
  def rc2k(cls, rc):
    """ row,col to index convert
    """
    return cls.obj[rc]

  @classmethod
  def k2rc(cls, k):
    """ index to row,col convert
    """
    return cls.arr[k]

# ----------------------------------------------------------------------

def get_neighbors(r, c, steps, rows, cols):
  return [(r + i, c + j) for (i, j) in steps if 0 <= r + i < rows and 0 <= c + j < cols]

def create_adj(tubeshigh, rowsdeep):
  """ Return a fully populated adj list dictionary for a
      staggered tube coil tube bank. The neighbors order
      is arranged to be in a suitable order for a fast
      hamiltonian search.
  """

  if tubeshigh <= 0 or rowsdeep <= 0:
    raise ValueError("tubeshigh and rowsdeep must be positive integers.")

  # conventional array dimensions
  rows = 2 * tubeshigh
  cols = rowsdeep

  def limits(cp):
    """ make sure the point is within the grid.
    """
    r, c = cp
    return (0 <= r < rows) and (0 <= c < cols)

  adj = {}

  # assign meaning to step names (r, c)
  left      = ( 0, -2)
  right     = ( 0,  2)
  up        = (-2,  0)
  down      = ( 2,  0)
  upleft    = (-1, -1)
  upright   = (-1,  1)
  downleft  = ( 1, -1)
  downright = ( 1,  1)

  # create adjacent links in the order of preferred valid steps
  steps1 = [right, downright, downleft, upleft, upright, left, down, up]
  steps2 = [left, downleft, downright, upright, upleft, right, down, up]

  for r in range(rows):
    for c in range(cols):
      if r % 2 == 0:
        if c % 2 == 0:
          adj[(r,c)] = [(r+i,c+j) for (i,j) in steps1]
      else:
        if c % 2 != 0:
          adj[(r,c)] = [(r+i,c+j) for (i,j) in steps2]

  # filter out of limit values
  for key, value in adj.items():
    value = filter(limits, value)
    adj[key] = list(value)

  # convert all (r,c) values in adj to index
  result = {}
  for key, value in adj.items():
    temp = []
    for item in value:
      temp.append(Map.rc2k(item))
    result[Map.rc2k(key)] = temp

  return result

def filter_adj(adj, arr):
  """ remove from adj values not in arr
  """
  result = {}
  for key, value in adj.items():
    if key in arr:
      temp = []
      for item in value:
        if item in arr:
          temp.append(item)
      result[key] = temp
  return result

def diag_order(tubeshigh, rowsdeep):
  """ Return list of tube id's in diagonal order.
      Starts at top right corner and traverses diagonally upwards.
  """
  result = []
  rows = 2 * tubeshigh
  cols = rowsdeep
  row, col = 0, cols-1
  while (row < rows) and (col >= 0):
    r, c = row, col
    while (r >= 0) and (c >= 0):
      k = Map.rc2k((r,c))
      if k != -1:
        result.append(k)
      r -= 1
      c -= 1
    if row < rows-1:
      row += 1
      col = cols-1
    else:
      row = rows-1
      col -= 1
  return result

def calc_factors(n):
  """ Return all factors of n.
  """
  fs = set()
  for i in range(1, 1+int(n**0.5)):
    div, mod = divmod(n, i)
    if mod == 0:
      fs |= {i, div}
  return sorted(list(fs))

# ----------------------------------------------------------------------

def find_ham_path_heuristic(graph, start, goal):
  ## Implement a heuristic-based approach (e.g., 2-Opt)
  pass

def find_ham_path(graph, start, goal):
  """ Hamiltonian path search (recursive).
  """
  size = len(graph)

  def search_from(cp, path=[]):
    path = path + [cp]
    if cp == goal and len(path) == size:
      return path
    for np in graph[cp]:
      if np not in path:
        new_path = search_from(np, path)
        if new_path:
          return new_path

  return search_from(start)

def chunk(arr_range, arr_size):
  arr_range = iter(arr_range)
  return list(iter(lambda: tuple(islice(arr_range, arr_size)), ()))

# ----------------------------------------------------------------------

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
    k = Map.rc2k((r, c))
    print(f"id={id}")
    self.tooltip = self.canvas.create_text(x, y + 10, text=str(Map.rc2k((r, c))), fill="black")

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
      circ.append(Map.k2rc(item))
    circs.append(circ)

  TubeBankForm(root, tubeshigh, rowsdeep, circs)

  root.mainloop()

# ----------------------------------------------------------------------

def calc(tubeshigh=16, rowsdeep=5, nc=8):
  """ calc circuits and draw
  """
  tubecount = tubeshigh * rowsdeep
  factors = calc_factors(tubecount)
  #print(factors)

  tpc = tubecount // nc # tubes per circ

  # init a global index converter
  Map.set_size(tubeshigh, rowsdeep)

  # create a full adj list
  graph = create_adj(tubeshigh, rowsdeep)
  #print(graph)

  # pull out a short list from the 1st tpc
  diag_tube_list = diag_order(tubeshigh, rowsdeep)
  circs = chunk(diag_tube_list, tpc)

  paths = []
  for tubes_in_circ in circs:
    # filter the graph
    circ = filter_adj(graph, tubes_in_circ)

    # get 1st key
    all_keys = list(circ.keys())
    start = all_keys[0]
    goal = all_keys[-1]

    # find a path
    path = find_ham_path(circ, start, goal)
    #print(path)
    paths.append(path)

  return paths


if __name__ == "__main__":
  tubeshigh = 14
  rowsdeep = 6
  nt = tubeshigh * rowsdeep
  factors = calc_factors(nt)
  #print(factors)
  nc = 4
  paths = calc(tubeshigh, rowsdeep, nc)
  #print(paths)
  # draw to canvas
  draw_tubebank(tubeshigh, rowsdeep, paths)
