from random import randint
from BaseAI_3 import BaseAI
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
        cells = grid.getAvailableCells()
        self.move_start_time = time.clock()

        if cells:
          # result = randint(0, 3)
          result = self.minimax_decision(grid)
          print(result)
          return result
        else:
          return 0

        #return cells[randint(0, len(cells) - 1)] if cells else None

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
      for cell_pos in cells:
        successor_2 = grid_state.clone()
        if successor_2.canInsert(cell_pos):
          successor_2.setCellValue(cell_pos, 2)
        successor_4 = grid_state.clone()
        if successor_4.canInsert(cell_pos):
          successor_4.setCellValue(cell_pos, 4)
      return successors

    def utility(self, grid_state):
      """
      Returns utility value of a grid state
      """
      return len(grid_state.getAvailableCells())

    def terminal_test(self, grid_state):
      """
      Returns True if: time for player's turn exceeds or equal to timeLimit
      and free cells are available
      and moves are available
      """
      cells_available = len(grid_state.getAvailableCells()) > 0
      moves_available = len(grid_state.getAvailableMoves()) > 0
      time_available = self.move_start_time - time.clock() >= 0.2
      return cells_available and moves_available and time_available
