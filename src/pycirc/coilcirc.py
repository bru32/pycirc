""" 
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
    self.edit = tk.Entry(self, width=16, textvariable=self.inputfield.var)
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

  # remove duplicates
  pattern = {}
  for circ in circs:
    a = circ[0]
    arr = [x - a for x in circ]
    if not arr in pattern.values():
      pattern[a] = arr
  arr = []
  for key, value in pattern.items():
    arr.append([key+a for a in value])

  XY = create_xymap(tubeshigh, rowsdeep)
  draw_circuits(canvas, XY, arr)
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

  # read the last canvas size
  canvas_width = canvas.winfo_width()
  canvas_height = canvas.winfo_height()
  x_pos = root.winfo_x()
  y_pos = root.winfo_y()

  with open("config.json", "w") as fp:
    config = {
      "mainform": {"x": x_pos, "y": y_pos},
      "canvas": {"width": canvas_width, "height": canvas_height},
      "tubeshigh": var1.get(),
      "rowsdeep": var2.get(),
      "nc": var3.get()}
    json.dump(config, fp, indent=2)

  root.quit()
  root.destroy()  


def on_mouse_wheel(event):
  """ Handle mouse wheel scrolling.
  """
  if event.delta > 0:
    canvas.yview_scroll(-1, "units")
  else:
    canvas.yview_scroll(1, "units")


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

  with open("config.json", "r") as fp:
    config = json.load(fp)
    x_pos = config.get("mainform", {}).get("x", 100)
    y_pos = config.get("mainform", {}).get("y", 100)
    canvas_width = config.get("canvas", {}).get("width", 300)
    canvas_height = config.get("canvas", {}).get("height", 500)
    tubeshigh = config.get("tubeshigh", tubeshigh)
    rowsdeep = config.get("rowsdeep", rowsdeep)
    nc = config.get("nc", nc)

  root.geometry(f"+{x_pos}+{y_pos}")

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

  frame3 = tk.Frame(frame1)
  frame3.pack(side="left", fill="both", expand=True)

  canvas = tk.Canvas(frame3, background="ivory2", 
    scrollregion=(0,0,1000,4000))


  hbar = tk.Scrollbar(frame3,orient="horizontal")
  hbar.pack(side="bottom",fill="x")
  hbar.config(command=canvas.xview)
  vbar=tk.Scrollbar(frame3,orient="vertical")
  vbar.pack(side="right",fill="y")
  vbar.config(command=canvas.yview)
  canvas.config(width=canvas_width, height=canvas_height)
  canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
  canvas.pack(side="left", expand=True, fill="both")

  root.bind_all("<MouseWheel>", on_mouse_wheel)

  do_calc()  # initial calculation

  root.mainloop()