import time


# initialState = [2, 5, 1, 4, 8, 7, 3, 6]
# goalState = [1, 2, 3, 4, 5, 6, 7, 8, 0]

# actions = ['up', 'down', 'left', 'right']

# # j = bredd, i = höjd
# #      j
# #   X  X  X
# # i X  X  X
# #   X  X  X

# if actions == 'up' and i > 1:
#     # flytta upp
#     pass
# elif actions == 'down' and i < 3:
#     # flytta ner
#     pass
# elif actions == 'left' and j > 1:
#     # flytta vänster
#     pass
# elif actions == 'right' and j < 3:
#     # flytta höger
#     pass
# else:
#     print("Invalid move")



#     [0,0,0,0,0,0,0]

#     [x,x,x,x,1,1,0]


import heapq

class PuzzleState:
    def __init__(self, board, g, parent=None):
        self.board = board
        self.g = g
        self.h1 = self.misplaced_tiles()
        self.f = self.g + self.h1
        self.parent = parent

    def __lt__(self, other):
        return self.f < other.f  # Min-Heap based on f(n)

    def misplaced_tiles(self):
        #Heuristic h1: Count misplaced tiles (excluding blank space).
        goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        count = sum(1 for i in range(3) for j in range(3) if self.board[i][j] != goal[i][j] and self.board[i][j] != 0)
        return count

    def get_neighbors(self):
        # Generate next possible states by moving the blank tile.
        neighbors = []
        directions = {'Up': (-1, 0), 'Down': (1, 0), 'Left': (0, -1), 'Right': (0, 1)}
        
        # Find the blank tile position
        x, y = next((i, j) for i in range(3) for j in range(3) if self.board[i][j] == 0)

        for move, (dx, dy) in directions.items():
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 3 and 0 <= new_y < 3:  # Valid move
                new_board = [row[:] for row in self.board]  # Copy board
                new_board[x][y], new_board[new_x][new_y] = new_board[new_x][new_y], new_board[x][y]  # Swap
                neighbors.append(PuzzleState(new_board, self.g + 1, self))  # Add new state
        
        return neighbors

    def is_goal(self):
        #Check if the current state is the goal state.
        return self.board == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def __repr__(self):
        return "\n".join([" ".join(map(str, row)) for row in self.board]) + "\n"

def a_star(start_board):
    start_state = PuzzleState(start_board, 0)
    open_list = []
    heapq.heappush(open_list, start_state)
    visited = set()

    while open_list:
        current = heapq.heappop(open_list)

        if current.is_goal():
            path = []
            while current:
                path.append(current)
                current = current.parent
            return path[::-1]  # Reverse the path

        visited.add(str(current.board))  # Store state as string for hashing

        for neighbor in current.get_neighbors():
            if str(neighbor.board) not in visited:
                heapq.heappush(open_list, neighbor)

    return None  # No solution found

# Initial state from the image
start_board = [
    [2, 5, 0],
    [1, 4, 8],
    [7, 3, 6]
]

solution_path = a_star(start_board)

# Print the solution steps
if solution_path:
    for step, state in enumerate(solution_path):
        print(f"Step {step}:\n{state}")
else:
    print("No solution found.")
