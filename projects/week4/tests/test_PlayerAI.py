from projects.week4.Grid import Grid
from projects.week4.ComputerAI import ComputerAI
from projects.week4.PlayerAI import PlayerAI
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

@pytest.fixture
def playerAI():
  return PlayerAI()

def test_player_move_successors(playerAI, grid4_2):
  successors = playerAI.player_move_successors(grid4_2)
  for s in successors:
    print(displayer.display(s))
  assert len(successors) == 2

def test_computer_move_successors(playerAI, grid4_2):
  computerAI = ComputerAI()
  successors = playerAI.computer_move_successors(grid4_2)
  for s in successors:
    print(displayer.display(s))
  assert len(successors) == len(grid4_2.getAvailableCells() * 2)

def test_compare_grids(playerAI, grid4_2, grid4_2_right):
  assert playerAI.compare_grids(grid4_2, grid4_2) == True
  assert playerAI.compare_grids(grid4_2, grid4_2_right) == False
  assert playerAI.compare_grids(grid4_2, None) == False
  assert playerAI.compare_grids(None, grid4_2_right) == False

def test_find_child_move_right(playerAI, grid4_2, grid4_2_right):
  move = playerAI.find_child_move(grid4_2, grid4_2_right)
  assert move == 3 # 3 - right move

def test_find_child_move_down(playerAI, grid4_2, grid4_2_down):
  move = playerAI.find_child_move(grid4_2, grid4_2_down)
  assert move == 1  # 1 - down move

def test_terminal_test(playerAI, grid4_2, grid4_full):
  assert playerAI.terminal_test(grid4_2) == False
  assert playerAI.terminal_test(grid4_full) == True
  playerAI.move_start_time = time.process_time()
  assert hasattr(playerAI, 'move_start_time')
  assert playerAI.terminal_test(grid4_2) == False
  while time.process_time() - playerAI.move_start_time < 0.2:
    pass
  assert playerAI.terminal_test(grid4_2) == True

def test_player_move(playerAI, grid4_2):
  playerAI.move_start_time = time.process_time()
  move = playerAI.getMove(grid4_2)
  print(f'move: {move}')
  assert isinstance(move, int)
  # down (1) and right (3) are the only possible moves in this grid state
  assert move == 3 or move == 1
  spent_time_on_move = time.process_time() - playerAI.move_start_time
  print(f'spent_time_on_move: {spent_time_on_move}')
  assert spent_time_on_move < 0.25 # 0.2s timeLimit + 0.05s allowance
  # assert False
