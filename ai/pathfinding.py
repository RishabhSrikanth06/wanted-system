from collections import deque
test_grid = [
    "#####",
    "#A..#",
    "#.#.#",
    "#..B#",
    "#####",
]
MOVEMENTS = [(-1,0),(0,-1),(1,0),(0,1)]

def valid_neighbours(grid, tile):
  row,col = tile
  result = []
  for dr, dc  in MOVEMENTS:
    new_row = dr + row
    new_col = dc + col
    if (0 <= new_row < len(grid)
                and 0 <= new_col < len(grid[new_row])
                and grid[new_row][new_col] != '#'):
            result.append((new_row, new_col))
  return result

def bfs(grid , start , end ):
    queue = deque()
    queue.append(start)
    node_arrived_from = {start:None}
    while queue:
        item = queue.popleft()
        if item == end:
            return rebuild_path(node_arrived_from, end)
        neighbours = valid_neighbours(grid,item)
        for neighbour in neighbours:
         if neighbour not in node_arrived_from:      
          node_arrived_from[neighbour] = item     
          queue.append(neighbour)      
    return None 

def rebuild_path(node_arrived_from, end):
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = node_arrived_from[current]
    path.reverse()
    return path
                   
def find_waypoints(grid):
    found = []
    for row, line in enumerate(grid):
        for col, char in enumerate(line):
            if char.isdigit():
                found.append((int(char), (row, col)))
    found.sort()
    return [pos for _, pos in found]

def reachable_within(grid, start, max_steps):
    distance = {start: 0}
    queue = deque([start])
    while queue:
        current = queue.popleft()
        if distance[current] == max_steps:
            continue                      # on the edge: don't spread further
        for n in valid_neighbours(grid, current):
            if n not in distance:
                distance[n] = distance[current] + 1
                queue.append(n)
    return distance
