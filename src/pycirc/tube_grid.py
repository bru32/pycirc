# plot coil tube bank
# Bruce Wernick

import tkinter as tk
from tkinter import ttk
from tkmonkey import *
from fiftyshades import COPPER_RUST


custom_colors = {
  "canvas": "white",
  "tube": COPPER_RUST,
  "my_blue": "#4CAF50",
  "deep_red": "#8B0000",
  "light_gray": "#CCCCCC",
  "cool_green": "forestgreen",
  }

class TubeBank(tk.Tk):

  x0, y0 = 25, 25  # left and top margin for tube bank

  # sy = tube high 1½" = 3*25.4/2 = 38.1mm
  # sx = rows deep √(sy² - ½sy²) = sy*√(3/4) = 0.866*sy = 32.9946mm
  # sx, sy = 32.9946, 38.1  # typical 1/2" coil
  sy = 30  # more suitable for a neater plot
  sx = 26  # keep same proportion (0.866*30=25.98)

  def __init__(self, title="App", size=(600,600), xypos=(600,10), icon=None):
    super().__init__()
    self.title(title)
    
    self.width, self.height = size
    xpos, ypos = xypos
    self.geometry(f"{self.width}x{self.height}+{xpos}+{ypos}")

    # Container frame
    frame = ttk.Frame(self)
    frame.pack(expand=True, fill="both", side="top", padx=0, pady=0)

    self.canvas = tk.Canvas(frame, 
      background=custom_colors["canvas"],
      borderwidth=0, highlightthickness=0, relief="flat")
    self.canvas.pack(expand=True, fill="both", side="top", padx=0, pady=0)
    self.canvas.update()

  def plot(self, tubeshigh=14, rowsdeep=6):
    
    x0 = TubeBank.x0
    y0 = TubeBank.y0

    sx = TubeBank.sx
    sy = TubeBank.sy

    tube_dia = 4  # not proportional

    for r in range(rowsdeep):
      x = x0 + r * sx
      
      # allow for staggered tube pattern
      dt = 0 if r % 2 == 0 else 0.5

      for t in range(tubeshigh):
        y = y0 + (t + dt) * sy
        self.canvas.create_circle(x, y, tube_dia, 
          fill=custom_colors["tube"])



# ---------------------------------------------------------

if __name__ == "__main__":
  tubebank = TubeBank(title="CoilCirc")
  tubebank.plot(14, 6)
  tubebank.mainloop()