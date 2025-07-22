
# read version from installed package
from importlib.metadata import version
__version__ = version("pycirc")


from .coil_circ_calc import calc_circs
from .coil_circ_draw import create_xymap,draw_circuits,draw_tube_bank
