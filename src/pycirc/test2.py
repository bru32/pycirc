# test2

from collections import defaultdict
from itertools import islice


def create_rcmap(tubeshigh, rowsdeep):
  RC = defaultdict(lambda: None)
  cols, rows = rowsdeep, 2*tubeshigh
  k = 0
  for r in range(rows):
    col0 = r % 2
    for c in range(col0, cols, 2):
      RC[(r,c)] = k
      k += 1
  return RC

def get_neighbors(r, c, steps, rows, cols):
  return [(r+i, c+j) for (i, j) in steps if 0 <= r + i < rows and 0 <= c + j < cols]

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
      temp.append(RC[item])
    result[RC[key]] = temp

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
      k = RC[(r,c)]
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


def calc(tubeshigh=14, rowsdeep=6, nc=4):
  """ calc circuits
  """
  global RC

  tubecount = tubeshigh * rowsdeep
  factors = calc_factors(tubecount)
  #print(factors)

  tpc = tubecount // nc # tubes per circ

  # init a global index converter
  RC = create_rcmap(tubeshigh, rowsdeep)

  # create a full adj list
  graph = create_adj(tubeshigh, rowsdeep)
  #print(graph)

  # pull out a short list from the 1st tpc
  diag_tube_list = diag_order(tubeshigh, rowsdeep)

  # filter out the None values
  filtered_list = list(filter(lambda item: item is not None, diag_tube_list))

  # break into chunks of tubes per circuit
  circs = chunk(filtered_list, tpc)

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
    paths.append(path)

  return paths


# ---------------------------------------------------------

if __name__ == "__main__":
  paths = calc()
