import heapq
import time

#  initial state from the image
start_board = [
    [2, 5, 0],
    [1, 4, 8],
    [7, 3, 6]
]

class PuzzleState:
       
    def __init__(self, board, g=0, parent=None, heuristic='h1'):
        self.board = board
        self.g = g
        self.heuristic = heuristic
        self.h1 = self.calculate_heuristic()  # heuristic cost
        self.f = self.g + self.h1
        self.parent = parent

    def __lt__(self, other): # defines how we compare two PuzzleState objects
        return self.f < other.f  # min-Heap based on f(n)
    # when two puzzle states objects are compared, they are compared based on their f values
    # this allows the heapq to prioritize states with lower f values

    def calculate_heuristic(self):
        # computes heuristic value based on the selected heuristic.
        if self.heuristic == 'h1':
            return self.misplaced_tiles()
        elif self.heuristic == 'h2':
            return self.manhattan_distance()
        return 0

    def misplaced_tiles(self):
        # heuristic h1: Count misplaced tiles (excluding blank space).
        goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        count = sum(1 for i in range(3) for j in range(3) if self.board[i][j] != goal[i][j] and self.board[i][j] != 0)
        return count

    def manhattan_distance(self):
        # Computes Manhattan distance of each tile from its goal position.
        goal_positions = {1: (0, 0), 2: (0, 1), 3: (0, 2),
                          4: (1, 0), 5: (1, 1), 6: (1, 2),
                          7: (2, 0), 8: (2, 1), 0: (2, 2)}  # Goal state
        distance = 0
        for i in range(3):
            for j in range(3):
                val = self.board[i][j]
                if val != 0:  # Ignore the blank tile
                    goal_x, goal_y = goal_positions[val]
                    distance += abs(i - goal_x) + abs(j - goal_y)
        return distance
    
    def get_neighbors(self):
        # generate next possible states by moving the blank tile.
        neighbors = []
        directions = {'Up': (-1, 0), 'Down': (1, 0), 'Left': (0, -1), 'Right': (0, 1)}
        
        # find the blank tile position
        x, y = next((i, j) 
                    for i in range(3) 
                    for j in range(3) 
                    if self.board[i][j] == 0
                    )

        for move, (dx, dy) in directions.items():
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 3 and 0 <= new_y < 3:  # valid move
                new_board = [row[:] for row in self.board]  # copy board
                new_board[x][y], new_board[new_x][new_y] = new_board[new_x][new_y], new_board[x][y]  # swap
                neighbors.append(PuzzleState(new_board, self.g + 1, self))  # add new state
        
        return neighbors

    def is_goal(self):
        # check if the current state is the goal state.
        return self.board == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def __repr__(self):
        return "\n".join([" ".join(map(str, row)) for row in self.board]) + "\n"

def a_star(start_board, heuristic='h1'):
    start_time = time.time() # start timer
    # performs A* search to solve the 8-puzzle problem
    start_state = PuzzleState(start_board, heuristic=heuristic)
    goal_state = [[1, 2, 3], 
                  [4, 5, 6], 
                  [7, 8, 0]]
    open_set = []
    heapq.heappush(open_set, start_state)
    visited = set()

    while open_set:
        current = heapq.heappop(open_set)

        if current.board == goal_state:
            elapsed_time = time.time() - start_time  # stop timing
            return reconstruct_path(current), elapsed_time  # solution found

        visited.add(str(current.board))

        for neighbor in current.get_neighbors():
            if str(neighbor.board) not in visited:
                heapq.heappush(open_set, neighbor)

    return None, None # no solution found

def reconstruct_path(state):
    # reconstructs the path from the goal state to the start state
    path = []
    while state:
        path.append(state.board)
        state = state.parent
    return path[::-1]  # Reverse the path

# solution_path = a_star(start_board)

solution_h1, time_h1 = a_star(start_board, heuristic='h1')  # Using h1 (misplaced tiles)
solution_h2, time_h2= a_star(start_board, heuristic='h2')  # Using h2 (Manhattan distance)

# Print the solution steps
print("Solution using h1 (Misplaced Tiles):")
stepsh1 = 0
for step in solution_h1:
    stepsh1 = stepsh1 + 1
    print("Step ", stepsh1)
    for row in step:
        print(row)
    print("\n")

print("Solution using h2 (Manhattan Distance):")
stepsh2 = 0
for step in solution_h2:
    stepsh2 = stepsh2 + 1 
    print("Step ", stepsh2)
    for row in step:
        print(row)
    print("\n")

print('Completed h1 in ', stepsh1, 'steps in', "{:.3f}".format(time_h1), 'seconds'  "\n")
print('Completed h2 in ', stepsh2, 'steps in' , "{:.3f}".format(time_h2), 'seconds' "\n")

