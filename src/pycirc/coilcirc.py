""" 
pycirc demo.
The circuit calculation returns lists of tube id's. 
These can be used to draw on any canvas.  The example 
below demonstrates the use of a tkinter canvas.
"""

__author__ = "Bruce Wernick"
__date__ = "22 July 2025"

import os
import json
from dataclasses import dataclass
import tkinter as tk
from pycirc import *


@dataclass
class InputField:
  label: str
  var: tk.IntVar


class EntryFrame(tk.Frame):
  def __init__(self, master=None, inputfield=InputField, **kwargs):
    super().__init__(master, **kwargs)
    self.master = master
    self.inputfield = inputfield
    self.create_widgets()

  def create_widgets(self):
    self.label = tk.Label(self, text=self.inputfield.label)
    self.label.pack(padx=2, pady=2)
    self.edit = tk.Entry(self, width=20, textvariable=self.inputfield.var)
    self.edit.pack(padx=5, pady=5)


def do_calc():
  """ Calculate and draw the circuit and tube bank.
  """
  canvas.delete("all")

  # get values from entry fields
  tubeshigh = int(var1.get())
  rowsdeep = int(var2.get())
  nc = int(var3.get())

  # re-calculate all
  circs = calc_circs(tubeshigh, rowsdeep, nc)
  XY = create_xymap(tubeshigh, rowsdeep)
  draw_circuits(canvas, XY, circs)
  draw_tube_bank(canvas, XY)


def show_help():
  """ open help page in browser.
  """
  import webbrowser
  fname = os.path.join("..", "..", "help", "index.html")
  path = os.path.abspath(fname)
  uri = "file://" + path
  webbrowser.open(uri, new=2)

def close_app():
  """ Exit the application.
  """
  with open("coilcirc.json", "w") as f:
    config = {
      "tubeshigh": var1.get(),
      "rowsdeep": var2.get(),
      "nc": var3.get()}
    json.dump(config, f, indent=2)
  root.quit()
  root.destroy()  

# ---------------------------------------------------------

if __name__ == "__main__":

  root = tk.Tk()
  root.title("CoilCirc - version 0.1.0")
  root.iconbitmap("coilcirc.ico")
  root.protocol("WM_DELETE_WINDOW", close_app)

  # container frame
  frame1 = tk.Frame(root)
  frame1.pack(expand=True, fill="both")

  # entry frame
  frame2 = tk.Frame(frame1)
  frame2.pack(side="left", fill="y")

  # default values
  tubeshigh = 14
  rowsdeep = 6
  nc = 4

  with open("coilcirc.json", "r") as f:
    config = json.load(f)
    tubeshigh = config.get("tubeshigh", tubeshigh)
    rowsdeep = config.get("rowsdeep", rowsdeep)
    nc = config.get("nc", nc)

  var1 = tk.IntVar(value=tubeshigh)
  var2 = tk.IntVar(value=rowsdeep)
  var3 = tk.IntVar(value=nc)

  EntryFrame(frame2, InputField("Tubes high:", var1)).pack(padx=5, pady=5)
  EntryFrame(frame2, InputField("Rows deep:", var2)).pack(padx=5, pady=5)
  EntryFrame(frame2, InputField("No. circuits:", var3)).pack(padx=5, pady=5)

  btn1 = tk.Button(frame2, text="Calculate", 
    width=10, command=do_calc)
  btn1.pack(padx=5, pady=5)

  btn2 = tk.Button(frame2, text="Help Index", 
    width=10, command=show_help)
  btn2.pack(padx=5, pady=5)

  btn3 = tk.Button(frame2, text="Quit", 
    width=10, command=close_app)
  btn3.pack(padx=5, pady=5)

  canvas = tk.Canvas(frame1, background="ivory2")
  canvas.pack(expand=True, fill="both")

  root.mainloop()