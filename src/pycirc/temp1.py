# better way to get index from (r,c)

def rc_to_index(r, c, cols):
  if r % 2 != c % 2: return None
  if not(0 <= c < cols): return None
  return (c + r * cols) // 2

tubeshigh = 14
rowsdeep = 6
for r in range(2*tubeshigh):
  for c in range(rowsdeep):
    k = rc_to_index(r, c, rowsdeep)
    if k != None:
      print(f"{k:2d}", end=" ")
    else:
      print(" +", end=" ")
  print()

