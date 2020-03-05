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

class TestBaseAdversialSearch:
  def test_player_move_successors(self):
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

  # def test_terminal_test(self, grid4_2, grid4_full):
  #   assert BaseAdversialSearch.terminal_test(grid4_2) == False
  #   assert BaseAdversialSearch.terminal_test(grid4_full) == True
  #   start_time = time.process_time()
  #   assert BaseAdversialSearch.terminal_test(grid4_2, start_time, 0.2) == False
  #   while time.process_time() - start_time < 0.2:
  #     pass
  #   assert BaseAdversialSearch.terminal_test(grid4_2, start_time, 0.2) == True

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

# TESTING UTILITY CLASS

class TestUtility:
  def test_average_tile_value(self, grid4_2, grid4_full):
    utility = Utility()
    atv = utility.average_tile_value(grid4_2, grid4_2.size)
    assert atv == 3

    atv_full = utility.average_tile_value(grid4_full, grid4_full.size)
    assert atv_full == 2
    
  def test_find_mergeable_pairs(self):
    assert Utility.find_mergeable_pairs([2, 4, 2, 2]) == 1
    assert Utility.find_mergeable_pairs([2, 0, 2, 2]) == 1
    assert Utility.find_mergeable_pairs([4, 4, 4, 2]) == 1
    assert Utility.find_mergeable_pairs([2, 16, 16, 2]) == 1
    assert Utility.find_mergeable_pairs([4, 4, 2, 2]) == 2
    assert Utility.find_mergeable_pairs([4, 4, 4, 4]) == 2
    assert Utility.find_mergeable_pairs([4, 0, 0, 4]) == 1
    assert Utility.find_mergeable_pairs([0, 8, 0, 8]) == 1
    assert Utility.find_mergeable_pairs([16, 0, 16, 0]) == 1
    assert Utility.find_mergeable_pairs([16, 8, 4, 0]) == 0
    assert Utility.find_mergeable_pairs([0, 2, 4, 0]) == 0
    
  def test_potential_merges_score(self):
    grid = grid_from_state(
        state=[[128, 32, 32,  2],
               [16, 64,  4, 16],
               [8, 16,  2,  4],
               [4,  2,  0,  2]])
    
    utility = Utility()
    pm = utility.potential_merges_score(grid)
    assert pm == 2
    
  def test_smoothness_score(self):
    grid = grid_from_state(
        state=[[128, 32, 32,  2],
               [16, 64,  4, 16],
               [8, 16,  2,  4],
               [4,  2,  0,  2]])
    utility = Utility()
    ss = utility.smoothness_score(grid)
    assert ss == 41
  
  def test_score_case1(self):
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

  def test_score(self):
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
    assert False

  # utility_full = Utility(grid4_full)
  # pm_full = utility_full.potential_merges()
  # assert pm_full == 8

# def test_column_sum_more_than_others(playerAI, grid4_2, grid4_2_inv):
#   assert playerAI.column_sum_more_than_others(grid4_2) == 0
#   assert playerAI.column_sum_more_than_others(grid4_2_inv) == 1
