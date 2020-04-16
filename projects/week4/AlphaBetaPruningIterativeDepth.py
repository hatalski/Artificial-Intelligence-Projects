from projects.week4.BaseAdversialSearch import BaseAdversialSearch
from projects.week4.Utility import Utility
import math
import time

class AlphaBetaPruningIterativeDepth(BaseAdversialSearch):
  def __init__(self, time_limit=0.2, depth_limit=10, depth_step=4):
    self.start_time = time.process_time()
    self.time_limit = time_limit
    self.depth_limit = depth_limit
    self.depth_step = depth_step
    self.depth = 0
    self.pruned = 0
    self.elapsed_time = 0
    self.utility = 0

  def stats(self):
    return (self.depth, self.pruned, round(self.elapsed_time, 8))

  def search(self, grid):
    alpha, beta = -math.inf, math.inf
    child = None
    while self.elapsed_time <= self.time_limit:
      self.depth_limit += self.depth_step
      child, self.utility = self.max(grid, alpha, beta)
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
    moves_na = len(grid.getAvailableMoves()) == 0
    return depth_limit_reached or moves_na
