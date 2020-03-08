from projects.week4.Grid import Grid
from projects.week4.Utility import Utility
from projects.week4.Displayer import Displayer
import pytest

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

def test_average_tile_value(grid4_2, grid4_full):
  utility = Utility()
  atv = utility.average_tile_value(grid4_2, grid4_2.size)
  assert atv == 3

  atv_full = utility.average_tile_value(grid4_full, grid4_full.size)
  assert atv_full == 2

def test_find_mergeable_pairs():
  assert Utility.find_mergeable_pairs([2, 4, 2, 2])[0] == 1
  assert Utility.find_mergeable_pairs([2, 0, 2, 2])[0] == 1
  assert Utility.find_mergeable_pairs([4, 4, 4, 2])[0] == 1
  assert Utility.find_mergeable_pairs([2, 16, 16, 2])[0] == 1
  assert Utility.find_mergeable_pairs([4, 4, 2, 2])[0] == 2
  assert Utility.find_mergeable_pairs([4, 4, 4, 4])[0] == 2
  assert Utility.find_mergeable_pairs([4, 0, 0, 4])[0] == 1
  assert Utility.find_mergeable_pairs([0, 8, 0, 8])[0] == 1
  assert Utility.find_mergeable_pairs([16, 0, 16, 0])[0] == 1
  assert Utility.find_mergeable_pairs([16, 8, 4, 0])[0] == 0
  assert Utility.find_mergeable_pairs([0, 2, 4, 0])[0] == 0

def test_potential_merges_score():
  grid = grid_from_state(
      state=[[128, 32, 32,  2],
              [16, 64,  4, 16],
              [8, 16,  2,  4],
              [4,  2,  0,  2]])

  utility = Utility()
  pm, pm_score = utility.potential_merges_score(grid)
  assert pm == 2

def test_smoothness_score():
  grid = grid_from_state(
      state=[[128, 32, 32,  2],
              [16, 64,  4, 16],
              [8, 16,  2,  4],
              [4,  2,  0,  2]])
  utility = Utility()
  ss = utility.smoothness_score(grid)
  assert ss == 41

def test_score():
  grid = grid_from_state(
      state=[[128, 32, 32,  2],
              [16, 64,  4, 16],
              [8, 16,  2,  4],
              [4,  2,  0,  2]])
  moves = grid.getAvailableMoves()
  print(f'available moves: {moves}')
  print(grid.map[1])
  utility = Utility()
  utility.score(grid)
  utility.display_features()
  #assert False

def test_score_case1():
  grid = grid_from_state(
      state=[[256, 2, 8,  8],
              [64, 0,  4,  2],
              [16, 16,  2,  4],
              [4,  8,  4,  2]])

  print('LEFT:')
  left_grid = grid.clone()
  left_grid.moveLR(False)
  displayer.display(left_grid)
  utility = Utility()
  utility.score(left_grid)
  utility.display_features()

  print('RIGHT:')
  right_grid = grid.clone()
  right_grid.moveLR(True)
  displayer.display(right_grid)
  utility = Utility()
  utility.score(right_grid)
  utility.display_features()

  print('UP:')
  up_grid = grid.clone()
  up_grid.moveUD(False)
  displayer.display(up_grid)
  utility = Utility()
  utility.score(up_grid)
  utility.display_features()

  print('DOWN:')
  down_grid = grid.clone()
  down_grid.moveUD(True)
  displayer.display(down_grid)
  utility = Utility()
  utility.score(down_grid)
  utility.display_features()

  #assert False

def test_score_case2():
  grid = grid_from_state(
      state=[[8,  4,  2,  0],
              [8, 16,  8,  2],
              [16, 32, 64, 16],
              [32, 64, 128, 512]])

  utility = Utility()
  utility.score(grid)
  utility.display_features()

  print('LEFT:')
  left_grid = grid.clone()
  left_grid.moveLR(False)
  displayer.display(left_grid)
  utility = Utility()
  utility.score(left_grid)
  utility.display_features()

  print('RIGHT:')
  right_grid = grid.clone()
  right_grid.moveLR(True)
  displayer.display(right_grid)
  utility = Utility()
  utility.score(right_grid)
  utility.display_features()

  print('UP:')
  up_grid = grid.clone()
  up_grid.moveUD(False)
  displayer.display(up_grid)
  utility = Utility()
  utility.score(up_grid)
  utility.display_features()

  print('DOWN:')
  down_grid = grid.clone()
  down_grid.moveUD(True)
  displayer.display(down_grid)
  utility = Utility()
  utility.score(down_grid)
  utility.display_features()

  print(
      f'moves: {down_grid.getAvailableMoves()} moves score: {utility.insufficient_moves_variety_score(down_grid)}')

  #assert False

def test_score_case3():
  grid = grid_from_state(
      state=[[0,      2,   0,   4],
              [0,      8,  16,  16],
              [16,   128,  64,  16],
              [1024, 512, 256,  32]])

  utility = Utility()
  utility.score(grid)
  utility.display_features()

  print('LEFT:')
  left_grid = grid.clone()
  left_grid.moveLR(False)
  displayer.display(left_grid)
  utility = Utility()
  utility.score(left_grid)
  utility.display_features()

  print('RIGHT:')
  right_grid = grid.clone()
  right_grid.moveLR(True)
  displayer.display(right_grid)
  utility = Utility()
  utility.score(right_grid)
  utility.display_features()

  print('UP:')
  up_grid = grid.clone()
  up_grid.moveUD(False)
  displayer.display(up_grid)
  utility = Utility()
  utility.score(up_grid)
  utility.display_features()

  print('DOWN:')
  down_grid = grid.clone()
  down_grid.moveUD(True)
  displayer.display(down_grid)
  utility = Utility()
  utility.score(down_grid)
  utility.display_features()

  print(
      f'moves: {down_grid.getAvailableMoves()} moves score: {utility.insufficient_moves_variety_score(down_grid)}')

  #assert False
