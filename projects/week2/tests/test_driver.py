import pytest
from projects.week2.driver import *

def test_bfs_search_0():
  game = PuzzleGame([3, 1, 2, 0, 4, 5, 6, 7, 8])
  s = game.solve('bfs')

  assert isinstance(s, Solution)
  assert s.solved == True
  assert s.path_to_goal == ['Up']
  assert s.cost_of_path == 1
  assert s.nodes_expanded == 1
  assert s.search_depth == 1
  assert s.max_search_depth == 1

def test_bfs_search_1():
  game = PuzzleGame([1, 2, 5, 3, 4, 0, 6, 7, 8])
  s = game.solve('bfs')

  assert isinstance(s, Solution)
  assert s.solved == True
  assert s.path_to_goal == ['Up', 'Left', 'Left']
  assert s.cost_of_path == 3
  assert s.nodes_expanded == 10
  assert s.search_depth == 3
  assert s.max_search_depth == 4

def test_bfs_search_2():
  game = PuzzleGame([8, 6, 4, 2, 1, 3, 5, 7, 0])
  s = game.solve('bfs')

  assert isinstance(s, Solution)
  assert s.solved == True
  assert s.path_to_goal == ['Left', 'Up', 'Up', 'Left', 'Down', 'Right', 'Down', 'Left', 'Up', 'Right', 'Right',
                            'Up', 'Left', 'Left', 'Down', 'Right', 'Right', 'Up', 'Left', 'Down', 'Down', 'Right', 'Up', 'Left', 'Up', 'Left']
  assert s.cost_of_path == 26
  assert s.nodes_expanded == 166786
  assert s.search_depth == 26
  assert s.max_search_depth == 27

def test_bfs_search_3():
  game = PuzzleGame([6, 1, 8, 4, 0, 2, 7, 3, 5])
  s = game.solve('bfs')

  assert isinstance(s, Solution)
  assert s.solved == True
  assert s.path_to_goal == ['Down', 'Right', 'Up', 'Up', 'Left', 'Down', 'Right', 'Down',
                            'Left', 'Up', 'Left', 'Up', 'Right', 'Right', 'Down', 'Down', 'Left', 'Left', 'Up', 'Up']
  assert s.cost_of_path == 20
  assert s.nodes_expanded == 54094
  assert s.search_depth == 20
  assert s.max_search_depth == 21

def test_dfs_search_0():
  game = PuzzleGame([3, 1, 2, 0, 4, 5, 6, 7, 8])
  s = game.solve('dfs')

  assert isinstance(s, Solution)
  assert s.solved == True
  assert s.path_to_goal == ['Up']
  assert s.cost_of_path == 1
  assert s.nodes_expanded == 1
  assert s.search_depth == 1
  assert s.max_search_depth == 1

def test_dfs_search_1():
  game = PuzzleGame([1, 2, 5, 3, 4, 0, 6, 7, 8])
  s = game.solve('dfs')

  assert isinstance(s, Solution)
  assert s.solved == True
  assert s.path_to_goal == ['Up', 'Left', 'Left']
  assert s.cost_of_path == 3
  assert s.nodes_expanded == 181437
  assert s.search_depth == 3
  assert s.max_search_depth == 66125

def test_dfs_search_2():
  game = PuzzleGame([8, 6, 4, 2, 1, 3, 5, 7, 0])
  s = game.solve('dfs')

  assert isinstance(s, Solution)
  assert s.solved == True
  assert s.path_to_goal[0:3] == ['Up', 'Up', 'Left']
  assert s.path_to_goal[-3:] == ['Up', 'Up', 'Left']
  assert s.cost_of_path == 9612
  assert s.nodes_expanded == 9869
  assert s.search_depth == 9612
  assert s.max_search_depth == 9612

def test_dfs_search_3():
  game = PuzzleGame([6, 1, 8, 4, 0, 2, 7, 3, 5])
  s = game.solve('dfs')

  assert isinstance(s, Solution)
  assert s.solved == True
  assert s.path_to_goal[0:3] == ['Up', 'Left', 'Down']
  assert s.path_to_goal[-4:] == ['Up', 'Left', 'Up', 'Left']
  assert s.cost_of_path == 46142
  assert s.nodes_expanded == 51015
  assert s.search_depth == 46142
  assert s.max_search_depth == 46142

def test_ast_search_0():
  game = PuzzleGame([3, 1, 2, 0, 4, 5, 6, 7, 8])
  s = game.solve('ast')

  assert isinstance(s, Solution)
  assert s.solved == True
  assert s.path_to_goal == ['Up']
  assert s.cost_of_path == 1
  #assert s.nodes_expanded == 1
  assert s.search_depth == 1
  assert s.max_search_depth == 1

def test_ast_search_1():
  game = PuzzleGame([1, 2, 5, 3, 4, 0, 6, 7, 8])
  s = game.solve('ast')

  assert isinstance(s, Solution)
  assert s.solved == True
  assert s.path_to_goal == ['Up', 'Left', 'Left']
  assert s.cost_of_path == 3
  #assert s.nodes_expanded == 1
  assert s.search_depth == 3
  assert s.max_search_depth == 3


def test_ast_search_2():
  game = PuzzleGame([8, 6, 4, 2, 1, 3, 5, 7, 0])
  s = game.solve('ast')

  assert isinstance(s, Solution)
  assert s.solved == True
  assert s.path_to_goal == ['Left', 'Up', 'Up', 'Left', 'Down', 'Right', 'Down', 'Left', 'Up', 'Right', 'Right',
                            'Up', 'Left', 'Left', 'Down', 'Right', 'Right', 'Up', 'Left', 'Down', 'Down', 'Right', 'Up', 'Left', 'Up', 'Left']
  assert s.cost_of_path == 26
  #assert s.nodes_expanded == 1585
  assert s.search_depth == 26
  assert s.max_search_depth == 26


def test_ast_search_3():
  game = PuzzleGame([6, 1, 8, 4, 0, 2, 7, 3, 5])
  s = game.solve('ast')

  assert isinstance(s, Solution)
  assert s.solved == True
  assert s.path_to_goal == ['Down', 'Right', 'Up', 'Up', 'Left', 'Down', 'Right', 'Down',
                            'Left', 'Up', 'Left', 'Up', 'Right', 'Right', 'Down', 'Down', 'Left', 'Left', 'Up', 'Up']
  assert s.cost_of_path == 20
  #assert s.nodes_expanded == 696
  assert s.search_depth == 20
  assert s.max_search_depth == 20
