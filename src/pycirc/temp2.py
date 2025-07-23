
def unique_paths(paths):
  all = set()
  for path in paths:
    all.add(tuple(path))
  return [list(cp) for cp in all]
