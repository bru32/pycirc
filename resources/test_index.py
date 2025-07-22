"""This is purely to test the different index counting methods
"""

from collections import defaultdict

def method1(tubeshigh, rowsdeep):
  A = []  # list of coordinates (x,y)
  B = defaultdict(lambda: None) # map B[(x,y)]=k
  k = 0
  for t in range(tubeshigh):
    for r in range(rowsdeep):
      coord = (t, r)
      A.append(coord)
      B[coord] = k
      k += 1
  return A, B
  
def method2(tubeshigh, rowsdeep):
  A = []  # list of coordinates (x,y)
  B = defaultdict(lambda: None) # map B[(x,y)]=k
  cols, rows = rowsdeep, 2*tubeshigh
  k = 0
  for r in range(rows):
    col0 = r % 2
    for c in range(col0, cols, 2):
      coord = (r, c)
      A.append(coord)
      B[coord] = k
      k += 1
  return A, B

# plot tube patterns to compare
import tkinter as tk
root = tk.Tk()
canvas = tk.Canvas(root, width=600, height=600)
canvas.pack(expand=True, fill="both")
opts = {"anchor":"c", "justify":"center"}

tubeshigh, rowsdeep = 14, 6 
ntubes = tubeshigh*rowsdeep

# for drawing only
x0, y0 = 25, 20
sx, sy = 33, 38

A, B = method1(tubeshigh, rowsdeep)
#print(len(A))
arr = []
for k in range(ntubes):
  t, r = A[k]
  x = x0 + r*sx
  dt = 0 if r % 2 == 0 else 0.5
  y = y0 + (t + dt)*sy
  arr.append((x,y))
  canvas.create_text(x, y, text=f"{k}", **opts)
#canvas.create_line(arr)
for t in range(tubeshigh):
  arr = []
  for r in range(rowsdeep):
    x = x0 + r*sx
    dt = 0 if r % 2 == 0 else 0.5
    y = y0 + (t + dt)*sy
    arr.append((x,y))
  canvas.create_line(arr, fill="gray", dash=(2,2))


A, B = method2(tubeshigh, rowsdeep)
#print(len(A))
arr = []
for k in range(ntubes):
  r, c = A[k]
  x = x0 + c*sx + 300  # offset to be on same canvas
  y = y0 + r*sy / 2
  arr.append((x,y))
  canvas.create_text(x, y, text=f"{k}", **opts)
#canvas.create_line(arr)
for r in range(2*tubeshigh):
  arr = []
  for c in range(rowsdeep):
    x = x0 + c*sx + 300  # offset to be on same canvas
    y = y0 + r*sy / 2
    arr.append((x,y))
  canvas.create_line(arr, fill="gray", dash=(2,2))

root.mainloop()
