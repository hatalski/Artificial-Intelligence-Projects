import math
import statistics

class Utility:
  def __init__(self):
    self.available_cells = 0
    self.max_tile = 0
    self.monotonic = 0
    self.smoothness = 0
    self.merges = 0
    self.max_tile_in_corner = 0
    self.average_value = 0
    self.total = 0

  def display_features(self):
    print(f'''
total: {self.total} 
available_cells: {self.available_cells}
max_tile: {self.max_tile}
monotonic: {self.monotonic}
smoothness: {self.smoothness}
merges: {self.merges}
max_tile_in_corner: {self.max_tile_in_corner}
average_value: {self.average_value}
    ''')

  def score(self, grid):
    self.available_cells = len(grid.getAvailableCells())
    #self.max_tile = math.log2(grid.getMaxTile())
    #self.average_value = self.average_tile_value(grid, grid.size)
    self.monotonic = self.monotonic_score(grid)*0.9
    self.merges = self.potential_merges_score(grid)*0.8
    self.smoothness = -round(self.smoothness_score(grid)*0.1, 1)
    self.max_tile_in_corner = self.max_value_in_the_corner(grid, grid.size)
    self.total = sum([self.available_cells, self.max_tile, self.average_value,
                      self.monotonic, self.merges, self.smoothness, self.max_tile_in_corner])
    return round(self.total, 1)

  @staticmethod
  def find_mergeable_pairs(l):
    """
    Returns number of mergeable pairs in an array (grid column or row).
    Possible options are 0, 1 and 2 for an array with 4 elements.
    
    Examples: [0, 2, 4, 0] returns 0; [16, 0, 16, 0] and [2, 0, 2, 2] returns 1; [4, 4, 2, 2] and [4, 4, 4, 4] retuns 2.
    
    Note: tested only for 4 elements in an array.
    """
    pairs = 0
    looked_up = set()
    size = len(l)
    for i in range(0, size):
      v = l[i]
      if v == 0 or v in looked_up:
        continue
      n = i
      encounters = {v: 1}
      while n + 1 < size:
        n += 1
        if l[n] == 0:
          continue
        if l[n] == v:
          encounters[v] += 1
        else:
          break
      if encounters[v] // 2 > 0:
        pairs += encounters[v] // 2
        looked_up.add(v)

    return pairs

  @staticmethod
  def strictly_increasing(L):
    """
    Returns True if values in an array are monotonically increasing.
    """
    return all(x < y for x, y in zip(L, L[1:]))

  @staticmethod
  def strictly_decreasing(L):
    """
    Returns True if values in an array are monotonically decreasing.
    """
    return all(x > y for x, y in zip(L, L[1:]))

  def monotonic_score(self, grid):
    """
    Returns number of monotonic rows and columns in a grid,
    where tiles are ordered ascending or descending based on their values.
    """
    score = 0
    for x in range(grid.size):
      col = []
      row = []
      for y in range(grid.size):
        row.append(grid.map[x][y])
        col.append(grid.map[y][x])
      if Utility.strictly_increasing(row) or Utility.strictly_decreasing(row):
        score += 1
      if Utility.strictly_increasing(col) or Utility.strictly_decreasing(col):
        score += 1
    return score

  def smoothness_score(self, grid):
    """
    Returns sum of a base 2 logarithm value difference of unique neighbor tile pairs found in grid.
    """
    size = grid.size
    #looked_up_pos = set()
    score = 0
    for x in range(size):
      for y in range(size):
        tile_value = grid.map[x][y]
        if tile_value == 0:
          continue
        # since we are going from left to right and from top to bottom
        # no need to look for values up and left: these pairs are already processed
        nx = x
        while grid.getCellValue((nx+1, y)) != None:
          nx += 1
          neighbor_value = grid.getCellValue((nx, y))
          if neighbor_value == 0:
            continue
          else:
            score += abs(math.log2(tile_value) - math.log2(neighbor_value))
            break
        ny = y
        while grid.getCellValue((x, ny+1)) != None:
          ny += 1
          neighbor_value = grid.getCellValue((x, ny))
          if neighbor_value == 0:
            continue
          else:
            score += abs(math.log2(tile_value) - math.log2(neighbor_value))
            break
        #looked_up_pos.add((x,y))
    return score

  def potential_merges_score(self, grid):
    """
    Return number of mergeable pairs in a grid.
    """
    merges = 0
    columns = list(zip(*grid.map))
    for c in columns:
      merges += Utility.find_mergeable_pairs(c)
    for r in range(0, grid.size):
      merges += Utility.find_mergeable_pairs(grid.map[r])
    return merges

  def average_tile_value(self, grid, size):
    """
    Returns average value of all non-empty tiles in a grid.
    """
    values = []
    for x in range(size):
      for y in range(size):
        v = grid.map[x][y]
        if v != 0:
          values.append(v)
    if len(values) == 0:
      return 0
    return round(statistics.mean(values))

  # EXPERIMENTATIONAL METHODS

  def max_value_in_the_corner(self, grid, size):
    """
    Returns 2 if tile with maximum value is in the corner (any corner). Otherwise, returns 0.
    """
    max_value = grid.getMaxTile()
    last = size - 1
    if grid.map[0][0] == max_value or grid.map[0][last] == max_value or grid.map[last][0] == max_value or grid.map[last][last] == max_value:
      return 2
    return 0

  def column_sum_more_than_others(self, grid, size, column=0):
    s = []
    for x in range(size):
      s.append(0)
      for y in range(size):
        v = grid.map[y][x]
        s[x] = s[x] + v
    if s[column] == max(s):
      return 1
    return 0
