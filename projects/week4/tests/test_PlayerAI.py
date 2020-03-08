from projects.week4.Grid import Grid
from projects.week4.ComputerAI import ComputerAI
from projects.week4.PlayerAI import PlayerAI, algorithm_dict
from projects.week4.Utility import Utility
from projects.week4.BaseAdversialSearch import BaseAdversialSearch
from projects.week4.Displayer import Displayer
from projects.week4.Minimax import Minimax
from projects.week4.AlphaBetaPruning import AlphaBetaPruning
from projects.week4.AlphaBetaPruningIterativeDepth import AlphaBetaPruningIterativeDepth
import pytest
import time

displayer = Displayer()

def populate_grid(grid, state):
  size = grid.size
  for x in range(0, size):
    for y in range(0, size):
      grid.insertTile((x, y), state[x][y])
  return grid

def grid_from_state(state):
  grid = Grid(size=4)
  populate_grid(grid, state)
  displayer.display(grid)
  return grid

@pytest.fixture
def grid4_full():
  grid = Grid(size=4)
  cells = grid.getAvailableCells()
  for cell in cells:
    grid.insertTile(cell, 2)
  displayer.display(grid)
  return grid

@pytest.fixture
def grid4_2():
  grid = Grid(size=4)
  grid.insertTile((0, 0), 2)
  grid.insertTile((0, 1), 4)
  displayer.display(grid)
  return grid

@pytest.fixture
def grid4_2_inv():
  grid = Grid(size=4)
  grid.insertTile((0, 0), 4)
  grid.insertTile((0, 1), 2)
  displayer.display(grid)
  return grid

@pytest.fixture
def grid4_2_right():
  grid = Grid(size=4)
  grid.insertTile((0, 2), 2)
  grid.insertTile((0, 3), 4)
  displayer.display(grid)
  return grid

@pytest.fixture
def grid4_2_down():
  grid = Grid(size=4)
  grid.insertTile((3, 0), 2)
  grid.insertTile((3, 1), 4)
  displayer.display(grid)
  return grid

class TestPlayerAI:
  def test_player_move_minimax(self, grid4_2):
    ai = PlayerAI(algorithm=algorithm_dict[0])
    move = ai.getMove(grid4_2)
    print(f'move: {move}')
    assert isinstance(move, int)
    # down (1) and right (3) are the only possible moves in this grid state
    assert move == 3 or move == 1
    spent_time_on_move = ai.move_stats[-1][2]
    print(f'spent_time_on_move: {spent_time_on_move}')
    assert spent_time_on_move < 0.25 # 0.2s timeLimit + 0.05s allowance
    # assert False

  def test_player_move_alpha_beta_pruning(self, grid4_2):
    ai = PlayerAI()
    move = ai.getMove(grid4_2)
    print(f'move: {move}')
    assert isinstance(move, int)
    # down (1) and right (3) are the only possible moves in this grid state
    assert move == 3 or move == 1
    spent_time_on_move = ai.move_stats[-1][2]
    print(f'spent_time_on_move: {spent_time_on_move}')
    assert spent_time_on_move < 0.25  # 0.2s timeLimit + 0.05s allowance
    # assert False
    
  def test_player_move_alpha_beta_pruning(self):
    ai = PlayerAI()
    grid = grid_from_state(
        state=[[256, 2, 8,  8],
               [64, 0,  4,  2],
               [16, 16,  2,  4],
               [4,  8,  4,  2]])
    move = ai.getMove(grid)
    print(f'move: {move}')
    assert isinstance(move, int)
    # down (1) and right (3) are the only possible moves in this grid state
    assert move == 2
    #spent_time_on_move = ai.move_stats[-1][2]
    #print(f'spent_time_on_move: {spent_time_on_move}')
    #assert spent_time_on_move < 0.25  # 0.2s timeLimit + 0.05s allowance
    #assert False