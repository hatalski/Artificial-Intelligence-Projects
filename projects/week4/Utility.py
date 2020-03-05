import math
import statistics

class Utility:
  def __init__(self):
    self.available_cells = 0
    self.max_tile = 0
    self.monotonic = 0
    self.smoothness = 0
    self.merge_pairs = 0
    self.merge_score = 0
    self.center_edges_diff = 0
    self.max_tile_in_corner = 0
    self.average_value = 0
    self.moves_score = 0
    self.total = 0

  def display_features(self):
    print(f'''
total: {self.total} 
available_cells: {self.available_cells}
max_tile: {self.max_tile}
monotonic: {self.monotonic}
smoothness: {self.smoothness}
merge_pairs: {self.merge_pairs}
merge_score: {self.merge_score}
center_edges_diff: {self.center_edges_diff}
max_tile_in_corner: {self.max_tile_in_corner}
moves_score: {self.moves_score}
average_value: {self.average_value}
    ''')

  def score(self, grid):
    self.available_cells = len(grid.getAvailableCells())
    #self.max_tile = math.log2(grid.getMaxTile())
    #self.average_value = self.average_tile_value(grid, grid.size)
    self.monotonic = self.monotonic_score(grid)
    self.merge_pairs, self.merge_score = self.potential_merges_score(grid)
    self.smoothness = -self.smoothness_score(grid) // 2
    self.center_edges_diff = self.grid_center_to_edges_value_diff(grid) // 2
    self.max_tile_in_corner = self.max_value_in_the_corner(grid, grid.size)
    #self.moves_score = self.insufficient_moves_variety_score(grid)
    # self.total = sum([self.available_cells, self.max_tile, self.average_value, self.moves_score,
    #                   self.monotonic, self.merge_score, self.smoothness, self.max_tile_in_corner])
    self.total = self.available_cells + self.max_tile + \
        self.average_value + self.moves_score + self.center_edges_diff + \
        self.monotonic + self.merge_score + self.smoothness + self.max_tile_in_corner
    return self.total

  @staticmethod
  def find_mergeable_pairs(l):
    """
    Returns number of mergeable pairs in an array (grid column or row).
    Possible options are 0, 1 and 2 for an array with 4 elements.
    
    Examples: [0, 2, 4, 0] returns 0; [16, 0, 16, 0] and [2, 0, 2, 2] returns 1; [4, 4, 2, 2] and [4, 4, 4, 4] retuns 2.
    
    Note: tested only for 4 elements in an array.
    """
    pairs = 0
    value_score = 0
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
        # merge have to be more lucrative with higher value than with lower
        value_score += (encounters[v] // 2) * math.log2(v)
        looked_up.add(v)

    return pairs, value_score

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
    pairs, score = 0, 0
    columns = list(zip(*grid.map))
    for c in columns:
      p, s = Utility.find_mergeable_pairs(c)
      pairs += p
      score += s
    for r in range(0, grid.size):
      p, s = Utility.find_mergeable_pairs(grid.map[r])
      pairs += p
      score += s
    return pairs, score

  # EXPERIMENTATIONAL METHODS
  
  def insufficient_moves_variety_score(self, grid):
    moves_count = len(grid.getAvailableMoves())
    if moves_count == 1:
      return -2
    elif moves_count == 2:
      return -1
    elif moves_count == 3:
      return 2
    else:
      return 0
    
  def grid_center_to_edges_value_diff(self, grid):
    """
    Returns a sum of values on the edges minus a sum of values in the center of a grid.
    """
    size = grid.size
    last = size - 1
    sum_on_edges = 0
    sum_in_center = 0
    for x in range(size):
      for y in range(size):
        v = grid.getCellValue((x, y))
        #print(x,y)
        #print(v)
        if v == 0:
          continue
        if (x == y == 0) or (x == 0 and y == last) or (y == 0 and x == last) or (x == y == last):
          sum_on_edges += math.log2(v)
        elif x == 0 or y == 0 or x == last or y == last:
          sum_on_edges += math.log2(v)
        else:
          sum_in_center += math.log2(v)
        #print(f'sum on edges: {sum_on_edges} and in center: {sum_in_center}')
    return sum_on_edges - sum_in_center
    
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

  def max_value_in_the_corner(self, grid, size):
    """
    Returns 2 if tile with maximum value is in the corner (any corner). Otherwise, returns 0.
    """
    max_value = grid.getMaxTile()
    last = size - 1
    if grid.map[0][0] == max_value or grid.map[0][last] == max_value or grid.map[last][0] == max_value or grid.map[last][last] == max_value:
      return math.log2(max_value)
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
