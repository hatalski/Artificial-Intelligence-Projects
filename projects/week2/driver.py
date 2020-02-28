from queue import Queue, LifoQueue
import heapq
from collections import deque
import time
import resource
import sys
import math

#### SKELETON CODE ####
## The Class that Represents the Puzzle
class PuzzleState(object):
    """docstring for PuzzleState"""
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        if n*n != len(config) or n < 2:
            raise Exception("the length of config is not correct!")
        self.n = n
        self.cost = cost
        self.parent = parent
        self.action = action
        self.config = config
        self.children = []

        for i, item in enumerate(self.config):
            if item == 0:
                self.blank_row = i // self.n
                self.blank_col = i % self.n
                break

    def __lt__(self, other):
        return self.config < other.config

    def display(self):
        for i in range(self.n):
            line = []
            offset = i * self.n
            for j in range(self.n):
                line.append(self.config[offset + j])
            print(line)

    def move_left(self):
        if self.blank_col == 0:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index - 1
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Left", cost=self.cost + 1)

    def move_right(self):
        if self.blank_col == self.n - 1:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index + 1
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Right", cost=self.cost + 1)

    def move_up(self):
        if self.blank_row == 0:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index - self.n
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Up", cost=self.cost + 1)

    def move_down(self):
        if self.blank_row == self.n - 1:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index + self.n
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Down", cost=self.cost + 1)

    def expand(self):
        """expand the node"""
        # add child nodes in order of UDLR
        if len(self.children) == 0:
            up_child = self.move_up()
            if up_child is not None:
                self.children.append(up_child)
            down_child = self.move_down()
            if down_child is not None:
                self.children.append(down_child)
            left_child = self.move_left()
            if left_child is not None:
                self.children.append(left_child)
            right_child = self.move_right()
            if right_child is not None:
                self.children.append(right_child)
        return self.children

class Solution:
    """
    Puzzle solution.
    """
    def __init__(self, node=None, nodes_expanded=0, max_search_depth=0, running_time=0.0, max_ram_usage=0.0):
        self.solved = False
        self.node = node
        if node is not None:
            self.path_to_goal, self.cost_of_path = Solution.calculate_total_cost(node)
            self.search_depth = node.cost
            self.solved = True
        else:
            self.path_to_goal = []
            self.cost_of_path = 0
            self.search_depth = 0
        self.nodes_expanded = nodes_expanded
        self.max_search_depth = max_search_depth
        self.running_time = running_time
        self.max_ram_usage = max_ram_usage

    @staticmethod
    def calculate_total_cost(node):
        """calculate the total estimated cost of a state"""
        path = []
        cost = 0
        #print(node.display())
        while node.parent is not None:
            cost = cost + 1
            path.append(node.action)
            node = node.parent
            #print(node.display())
        path.reverse()
        return path, cost

    def __str__(self):
        return f'path_to_goal: {self.path_to_goal}\ncost_of_path: {self.cost_of_path}\nnodes_expanded: {self.nodes_expanded}\nsearch_depth: {self.search_depth}\nmax_search_depth: {self.max_search_depth}\nrunning_time: {self.running_time}\nmax_ram_usage: {self.max_ram_usage}'

class Frontier:
    def __init__(self, queue):
        self.fringe = queue
        # self.method = method
        # if (method == 'ast'):
        #     heapq.heapify(self.fringe)
        # elif (method == 'bsf'):
        #     self.fringe = Queue(0)
        # elif (method == 'dsf'):
        #     self.fringe = LifoQueue(0)
        
        self.fringe_set = set()
        #self.expanded_set = set()

    def put(self, state):
        self.fringe.put(state)
        self.fringe_set.add(state.config)

    def put_with_cost(self, cost, state):
       heapq.heappush(self.fringe, (cost, state))
       self.fringe_set.add(state.config)

    def get(self):
        node = self.fringe.get()
        self.fringe_set.discard(node)
        return node

    def get_with_cost(self):
        node = heapq.heappop(self.fringe)
        self.fringe_set.discard(node)
        return node

    def is_in(self, state_config):
        return state_config in self.fringe_set
    
    def not_int(self, state_config):
        return state_config not in self.fringe_set

class PuzzleGame:
    def __init__(self, initial_board_state):
        """
        Initialize puzzle game given initial board state.
        Sets goal state based on initial_state dimension.
        Examples:
        if dimension is 3 then goal is (0,1,2,3,4,5,6,7,8)
        if dimension is 4 then goal is (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14)
        """
        n = int(math.sqrt(len(initial_board_state)))
        self.root_state = PuzzleState(tuple(map(int, initial_board_state)), n)
        self.goal_state = PuzzleState(tuple(map(int, range(0, n * n))), n)
        self.solvable = (PuzzleGame.get_odd_pairs(self.root_state.config) %
                         2 == 0) == (PuzzleGame.get_odd_pairs(self.goal_state.config) % 2 == 0)

    @staticmethod
    def get_odd_pairs(state):
        """
        Find and count odd pairs of numbers in the puzzle state.
        First convert state to the snake order list.
        Then remove 0 from the list.
        Then find odd pairs and count them.
        """
        l = list(state)
        row_length = len(l)
        for r in range(0, row_length):
            row = r+1
            if (row % 2 == 0):
                rev = reversed(l[row_length * (row - 1):row_length * row])
                l[row_length:row_length * row] = rev
        # remove 0 from the list
        l = list(filter(lambda n: n != 0, l))
        length = len(l)
        odd_pairs = 0
        for i in range(0, length-1):
            for n in range(i+1, length):
                if (l[i] > l[n]):
                    odd_pairs = odd_pairs + 1
        return odd_pairs

    def solve(self, search_method):
        """Returns solution to the puzzle using specified *search_method* algorithm."""
        solution = Solution()
        if self.solvable == False:
            print('Puzzle is not solvable.')
            print(
                f'Initial state {self.root_state.config} will never lead to the goal state {self.goal_state.config}')
            return solution

        start_time = time.time()

        if search_method == "bfs":
            solution = self.bfs_search()
        elif search_method == "dfs":
            solution = PuzzleGame.dfs_search(self.root_state, self.goal_state)
        elif search_method == "ast":
            solution = PuzzleGame.ast_search(self.root_state, self.goal_state)
        else:
            print("Enter a valid search method as argument!")
            return solution
        
        solution.max_ram_usage = resource.getrusage(
            resource.RUSAGE_SELF).ru_maxrss / 1024 / 1024
        solution.running_time = time.time() - start_time
        return solution

    # UNINFORMED SEARCH ALGORITHMS

    def bfs_search(self):
        """BFS (Breadth first search) algorithm."""
        # initialize frontier set (FIFO queue)
        fringe = Queue(0)
        # initialize unique set of expanded nodes
        expanded = set()
        frontier = set()
        fringe.put(self.root_state)
        frontier.add(self.root_state.config)
        max_search_depth = 0
        nodes_expanded = 0

        while fringe:
            # Step 1: remove a node from fringe set
            node = fringe.get()
            frontier.discard(node.config)
            # Step 2: check the current state against the goal state
            if (node.config == self.goal_state.config):
                return Solution(node, nodes_expanded=nodes_expanded, max_search_depth=max_search_depth)
            # Step 3: if solution has not been found then check if the current puzzle state was not expanded yet
            if (node.config not in expanded):
                children = node.expand()
                expanded.add(node.config)
                nodes_expanded = nodes_expanded + 1
                for child in children:
                    if (child.config not in expanded):
                        if (child.config not in frontier):
                            fringe.put(child)
                            frontier.add(child.config)
                            if (max_search_depth < child.cost):
                                max_search_depth = child.cost
        return Solution(nodes_expanded=nodes_expanded, max_search_depth=max_search_depth)

    @staticmethod
    def dfs_search(root_state, goal_state):
        """
        DFS (Depth first search) algorithm.
        Time difficulty: O(b**(d+1))
        Space difficulty: O(b**(d+1))
        Optimality: Yes (if cost of action is equal) 
        """
        # initialize frontier set (LIFO queue)
        fringe = LifoQueue(0)
        # initialize unique set of expanded nodes
        expanded = set()
        frontier = set()
        fringe.put(root_state)
        frontier.add(root_state.config)
        max_search_depth = 0
        nodes_expanded = 0

        while fringe:
            # Step 1: remove a node from fringe set
            node = fringe.get()
            frontier.discard(node.config)
            # Step 2: check the current state against the goal state
            if (node.config == goal_state.config):
                return Solution(node, nodes_expanded=nodes_expanded, max_search_depth=max_search_depth)
            # Step 3: if solution has not been found then check if the current puzzle state was not expanded yet
            if (node.config not in expanded):
                children = node.expand()
                children.reverse()
                expanded.add(node.config)
                nodes_expanded = nodes_expanded + 1
                for child in children:
                    if (child.config not in expanded):
                        if (child.config not in frontier):
                            fringe.put(child)
                            frontier.add(child.config)
                            if (max_search_depth < child.cost):
                                max_search_depth = child.cost
        return Solution(nodes_expanded=nodes_expanded, max_search_depth=max_search_depth)

    @staticmethod
    def dls_search(root_state, goal_state, limit):
        """DLS (Depth limited search)."""
        return Solution()

    @staticmethod
    def ids_search(root_state, goal_state):
        """IDS (Iterative deepening search)."""
        return Solution()

    @staticmethod
    def ucs_search(root_state, goal_state):
        """
        UCS (Uniform cost search).
        If the path cost is identical for every possible move, then this search is identical to BFS algorithm.
        In the case of Puzzle game path cost is always = 1, so we can basically return BFS search results.
        """
        return PuzzleGame.bfs_search(root_state, goal_state)


    # INFORMED SEARCH ALGORITHMS

    @staticmethod
    def heuristic(current_state, goal_state, dimension):
        """
        Heuristic function.
        Evaluate path cost from *current_state* to the *goal_state*.
        If *current_state* = *goal_state* the function must return 0.
        """
        result = 0
        for i, tile in enumerate(current_state):
            if tile == 0:
                continue
            else:
                result = result + PuzzleGame.calculate_manhattan_dist(i, tile, dimension)
        return result

    @staticmethod
    def calculate_manhattan_dist(idx, tile, dimension):
        """Calculate the manhattan distance of a tile."""
        node_x, node_y = int(idx // dimension), int(idx % dimension)
        goal_x, goal_y = int(tile // dimension), int(tile % dimension)
        diff_x, diff_y = abs(node_x - goal_x), abs(node_y - goal_y)
        return diff_x + diff_y

    @staticmethod
    def greedy_search(root_state, goal_state):
        """Greedy search"""
        return Solution()

    @staticmethod
    def ast_search(root_state, goal_state):
        """A * search"""
        # initialize frontier set (Priority queue)
        fringe = []
        heapq.heapify(fringe)
        # initialize unique set of expanded nodes
        dimension = root_state.n
        expanded = set()
        frontier = set()
        root_heuristic = PuzzleGame.heuristic(root_state.config, goal_state.config, dimension) + root_state.cost
        heapq.heappush(fringe, (root_heuristic, root_state))
        frontier.add(root_state.config)
        max_search_depth = 0
        nodes_expanded = 0

        while fringe:
            # Step 1: remove a node from fringe set
            priority, node = heapq.heappop(fringe)
            frontier.discard(node.config)
            # Step 2: check the current state against the goal state
            if (node.config == goal_state.config):
                return Solution(node, nodes_expanded=nodes_expanded, max_search_depth=max_search_depth)
            # Step 3: if solution has not been found then check if the current puzzle state was not expanded yet
            if (node.config not in expanded):
                children = node.expand()
                expanded.add(node.config)
                nodes_expanded = nodes_expanded + 1
                for child in children:
                    if (child.config not in expanded):
                        if (child.config not in frontier):
                            child_heuristic = PuzzleGame.heuristic(
                                child.config, goal_state.config, dimension) + child.cost
                            heapq.heappush(fringe, (child_heuristic, child))
                            frontier.add(child.config)
                            if (max_search_depth < child.cost):
                                max_search_depth = child.cost

        return Solution(nodes_expanded=nodes_expanded, max_search_depth=max_search_depth)

    @staticmethod
    def ida_search(root_state, goal_state):
        """IDA algorithm"""
        return Solution()

# Function that Writes to output.txt
### Students need to change the method to have the corresponding parameters
def write_to_file(str_to_write):
    """
    Example output:
    path_to_goal: ['Up', 'Left', 'Left']
    cost_of_path: 3
    nodes_expanded: 181437
    search_depth: 3
    max_search_depth: 66125
    running_time: 5.01608433
    max_ram_usage: 4.23940217
    """
    with open("output.txt", "w", encoding="utf-8") as file:
        file.write(str_to_write)

# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    search_method = sys.argv[1].lower()
    args_state = sys.argv[2].split(",")

    puzzle_game = PuzzleGame(args_state)
    if puzzle_game.solvable:
        solution = puzzle_game.solve(search_method)
        write_to_file(str(solution))
        if solution.solved:
            print('Puzzle is solved.')
        print(solution)
    else:
        print('Puzzle is not solvable.')
        print(f'Initial state {puzzle_game.root_state.config} will never lead to the goal state {puzzle_game.goal_state.config}')

if __name__ == '__main__':
    main()
