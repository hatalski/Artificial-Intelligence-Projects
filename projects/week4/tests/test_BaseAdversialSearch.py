from projects.week4.Grid import Grid
from projects.week4.Utility import Utility
from projects.week4.BaseAdversialSearch import BaseAdversialSearch
import pytest
from projects.week4.Displayer import Displayer

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
def grid4_2():
  grid = Grid(size=4)
  grid.insertTile((0, 0), 2)
  grid.insertTile((0, 1), 4)
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

def test_player_move_successors():
  grid = grid_from_state(
      state=[[256, 2, 8,  8],
              [64, 0,  4,  2],
              [16, 16,  2,  4],
              [4,  8,  4,  2]])
  successors = BaseAdversialSearch.player_move_successors(grid)
  for s in successors:
    print(displayer.display(s))
  assert len(successors) == 4
  #assert False

def test_computer_move_successors(grid4_2):
  successors = BaseAdversialSearch.computer_move_successors(grid4_2)
  for s in successors:
    print(displayer.display(s))
  assert len(successors) == len(grid4_2.getAvailableCells() * 2)

def test_compare_grids(grid4_2, grid4_2_right):
  assert BaseAdversialSearch.compare_grids(grid4_2, grid4_2) == True
  assert BaseAdversialSearch.compare_grids(grid4_2, grid4_2_right) == False
  assert BaseAdversialSearch.compare_grids(grid4_2, None) == False
  assert BaseAdversialSearch.compare_grids(None, grid4_2_right) == False

def test_find_best_move_right(grid4_2, grid4_2_right, grid4_2_down):
  move_right = BaseAdversialSearch.find_best_move(grid4_2, grid4_2_right)
  assert move_right == 3  # 3 - right move
  move_down = BaseAdversialSearch.find_best_move(grid4_2, grid4_2_down)
  assert move_down == 1  # 1 - down move
