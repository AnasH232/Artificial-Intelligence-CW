from collections import deque
from queue import PriorityQueue

# Maze grid (1 = open path, 0 = wall)
maze = [
    [1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
    [0, 1, 0, 1, 0, 1, 1, 0, 1, 0],
    [1, 1, 1, 1, 0, 1, 0, 1, 1, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 1, 0, 0, 1, 0, 1, 0, 1, 1],
    [0, 1, 1, 0, 1, 1, 1, 0, 1, 0],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1]
]

# Start and goal position (row, column)
start = (0, 0)
goal = (9, 9)

# Directions to move: left, right, up, down
moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def bfs(maze, start, goal):
    step_counter = 0
    # Create a queue to store (current_position, path_so_far)
    queue = deque([(start, [start])])
    
    visited = set()
    
    # Loop until queue is empty
    while queue:
        # Take the first element from the queue
        (x, y), path = queue.popleft()
        
        # If we reached the goal, return the path

        step_counter += 1
        print(f"Step {step_counter}: exploring ({x}, {y})")

        if (x, y) == goal:
            return path, step_counter
        
        # Mark this cell as visited
        visited.add((x, y))
        
        # Explore all possible directions
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            
            # Check if new position is valid then adds to queue and path
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]):
                if maze[nx][ny] == 1 and (nx, ny) not in visited:
                    queue.append(((nx, ny), path + [(nx, ny)]))
    return None

def manhattanDist(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def a_star_maze(maze, start, goal):
    pq = PriorityQueue()
    pq.put((manhattanDist(start, goal), [start], 0))  # (f = g + h, path, g)
    visited = set()
    step_counter = 0

    while not pq.empty():
        f, path, g = pq.get()
        x, y = path[-1]

        if (x, y) in visited:
            continue

        visited.add((x, y))
        step_counter += 1

        print(f"Step {step_counter}: exploring ({x}, {y}) | current cost(g)={g}, Dist(h)={manhattanDist((x,y), goal)}, estimated cost(f)={f}")

        if (x, y) == goal:
            return path, g, step_counter

        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == 1:
                if (nx, ny) not in visited:
                    new_g = g+1  # cost of each move is assumed as 1
                    new_f = new_g + manhattanDist((nx, ny), goal)
                    pq.put((new_f, path + [(nx, ny)], new_g))

    return None

# Function prints the maze and the path, step_counter
def printPath(path, steps):
    if path:
        # Create a copy of the maze to visualize path
        maze_with_path = [row[:] for row in maze]
        
        # Mark the path with '*'
        for x, y in path:
            if (x, y) != start and (x, y) != goal:
                maze_with_path[x][y] = '*'
        
        # Mark start and goal
        sx, sy = start
        gx, gy = goal
        maze_with_path[sx][sy] = 'S'
        maze_with_path[gx][gy] = 'E'
        
        # Print the maze
        print("Maze Solution Path:\n")
        for row in maze_with_path:
            print(" ".join(str(cell) for cell in row))
        
        print(f"\n✅ Path found in {steps} steps")
        print(f"Total cost (number of steps in path): {len(path) - 1}")

    else:
        print("No path found!")


print("BFS Search: ")
path, bfs_steps = bfs(maze, start, goal)
printPath(path, bfs_steps)

print("\nA* search: ")
path, cost, astar_steps = a_star_maze(maze, start, goal)
printPath(path, astar_steps)
print(f"Cost of A* path: {cost}")


