from ai.pathfinding import bfs,reachable_within
SEARCH_TIME = 25 
class Cop :
    
    def __init__(self, start_pos,waypoints):
        self.pos = start_pos
        self.state = "PATROL"
        self.path = []
        self.waypoints = waypoints
        self.wp_index = 1
        self.store = None
        self.checked = set()
        self.tick = 0
        self.robbery_tick = 0
        self.search_timer = 0
       



    def update(self,grid):
        self.tick +=1
        if self.state == "PATROL":
          self.patrol(grid)
        elif self.state == "RESPOND":
            self.respond(grid)
        elif self.state == "SEARCH":
            self.search(grid)
    def go_to(self, grid, target):
        full_path = bfs(grid, self.pos, target)
        self.path = full_path[1:] if full_path else []

    def step(self):
        if self.path:
            self.pos = self.path.pop(0)


    def patrol(self, grid):
        target = self.waypoints[self.wp_index]
        if not self.path:
            self.go_to(grid, target)
        self.step()
        if self.pos == target:
            self.wp_index = (self.wp_index + 1) % len(self.waypoints)

    def alarm(self , store_pos):
       self.state = "RESPOND"
       self.store = store_pos
       self.robbery_tick = self.tick
       self.path.clear()
       self.checked.clear()

    def respond(self,grid):
        if not self.path:
            self.go_to(grid, self.store)
        self.step()
        if self.pos == self.store:
            self.state = "SEARCH"
            self.search_timer = SEARCH_TIME

             
        

    def search(self, grid):
       
        self.checked.add(self.pos)     
        if not self.path:
            elapsed = self.tick - self.robbery_tick
            zone = reachable_within(grid, self.store, elapsed)
            candidates = [t for t in zone if t not in self.checked]
            if candidates:
                r, c = self.pos
                target = min(candidates, key=lambda t: abs(t[0] - r) + abs(t[1] - c))
                self.go_to(grid, target)
        self.step()

        self.search_timer -= 1
        if self.search_timer <= 0:
            self.state = "PATROL"
            self.path = []
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

    for _ in range(5):
        cop.update(grid)
    print("--- ROBBERY at tick", cop.tick, "---")
    cop.alarm((3, 5))

    for _ in range(35):
        cop.update(grid)
        extra = f"  timer={cop.search_timer}" if cop.state == "SEARCH" else ""
        print(f"tick {cop.tick:2}  {cop.state:8} {cop.pos}{extra}")    
