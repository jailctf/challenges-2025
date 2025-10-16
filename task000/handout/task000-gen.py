# lib from https://github.com/google/ARC-GEN/blob/main/common.py
import common


def generate():
  width, height = 10, 10
  num_boxes = common.randint(1, 2)
  color = common.random_color(exclude = [common.black(), common.gray()])
  while True:  # keep trying until we get the desired number of boxes
    rows, cols, wides, talls = [], [], [], []
    for _ in range(num_boxes):
      w = common.randint(2, width - 2)
      t = common.randint(2, height - 2)
      r = common.randint(0, height - t - 2)
      c = common.randint(0, width - w - 2)
      if common.overlaps(rows + [r], cols + [c], wides + [w + 1], talls + [t + 1], 1):
        continue
      rows.append(r)
      cols.append(c)
      wides.append(w)
      talls.append(t)
    if len(wides) == num_boxes: break
  hollows = [common.randint(0, 1) for _ in range(num_boxes)]

  grid, output = common.grids(width, height, common.gray())
  for r, c, w, t, h in zip(rows, cols, wides, talls, hollows):
    for row in range(r, r + t):
      for col in range(c, c + w):
        if h and row not in [r, r + t - 1] and col not in [c, c + w - 1]:
          continue
        output[row][col] = grid[row][col] = color
  
  # example solution
  for r, row in enumerate(output):
    for c, color in enumerate(row):
     if r and c and color==5 and output[r-1][c-1] not in [0,5]: output[r][c]=0

  return {"input": grid, "output": output}


def validate():
  pass