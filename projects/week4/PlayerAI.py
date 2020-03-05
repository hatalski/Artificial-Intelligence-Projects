from projects.week4.BaseAI import BaseAI
from projects.week4.Minimax import Minimax
from projects.week4.AlphaBetaPruning import AlphaBetaPruning
from projects.week4.AlphaBetaPruningIterativeDepth import AlphaBetaPruningIterativeDepth
from projects.week4.BaseAdversialSearch import BaseAdversialSearch

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
