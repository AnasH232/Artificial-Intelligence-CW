import time
from queue import PriorityQueue

# 0 is blank space
goal = [[1,2,3],
        [4,5,6],
        [7,8,0]]

initial_state = [[[1,2,3],[4,5,6],[7,8,0]],
          [[1,2,3],[4,5,6],[0,7,8]],
          [[1,0,3],[4,6,2],[7,8,5]],
          [[7,2,4],[5,0,6],[8,3,1]],
          [[1,2,3],[4,5,6],[8,7,0]]]

# Directions to move: left, right, up, down
moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def misplaced_count(state, goal):
    count = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0 and state[i][j] != goal[i][j]:
                count+=1
    return count

def manhattan_dist(state, goal):
    dist = 0
    goal_dict = {}

    for i in range(3):
        for j in range(3):
            goal_dict[goal[i][j]] = (i,j)

    for i in range(3):
        for j in range(3):
            if state[i][j]!=0:
                g_i, g_j = goal_dict[state[i][j]]
                dist += abs(i-g_i) + abs(j-g_j)

    return dist

def a_star(start, goal, heuristic):
    pq = PriorityQueue()
    pq.put((heuristic(start,goal),[start], 0))
    visited = set()
    step_counter = 0
    t1 = time.time()

    while not pq.empty():
        f, path, g = pq.get()
        curr_state = path[-1]

        #have to convert state into tuple so it can be added to visited set
        state_tup = tuple(tuple(row) for row in curr_state)

        if state_tup in visited:
            continue
        visited.add(state_tup)
        step_counter+=1

        if curr_state == goal:
            total_time = time.time() -t1
            return path, g, step_counter, total_time
        
        #loop to find blank space (0)
        for i in range(3):
            for j in range(3):
                if curr_state[i][j]==0:
                    x, y = i, j
        
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0<=nx<3 and 0<=ny<3:
                new_state = [row[:] for row in curr_state]
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
                
                #convert new state to tuple to check if in set
                new_tuple = tuple(tuple(row) for row in new_state)
                if new_tuple not in visited:
                    new_g = g+1
                    new_f = new_g + heuristic(new_state, goal)
                    pq.put((new_f, path + [new_state], new_g))
    
    total_time = time.time() - t1
    print("This puzzle is unsolvable.")
    print(f"Time taken: {total_time}")
    return None, None, step_counter, total_time

count=0
for state in initial_state:
    count+=1
    print(f"\n------------------------------------------------------State {count}------------------------------------------------------")
    print("\n Initial grid: ")
    for row in state:
        print(row)
    
    #Misplaced tiles performed first
    print("\nHeuristic: Misplaced Tiles")
    path, cost, steps, t = a_star(state, goal, misplaced_count)
    if path:
        for grid in path:
            for row in grid:
                print(row)
            print("")

        print(f"Solved in {cost} moves")
        print(f"Time taken: {t}s")
        print(f"Nodes expanded: {steps}")

    #Manhattan Distance done next
    print("\nHeuristic: Manhattan Distance")
    path, cost, steps, t = a_star(state, goal, manhattan_dist)
    if path:
        for grid in path:
            for row in grid:
                print(row)
            print("")

        print(f"Solved in {cost} moves")
        print(f"Time taken: {t}s")
        print(f"Nodes expanded: {steps}")
