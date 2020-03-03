from projects.week4.BaseAI import BaseAI
import time
import math

class PlayerAI(BaseAI):
  def getMove(self, grid):
    """
    The getMove() function, which you will need to implement, 
    returns a number that indicates the player’s action. 
    In particular, 0 stands for "Up", 1 stands for "Down", 2 stands for "Left", 
    and 3 stands for "Right".
    """
    moves = grid.getAvailableMoves()
    self.move_start_time = time.process_time()

    if moves:
      best_successor = self.minimax_decision(grid)
      best_move = self.find_child_move(grid, best_successor)
      return best_move
    else:
      return None

  def find_child_move(self, grid_state, child):
    moves = grid_state.getAvailableMoves()
    for move in moves:
        successor = grid_state.clone()
        if successor.move(move):
          if self.compare_grids(successor, child):
            return move
    return None

  def compare_grids(self, grid1, grid2):
    if grid1.size == grid2.size:
      size = grid1.size
      for x in range(size):
        for y in range(size):
          if grid1.map[x][y] != grid2.map[x][y]:
            return False
      return True
    else:
      return False

  def minimax_decision(self, grid_state):
    child, utility = self.maximize(grid_state)
    print(f'minimax returns: {child} with utility: {utility}')
    return child

  def minimize(self, grid_state):
    """
    Action to minimize value is different since Computer places a tile randomly 
    on the grid. However, we should consider that computer's tile placement 
    is not random, but intentional with a goal to minimize player's value.
    """
    if self.terminal_test(grid_state):
      return (None, self.utility(grid_state))

    min_child, min_utility = None, math.inf

    for child in self.computer_move_successors(grid_state):
      _, utility = self.maximize(child)
      if utility < min_utility:
        min_child, min_utility = child, utility
    
    return min_child, min_utility

  def maximize(self, grid_state):
    if self.terminal_test(grid_state):
      return (None, self.utility(grid_state))

    max_child, max_utility = None, -math.inf

    for child in self.player_move_successors(grid_state):
      _, utility = self.minimize(child)
      if utility > max_utility:
        max_child, max_utility = child, utility
    
    return max_child, max_utility

  def player_move_successors(self, grid_state):
    """
    Returns successors of all possible Player moves
    """
    successors = []
    moves = grid_state.getAvailableMoves()
    for move in moves:
      successor = grid_state.clone()
      if successor.move(move):
        successors.append(successor)
    return successors

  def computer_move_successors(self, grid_state):
    """
    Returns successors of all possible Computer moves
    """
    successors = []
    cells = grid_state.getAvailableCells()
    print(f'cells: {cells}')
    for cell_pos in cells:
      successor_2 = grid_state.clone()
      if successor_2.canInsert(cell_pos):
        successor_2.setCellValue(cell_pos, 2)
        successors.append(successor_2)
      successor_4 = grid_state.clone()
      if successor_4.canInsert(cell_pos):
        successor_4.setCellValue(cell_pos, 4)
        successors.append(successor_4)
    return successors

  def utility(self, grid_state):
    """
    Returns utility value of a grid state
    Use count of free cells, maximum value of tile, 
    """
    return len(grid_state.getAvailableCells())

  def terminal_test(self, grid_state):
    """
    Returns True if: 
    time for player's turn exceeds or equal to timeLimit
    or free cells are not available
    or moves are not available
    """
    time_not_available = False
    cells_not_available = len(grid_state.getAvailableCells()) == 0
    moves_not_available = len(grid_state.getAvailableMoves()) == 0
    if hasattr(self, 'move_start_time'):
      print(self.move_start_time)
      current = time.process_time()
      diff = current - self.move_start_time
      print(f'current: {current} ; diff: {diff}')
      time_not_available = diff >= 0.2

    return cells_not_available or moves_not_available or time_not_available
