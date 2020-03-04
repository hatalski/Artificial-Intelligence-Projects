from projects.week4.BaseAI import BaseAI
import time
import math
import statistics

algorithm_dict = {
    0: "MINIMAX",
    1: "ALPHABETAPRUNING",
    2: "ALPHABETAPRUNING_ITERATIVEDEPTH"
}

class PlayerAI(BaseAI):
  def __init__(self, algorithm=algorithm_dict[2]):
    self.algorithm = algorithm
    self.move_stats = []

  def getMove(self, grid):
    """
    The getMove() function, which you will need to implement, 
    returns a number that indicates the player’s action. 
    In particular, 0 stands for "Up", 1 stands for "Down", 2 stands for "Left", 
    and 3 stands for "Right".
    """
    alg = AlphaBetaPruningIterativeDepth()
    if self.algorithm == algorithm_dict[0]:
      alg = Minimax(time_limit=0.04)
    elif self.algorithm == algorithm_dict[1]:
      alg = AlphaBetaPruning(time_limit=0.07)
    best_move = alg.search(grid)
    self.move_stats.append(alg.stats())

    return best_move

class BaseAdversialSearch:
  def search(self, grid):
    pass

  def min(self, grid):
    pass

  def max(self, grid):
    pass

  def stats(self):
    pass

  @staticmethod
  def player_move_successors(grid):
    """
    Returns grid successors of all possible Player moves
    """
    successors = []
    moves = grid.getAvailableMoves()
    for move in moves:
      successor = grid.clone()
      if successor.move(move):
        successors.append(successor)
    return successors

  @staticmethod
  def computer_move_successors(grid):
    """
    Returns grid successors of all possible Computer moves
    """
    successors = []
    cells = grid.getAvailableCells()
    for cell_pos in cells:
      successor_2 = grid.clone()
      if successor_2.canInsert(cell_pos):
        successor_2.setCellValue(cell_pos, 2)
        successors.append(successor_2)
      successor_4 = grid.clone()
      if successor_4.canInsert(cell_pos):
        successor_4.setCellValue(cell_pos, 4)
        successors.append(successor_4)
    return successors

  @staticmethod
  def find_best_move(grid, child):
    moves = grid.getAvailableMoves()
    for move in moves:
        successor = grid.clone()
        if successor.move(move):
          if BaseAdversialSearch.compare_grids(successor, child):
            return move
    return None

  @staticmethod
  def compare_grids(grid1, grid2):
    if grid1 is None or grid2 is None:
      return False
    if grid1.size == grid2.size:
      size = grid1.size
      for x in range(size):
        for y in range(size):
          if grid1.map[x][y] != grid2.map[x][y]:
            return False
      return True
    else:
      return False

  @staticmethod
  def terminal_test(grid, start_time=None, time_limit=None):
    """
    Returns True if: 
    time for player's turn exceeds or equal to timeLimit
    or free cells are not available
    or moves are not available
    """
    time_not_available = False
    cells_not_available = len(grid.getAvailableCells()) == 0
    moves_not_available = len(grid.getAvailableMoves()) == 0
    if start_time is not None:
      current = time.process_time()
      diff = current - start_time
      time_not_available = diff >= time_limit

    return cells_not_available or moves_not_available or time_not_available

class Minimax(BaseAdversialSearch):
  def __init__(self, time_limit=0.2):
    self.start_time = time.process_time()
    self.time_limit = time_limit
    self.depth = 0
    self.pruned = 0
    self.elapsed_time = 0
  
  def stats(self):
    return self.pruned, self.depth, self.elapsed_time

  def search(self, grid):
    #self.start_time = time.process_time()
    child, utility = self.max(grid)
    best_move = BaseAdversialSearch.find_best_move(grid, child)
    self.elapsed_time = round(time.process_time() - self.start_time, 8)
    return best_move

  def min(self, grid):
    """
    Action to minimize value is different since Computer places a tile randomly 
    on the grid. However, we should consider that computer's tile placement 
    is not random, but intentional with a goal to minimize player's value.
    """
    if BaseAdversialSearch.terminal_test(grid, self.start_time, self.time_limit):
      return (None, Utility().score(grid))

    self.depth = self.depth + 1
    min_child, min_utility = None, math.inf

    successors = BaseAdversialSearch.computer_move_successors(grid)
    for child in successors:
      _, utility = self.max(child)
      if utility < min_utility:
        min_child, min_utility = child, utility
    
    return min_child, min_utility

  def max(self, grid):
    if BaseAdversialSearch.terminal_test(grid, self.start_time, self.time_limit):
      return (None, Utility().score(grid))

    self.depth = self.depth + 1
    max_child, max_utility = None, -math.inf

    successors = BaseAdversialSearch.player_move_successors(grid)
    for child in successors:
      _, utility = self.min(child)
      if utility > max_utility:
        max_child, max_utility = child, utility

    return max_child, max_utility

class AlphaBetaPruning(BaseAdversialSearch):
  def __init__(self, time_limit=0.2):
    self.start_time = time.process_time()
    self.time_limit = time_limit
    self.depth = 0
    self.pruned = 0
    self.elapsed_time = 0

  def stats(self):
    return self.depth, self.pruned, self.elapsed_time

  def search(self, grid):
    alpha, beta = -math.inf, math.inf
    child, utility = self.max(grid, alpha, beta)
    best_move = BaseAdversialSearch.find_best_move(grid, child)
    self.elapsed_time = round(time.process_time() - self.start_time, 8)
    return best_move

  def min(self, grid, alpha, beta):
    if BaseAdversialSearch.terminal_test(grid, self.start_time, self.time_limit):
      return (None, Utility().score(grid))

    self.depth = self.depth + 1
    min_child, min_utility = None, math.inf

    successors = BaseAdversialSearch.computer_move_successors(grid)
    for child in successors:
      _, utility = self.max(child, alpha, beta)
      if utility < min_utility:
        min_child, min_utility = child, utility
      if min_utility <= alpha:
        self.pruned += 1
        return min_child, min_utility
      beta = min(beta, min_utility)
      print(f'beta:{beta}')

    return min_child, min_utility

  def max(self, grid, alpha, beta):
    if BaseAdversialSearch.terminal_test(grid, self.start_time, self.time_limit):
      return (None, Utility().score(grid))

    self.depth = self.depth + 1
    max_child, max_utility = None, -math.inf

    successors = BaseAdversialSearch.player_move_successors(grid)
    for child in successors:
      _, utility = self.min(child, alpha, beta)
      if utility > max_utility:
        max_child, max_utility = child, utility
      if max_utility >= beta:
        self.pruned += 1
        return max_child, max_utility
      alpha = max(alpha, max_utility)
      print(f'alpha:{alpha}')

    return max_child, max_utility

class AlphaBetaPruningIterativeDepth(BaseAdversialSearch):
  def __init__(self, time_limit=0.2, depth_limit=10, depth_step=1):
    self.start_time = time.process_time()
    self.time_limit = time_limit
    self.depth_limit = depth_limit
    self.depth_step = depth_step
    self.depth = 0
    self.pruned = 0
    self.elapsed_time = 0

  def stats(self):
    return self.depth, self.pruned, round(self.elapsed_time, 8)

  def search(self, grid):
    alpha, beta = -math.inf, math.inf
    child = None
    while self.elapsed_time <= self.time_limit:
      self.depth_limit += self.depth_step
      child, utility = self.max(grid, alpha, beta)
      self.elapsed_time = time.process_time() - self.start_time
    best_move = BaseAdversialSearch.find_best_move(grid, child)
    print(
        f'\ndepth limit: {self.depth_limit} best move: {best_move} pruned:{self.pruned}\nalpha: {alpha} beta: {beta}')
    return best_move

  def min(self, grid, alpha, beta):
    if self.cutoff_test(grid):
      return (None, Utility().score(grid))

    self.depth = self.depth + 1
    min_child, min_utility = None, math.inf

    successors = BaseAdversialSearch.computer_move_successors(grid)
    for child in successors:
      _, utility = self.max(child, alpha, beta)
      if utility < min_utility:
        min_child, min_utility = child, utility
      if min_utility <= alpha:
        self.pruned += 1
        #print(f'pruned min_utility:{min_utility}')
        return min_child, min_utility
      beta = min(beta, min_utility)
    #print(f'beta:{beta} alpha:{alpha}')

    return min_child, min_utility

  def max(self, grid, alpha, beta):
    if self.cutoff_test(grid):
      return (None, Utility().score(grid))

    self.depth = self.depth + 1
    max_child, max_utility = None, -math.inf

    successors = BaseAdversialSearch.player_move_successors(grid)
    for child in successors:
      _, utility = self.min(child, alpha, beta)
      if utility > max_utility:
        max_child, max_utility = child, utility
      if max_utility >= beta:
        self.pruned += 1
        #print(f'pruned max_utility:{max_utility}')
        return max_child, max_utility
      alpha = max(alpha, max_utility)
    #print(f'beta:{beta} alpha:{alpha}')

    return max_child, max_utility

  def cutoff_test(self, grid):
    depth_limit_reached = self.depth >= self.depth_limit
    #cells_na = len(grid.getAvailableCells()) == 0
    moves_na = len(grid.getAvailableMoves()) == 0

    return depth_limit_reached or moves_na

class AlphaBetaPruningIterativeDepth_2(BaseAdversialSearch):
  def __init__(self, time_limit=0.2, depth_limit=10, depth_step=1):
    self.start_time = time.process_time()
    self.time_limit = time_limit
    self.depth_limit = depth_limit
    self.depth_step = depth_step
    self.depth = 0
    self.pruned = 0
    self.elapsed_time = 0

  def stats(self):
    return self.depth, self.pruned, round(self.elapsed_time, 8)

  def search(self, grid):
    self.alpha, self.beta = -math.inf, math.inf
    child = None
    while self.elapsed_time <= self.time_limit:
      self.depth_limit += self.depth_step
      child, utility = self.max(grid)
      self.elapsed_time = time.process_time() - self.start_time
    best_move = BaseAdversialSearch.find_best_move(grid, child)
    print(f'\ndepth limit: {self.depth_limit} best move: {best_move} pruned:{self.pruned}\nalpha: {self.alpha} beta: {self.beta}')
    return best_move

  def min(self, grid):
    if self.cutoff_test(grid):
      return (None, Utility().score(grid))

    self.depth = self.depth + 1
    min_child, min_utility = None, math.inf

    successors = BaseAdversialSearch.computer_move_successors(grid)
    for child in successors:
      _, utility = self.max(child)
      if utility < min_utility:
        min_child, min_utility = child, utility
      if min_utility <= self.alpha:
        self.pruned += 1
        return min_child, min_utility
      self.beta = min(self.beta, min_utility)
    print(f'beta:{self.beta} alpha:{self.alpha}')

    return min_child, min_utility

  def max(self, grid):
    if self.cutoff_test(grid):
      return (None, Utility().score(grid))

    self.depth = self.depth + 1
    max_child, max_utility = None, -math.inf

    successors = BaseAdversialSearch.player_move_successors(grid)
    for child in successors:
      _, utility = self.min(child)
      if utility > max_utility:
        max_child, max_utility = child, utility
      if max_utility >= self.beta:
        self.pruned += 1
        return max_child, max_utility
      self.alpha = max(self.alpha, max_utility)
    print(f'beta:{self.beta} alpha:{self.alpha}')

    return max_child, max_utility

  def cutoff_test(self, grid):
    depth_limit_reached = self.depth >= self.depth_limit
    #cells_na = len(grid.getAvailableCells()) == 0
    moves_na = len(grid.getAvailableMoves()) == 0

    return depth_limit_reached or moves_na

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
    self.monotonic = self.monotonic_grid(grid, grid.size)*0.9
    self.merges = self.potential_merges_score(grid)*0.8
    #self.smoothness = self.smoothness_score(grid, grid.size)
    self.max_tile_in_corner = self.max_value_in_the_corner(grid, grid.size)
    self.total = sum([self.available_cells, self.max_tile, self.average_value,
                     self.monotonic, self.merges, self.smoothness, self.max_tile_in_corner])
    return self.total

  @staticmethod
  def strictly_increasing(L):
    return all(x < y for x, y in zip(L, L[1:]))
  
  @staticmethod
  def strictly_decreasing(L):
    return all(x > y for x, y in zip(L, L[1:]))

  def monotonic_grid(self, grid, size):
    """
    Score is calculated from the number of monotonic rows and columns
    """
    score = 0
    for x in range(size):
      col = []
      row = []
      for y in range(size):
        row.append(grid.map[x][y])
        col.append(grid.map[y][x])
      if Utility.strictly_increasing(row) or Utility.strictly_decreasing(row):
        score += 1
      if Utility.strictly_increasing(col) or Utility.strictly_decreasing(col):
        score += 1
    return score

  def average_tile_value(self, grid, size):
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
    max_value = grid.getMaxTile()
    last = size - 1
    if grid.map[0][0] == max_value or grid.map[0][last] == max_value or grid.map[last][0] == max_value or grid.map[last][last] == max_value:
      return 2
    return 0

  def smoothness_score(self, grid, size):
    smooth = 0
    for x in range(size):
      for y in range(size):
        tile_value = grid.map[x][y]
        if (tile_value == 0):
          continue
        log_value = math.log2(tile_value)
        # compare to nearest tile up,down,left,right
        if x > 0:
          right_v = grid.map[x-1][y]
          if right_v != 0:
            smooth += abs(log_value - math.log2(right_v))
        elif x < 3:
          left_v = grid.map[x+1][y]
          if left_v != 0:
            smooth += abs(log_value - math.log2(left_v))
        elif y > 0:
          up_v = grid.map[x][y-1]
          if up_v != 0:
            smooth += abs(log_value - math.log2(up_v))
        elif y < 3:
          down_v = grid.map[x][y+1]
          if down_v != 0:
            smooth += abs(log_value - math.log2(down_v))

    return smooth

  @staticmethod
  def find_mergeable_pairs(l):
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
      #if encounters[v] % 2 == 0:
      if encounters[v] // 2 > 0:
        pairs += encounters[v] // 2
        looked_up.add(v)

    return pairs
    
  def potential_merges_score(self, grid):
    merges = 0
    columns = list(zip(*grid.map))
    for c in columns:
      merges += Utility.find_mergeable_pairs(c)
    for r in range(0, grid.size):
      merges += Utility.find_mergeable_pairs(grid.map[r])
    return merges

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
