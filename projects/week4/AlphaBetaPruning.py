from projects.week4.BaseAdversialSearch import BaseAdversialSearch
from projects.week4.Utility import Utility
import math
import time

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
    if self.terminal_test(grid):
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
    if self.terminal_test(grid):
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

  def terminal_test(self, grid):
    """
    Returns True if: 
    time for player's turn exceeds or equal to timeLimit
    or free cells are not available
    or moves are not available
    """
    time_na = False
    moves_na = len(grid.getAvailableMoves()) == 0
    if self.start_time is not None:
      current = time.process_time()
      diff = current - self.start_time
      time_na = diff >= self.time_limit

    return moves_na or time_na
