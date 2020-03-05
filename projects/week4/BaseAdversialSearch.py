class BaseAdversialSearch:
  def search(self, grid):
    pass

  def min(self, grid):
    pass

  def max(self, grid):
    pass

  def stats(self):
    pass

  @staticmethod
  def player_move_successors(grid):
    """
    Returns grid successors of all possible Player moves
    """
    successors = []
    moves = grid.getAvailableMoves()
    for move in moves:
      successor = grid.clone()
      if successor.move(move):
        successors.append(successor)
    return successors

  @staticmethod
  def computer_move_successors(grid):
    """
    Returns grid successors of all possible Computer moves
    """
    successors = []
    cells = grid.getAvailableCells()
    for cell_pos in cells:
      successor_2 = grid.clone()
      if successor_2.canInsert(cell_pos):
        successor_2.setCellValue(cell_pos, 2)
        successors.append(successor_2)
      successor_4 = grid.clone()
      if successor_4.canInsert(cell_pos):
        successor_4.setCellValue(cell_pos, 4)
        successors.append(successor_4)
    return successors

  @staticmethod
  def find_best_move(grid, child):
    moves = grid.getAvailableMoves()
    for move in moves:
        successor = grid.clone()
        if successor.move(move):
          if BaseAdversialSearch.compare_grids(successor, child):
            return move
    return None

  @staticmethod
  def compare_grids(grid1, grid2):
    if grid1 is None or grid2 is None:
      return False
    if grid1.size == grid2.size:
      size = grid1.size
      for x in range(size):
        for y in range(size):
          if grid1.map[x][y] != grid2.map[x][y]:
            return False
      return True
    else:
      return False
