from queue import Queue, LifoQueue
import heapq
from collections import deque
import time
import resource
import sys
import math

import itertools

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
        return self.config < other.config #and self.cost < other.cost

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

    def heuristic_and_cost(self):
        """Cost for A* algorithm. f(n) = g(n) + h(n)"""
        return self.cost + self.heuristic()

    def heuristic(self, goal_state=(0,1,2,3,4,5,6,7,8)):
        """
        Heuristic function.
        Evaluate path cost from *current_state* to the *goal_state*.
        If *current_state* = *goal_state* the function must return 0.

        Note: goal_state is not yet implemented, the default (0,1,2,3,4,5,6,7,8) is implied
        """
        result = 0
        for i, tile in enumerate(self.config):
            if tile == 0:
                continue
            else:
                result = result + PuzzleState.calculate_manhattan_dist(i, tile, self.n)
        return result

    @staticmethod
    def calculate_manhattan_dist(index, tile, dimension):
        """Calculate the manhattan distance of a tile."""
        node_x, node_y = int(index // dimension), int(index % dimension)
        goal_x, goal_y = int(tile // dimension), int(tile % dimension)
        return abs(node_x - goal_x) + abs(node_y - goal_y)

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

class PriorityFrontier:
    """
    Information on how to change priority of the item in the priority queue: https://docs.python.org/3/library/heapq.html#module-heapq
    """

    REMOVED = 'R'

    def __init__(self, queue):
        self.fringe = queue

        self.expanded_set = set()
        self.expanded_total = 0

        # for priority queue
        self.entry_finder = {}
        self.counter = itertools.count()

    def add_or_update_state(self, cost, state):
        """
        Add a new state or update the priority of an existing state
        """
        if state.config in self.entry_finder:
            self.remove_state(state.config)
        count = next(self.counter)
        entry = [cost, count, state]
        self.entry_finder[state.config] = entry
        heapq.heappush(self.fringe, entry)

    def remove_state(self, state_config):
        """
        Mark an existing state as REMOVED.
        """
        entry = self.entry_finder.pop(state_config)
        entry[-1] = PriorityFrontier.REMOVED

    def pop_state(self):
        """
        Remove and return the lowest priority state.
        """
        while self.fringe:
            cost, count, state = heapq.heappop(self.fringe)
            if state is not PriorityFrontier.REMOVED:
                del self.entry_finder[state.config]
                return state

    def add_to_expanded(self, state_config):
        self.expanded_set.add(state_config)
        self.expanded_total = self.expanded_total + 1

    def not_in_expanded(self, state_config):
        return state_config not in self.expanded_set

    def not_in_frontier(self, state_config):
        return state_config not in self.entry_finder

class Frontier:
    def __init__(self, queue):
        self.fringe = queue
        self.fringe_set = set()

        self.expanded_set = set()
        self.expanded_total = 0

    def add_to_expanded(self, state_config):
        self.expanded_set.add(state_config)
        self.expanded_total = self.expanded_total + 1

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

    def is_in_fringe(self, state_config):
        return state_config in self.fringe_set
    
    def not_in_fringe(self, state_config):
        return state_config not in self.fringe_set

    def not_in_expanded(self, state_config):
        return state_config not in self.expanded_set

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
        self.solvable = (PuzzleGame.__odd_pairs(self.root_state.config) %
                         2 == 0) == (PuzzleGame.__odd_pairs(self.goal_state.config) % 2 == 0)

        print(f'Started solving puzzle: {self.root_state.config} with the goal: {self.goal_state.config}')

    @staticmethod
    def __odd_pairs(state):
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
            solution = self.__uninformed_search(Queue(0))
        elif search_method == "dfs":
            solution = self.__uninformed_search(LifoQueue(0), reversed_children=True)
        elif search_method == "ast":
            heap = []
            heapq.heapify(heap)
            solution = self.__ast_search(heap)
        elif search_method == "greedy":
            heap = []
            heapq.heapify(heap)
            solution = self.__greedy_search(heap)
        else:
            print("Enter a valid search method as argument!")
            return solution
        
        solution.max_ram_usage = resource.getrusage(
            resource.RUSAGE_SELF).ru_maxrss / 1024 / 1024
        solution.running_time = time.time() - start_time
        return solution

    # UNINFORMED SEARCH ALGORITHMS

    def __uninformed_search(self, queue, reversed_children=False):
        """
        Generic uninformed search algorithm that can accomodate both BFS (Breadth first search) and DFS (Deepest first search) algorithms.
        
        For BFS use Queue(0) as a queue.
        
        For DFS use LifoQueue(0) as a queue and set reversed_children=True

        DFS (Depth first search) algorithm:
        Time difficulty: O(b**(d+1))
        Space difficulty: O(b**(d+1))
        Optimality: Yes (if cost of action is equal) 
        """
        goal_state_config = self.goal_state.config
        # initialize frontier (FIFO queue and expanded set)
        f = Frontier(queue)
        f.put(self.root_state)
        max_search_depth = 0

        while f.fringe:
            # Step 1: remove a node from fringe set
            node = f.get()
            # Step 2: check the current state against the goal state
            if (node.config == goal_state_config):
                return Solution(node, nodes_expanded=f.expanded_total, max_search_depth=max_search_depth)
            # Step 3: if solution has not been found then check if the current puzzle state was not expanded yet
            if f.not_in_expanded(node.config):
                children = node.expand()
                if reversed_children:
                    children.reverse()
                f.add_to_expanded(node.config)
                for child in children:
                    if f.not_in_expanded(child.config):
                        if f.not_in_fringe(child.config):
                            f.put(child)
                            if (max_search_depth < child.cost):
                                max_search_depth = child.cost
        return Solution(nodes_expanded=f.expanded_total, max_search_depth=max_search_depth)

    def __dls_search(self, limit):
        """DLS (Depth limited search)."""
        return Solution()

    def __ids_search(self):
        """IDS (Iterative deepening search)."""
        return Solution()

    def __ucs_search(self):
        """
        UCS (Uniform cost search).
        If the path cost is identical for every possible move, then this search is identical to BFS algorithm.
        In the case of Puzzle game path cost is always = 1, so we can basically return BFS search results.
        """
        return self.bfs_search()

    # INFORMED SEARCH ALGORITHMS

    def __greedy_search(self, heap):
        """
        Greedy search
        
        Main difference to A* is calculation of heuristic anticipated cost excluding path cost to the current state (from root).
        """
        goal_state_config = self.goal_state.config
        # initialize frontier (Priority queue)
        f = Frontier(heap)
        f.put_with_cost(self.root_state.heuristic(), self.root_state)
        max_search_depth = 0

        while f.fringe:
            # Step 1: remove a node from fringe set
            priority, node = f.get_with_cost()
            # Step 2: check the current state against the goal state
            if (node.config == goal_state_config):
                return Solution(node, nodes_expanded=f.expanded_total, max_search_depth=max_search_depth)
            # Step 3: if solution has not been found then check if the current puzzle state was not expanded yet
            if f.not_in_expanded(node.config):
                children = node.expand()
                f.add_to_expanded(node.config)
                for child in children:
                    if f.not_in_expanded(child.config):
                        if f.not_in_fringe(child.config):
                            f.put_with_cost(child.heuristic(), child)
                            if (max_search_depth < child.cost):
                                max_search_depth = child.cost

        return Solution(nodes_expanded=f.expanded_total, max_search_depth=max_search_depth)

    def __ast_search(self, heap):
        """A * search"""
        goal_state_config = self.goal_state.config
        # initialize frontier (Priority queue)
        pf = PriorityFrontier(heap)
        pf.add_or_update_state(self.root_state.heuristic_and_cost(), self.root_state)
        max_search_depth = 0
        counter = itertools.count()

        while pf.fringe:
            trials_count = next(counter)
            # Step 1: remove a node from fringe set
            node = pf.pop_state()
            if (trials_count % 10000 == 0):
                print(
                    f'trials: {trials_count} ; distance: {node.heuristic()} ; node: {node.config}')
            # Step 2: check the current state against the goal state
            if (node.config == goal_state_config):
                return Solution(node, nodes_expanded=pf.expanded_total, max_search_depth=max_search_depth)
            # Step 3: if solution has not been found then check if the current puzzle state was not expanded yet
            if pf.not_in_expanded(node.config):
                children = node.expand()
                pf.add_to_expanded(node.config)
                for child in children:
                    if pf.not_in_expanded(child.config) and pf.not_in_frontier(child.config):
                        pf.add_or_update_state(child.heuristic_and_cost(), child)
                        if (max_search_depth < child.cost):
                            max_search_depth = child.cost

        return Solution(nodes_expanded=pf.expanded_total, max_search_depth=max_search_depth)

    def _ida_search(self):
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
