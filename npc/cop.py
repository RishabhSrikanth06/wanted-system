from ai.pathfinding import bfs

class Cop :
    def __init__(self, start_pos,waypoints):
        self.pos = start_pos
        self.state = "PATROL"
        self.path = []
        self.waypoints = waypoints
        self.wp_index = 1
    def update(self,grid):
        if self.state == "PATROL":
          self.patrol(grid)
        elif self.state == "RESPOND":
            self.respond(grid)
        elif self.state == "SEARCH":
            self.search(grid)
    def patrol(self, grid):
        target = self.waypoints[self.wp_index]
        if not self.path:
          full_path = bfs(grid, self.pos, target)
          self.path = full_path[1:]
        if self.path:
            self.pos = self.path.pop(0)
      
        if self.pos == target:
           self.wp_index = (self.wp_index + 1) % len(self.waypoints)

if __name__ == "__main__":
    from ai.pathfinding import find_waypoints

    grid = [
        "###########",
        "#1.......2#",
        "#.##.#.##.#",
        "#....S....#",
        "#.##.#.##.#",
        "#4......H3#",
        "###########",
    ]

    wps = find_waypoints(grid)
    cop = Cop(wps[0], wps)

    for tick in range(26):
        cop.update(grid)
        print(tick + 1, cop.pos)
   
    

        