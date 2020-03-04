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
      alg = Minimax(time_limit=0.07)
    elif self.algorithm == algorithm_dict[1]:
      alg = AlphaBetaPruning(time_limit=0.07)
    best_move = alg.search(grid)
    self.move_stats.append(alg.stats())

    if best_move is None:
      print(f'\nMove stats: {self.move_stats}')
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

    return max_child, max_utility

class AlphaBetaPruningIterativeDepth(BaseAdversialSearch):
  def __init__(self, time_limit=0.2, depth_limit=10):
    self.start_time = time.process_time()
    self.time_limit = time_limit
    self.depth_limit = depth_limit
    self.depth = 0
    self.pruned = 0
    self.elapsed_time = 0

  def stats(self):
    return self.depth, self.pruned, round(self.elapsed_time, 8)

  def search(self, grid):
    alpha, beta = -math.inf, math.inf
    child = None
    while self.elapsed_time <= self.time_limit:
      self.depth_limit += 5
      child, utility = self.max(grid, alpha, beta)
      self.elapsed_time = time.process_time() - self.start_time
    print(f'\ndepth_limit: {self.depth_limit}')
    best_move = BaseAdversialSearch.find_best_move(grid, child)
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
        return min_child, min_utility
      beta = min(beta, min_utility)

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
        return max_child, max_utility
      alpha = max(alpha, max_utility)

    return max_child, max_utility

  def cutoff_test(self, grid):
    depth_limit_reached = self.depth >= self.depth_limit
    #cells_na = len(grid.getAvailableCells()) == 0
    moves_na = len(grid.getAvailableMoves()) == 0

    return depth_limit_reached or moves_na

class Utility:
  def __init__(self):
    self.criteria = []

  def score(self, grid):
    self.criteria.append(len(grid.getAvailableCells())*0.4)
    #self.criteria.append(math.log2(grid.getMaxTile()))
    #self.criteria.append(self.column_sum_more_than_others(grid, grid.size))
    #self.criteria.append(self.average_tile_value(grid, grid.size))
    self.criteria.append(self.monotonic_grid(grid, grid.size)*0.2)
    self.criteria.append(self.potential_merges(grid, grid.size)*0.3)
    self.criteria.append(self.max_value_in_the_corner(grid, grid.size)*0.1)
    return sum(self.criteria)

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
    return math.log2(statistics.mean(values))

  def max_value_in_the_corner(self, grid, size):
    max_value = grid.getMaxTile()
    last = size - 1
    if grid.map[0][0] == max_value or grid.map[0][last] == max_value or grid.map[last][0] == max_value or grid.map[last][last] == max_value:
      return 10
    return 0

  def potential_merges(self, grid, size):
    count = 0
    for x in range(size):
      for y in range(size):
        tile_value = grid.map[x][y]
        if (tile_value == 0):
          continue
        #multiplier = math.log2(tile_value)
        # compare to nearest tile up,down,left,right
        if x > 0 and tile_value == grid.map[x-1][y]:
          count += 1
        elif x < 3 and tile_value == grid.map[x+1][y]:
          count += 1
        elif y > 0 and tile_value == grid.map[x][y-1]:
          count += 1
        elif y < 3 and tile_value == grid.map[x][y+1]:
          count += 1
    return count // 2

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
