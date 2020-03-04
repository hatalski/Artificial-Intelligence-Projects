from projects.week4.Grid import Grid
from projects.week4.ComputerAI import ComputerAI
from projects.week4.PlayerAI import PlayerAI, algorithm_dict, Utility, BaseAdversialSearch, Minimax, AlphaBetaPruning
from projects.week4.Displayer import Displayer
import pytest
import time

displayer = Displayer()

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

class TestBaseAdversialSearch:
  def test_player_move_successors(self, grid4_2):
    successors = BaseAdversialSearch.player_move_successors(grid4_2)
    for s in successors:
      print(displayer.display(s))
    assert len(successors) == 2

  def test_computer_move_successors(self, grid4_2):
    successors = BaseAdversialSearch.computer_move_successors(grid4_2)
    for s in successors:
      print(displayer.display(s))
    assert len(successors) == len(grid4_2.getAvailableCells() * 2)

  def test_compare_grids(self, grid4_2, grid4_2_right):
    assert BaseAdversialSearch.compare_grids(grid4_2, grid4_2) == True
    assert BaseAdversialSearch.compare_grids(grid4_2, grid4_2_right) == False
    assert BaseAdversialSearch.compare_grids(grid4_2, None) == False
    assert BaseAdversialSearch.compare_grids(None, grid4_2_right) == False

  def test_find_best_move_right(self, grid4_2, grid4_2_right, grid4_2_down):
    move_right = BaseAdversialSearch.find_best_move(grid4_2, grid4_2_right)
    assert move_right == 3  # 3 - right move
    move_down = BaseAdversialSearch.find_best_move(grid4_2, grid4_2_down)
    assert move_down == 1  # 1 - down move

  def test_terminal_test(self, grid4_2, grid4_full):
    assert BaseAdversialSearch.terminal_test(grid4_2) == False
    assert BaseAdversialSearch.terminal_test(grid4_full) == True
    start_time = time.process_time()
    assert BaseAdversialSearch.terminal_test(grid4_2, start_time, 0.2) == False
    while time.process_time() - start_time < 0.2:
      pass
    assert BaseAdversialSearch.terminal_test(grid4_2, start_time, 0.2) == True

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

# TESTING UTILITY CLASS

class TestUtility:
  def test_potential_merges(self, grid4_2, grid4_full):
    utility = Utility()
    pm = utility.potential_merges(grid4_2, grid4_2.size)
    assert pm == 0

    pm_full = utility.potential_merges(grid4_full, grid4_full.size)
    assert pm_full == 8

  def test_average_tile_value(self, grid4_2, grid4_full):
    utility = Utility()
    atv = utility.average_tile_value(grid4_2, grid4_2.size)
    assert atv == 3

    atv_full = utility.average_tile_value(grid4_full, grid4_full.size)
    assert atv_full == 2

  # utility_full = Utility(grid4_full)
  # pm_full = utility_full.potential_merges()
  # assert pm_full == 8

# def test_column_sum_more_than_others(playerAI, grid4_2, grid4_2_inv):
#   assert playerAI.column_sum_more_than_others(grid4_2) == 0
#   assert playerAI.column_sum_more_than_others(grid4_2_inv) == 1
