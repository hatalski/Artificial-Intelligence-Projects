from random import randint
from BaseAI_3 import BaseAI

class PlayerAI(BaseAI):
    def getMove(self, grid):
        """
        The getMove() function, which you will need to implement, 
        returns a number that indicates the player’s action. 
        In particular, 0 stands for "Up", 1 stands for "Down", 2 stands for "Left", 
        and 3 stands for "Right".
        """
        cells = grid.getAvailableCells()

        if cells:
          result = randint(0, 3)
          print(result)
          return result
        else:
          return 0

        #return cells[randint(0, len(cells) - 1)] if cells else None

    def minimax_decision(self, state):
      child, _ = self.maximize(state)
      return child

    def minimize(self, state):
      if terminal_test(state):
        return (None, state)

      min_child, min_utility = None, math.inf

      for child in state.children():
        _, utility = self.maximize(child)
        if utility < min_utility:
          min_child, min_utility = child, utility
      
      return min_child, min_utility

    def maximize(self, state):
      if terminal_test(state):
        return (None, state)

      max_child, max_utility = None, -math.inf

      for child in state.children():
        _, utility = self.minimize(child)
        if utility > max_utility:
          max_child, max_utility = child, utility
      
      return max_child, max_utility
