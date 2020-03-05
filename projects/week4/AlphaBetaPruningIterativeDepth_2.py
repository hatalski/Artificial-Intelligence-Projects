from projects.week4.BaseAdversialSearch import BaseAdversialSearch
from projects.week4.Utility import Utility
import math
import time

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
    print(
        f'\ndepth limit: {self.depth_limit} best move: {best_move} pruned:{self.pruned}\nalpha: {self.alpha} beta: {self.beta}')
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
    moves_na = len(grid.getAvailableMoves()) == 0
    return depth_limit_reached or moves_na
