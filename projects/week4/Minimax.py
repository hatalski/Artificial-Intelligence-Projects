from projects.week4.BaseAdversialSearch import BaseAdversialSearch
from projects.week4.Utility import Utility
import math
import time

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
    if self.terminal_test(grid):
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
    if self.terminal_test(grid):
      return (None, Utility().score(grid))

    self.depth = self.depth + 1
    max_child, max_utility = None, -math.inf

    successors = BaseAdversialSearch.player_move_successors(grid)
    for child in successors:
      _, utility = self.min(child)
      if utility > max_utility:
        max_child, max_utility = child, utility

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
