from collections import defaultdict
from itertools import product

print('Day 22 of Advent of Code!')



TEST_DATA = '''1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9'''

FLOOR = 0

class Brick:
    def __init__(self, coords) -> None:
        self.coords = coords
        self.moving = True
        self.supports = set()
        self.supported_by = set()

    def __repr__(self) -> str:
        return f'{self.coords}'
    
    def bottom_row(self):
        min_z = min(coord[2] for coord in self.coords)
        return set((coord for coord in self.coords if coord[2] == min_z))
    
    def top_row(self):
        max_z = max(coord[2] for coord in self.coords)
        return set((coord for coord in self.coords if coord[2] == max_z))
    
    def is_on_bottom(self):
        min_z = min(coord[2] for coord in self.coords)
        return min_z == 1
    
    def is_something_below(self, grid):
        one_below = set([(x, y, z-1) for x, y, z in self.bottom_row()])
        belows = [coord in grid for coord in one_below]
        return any(belows) or self.is_on_bottom()
    
    def find_supporting_bricks(self, grid):
        for field in self.bottom_row():
            coord = (field[0], field[1], field[2]-1)
            if coord in grid:
                below = grid[coord]
                if below != self:
                    self.supported_by.add(below)
                    below.supports.add(self)

    def drop(self, grid):
        new_coords = set([(x, y, z-1) for x, y, z in self.coords])
        for old_coord in self.coords:
            del grid[old_coord]
        self.coords = new_coords
        for new_coord in self.coords:
            grid[new_coord] = self

    def stop(self):
        self.moving = False


def make_bricks(data):
    brick_coords = data.splitlines()
    bricks = []
    grid = {}
    for brick_coord in brick_coords:
        start, end = brick_coord.split('~')
        sx, sy, sz = [int(d) for d in start.split(',')]
        ex, ey, ez = [int(d) for d in end.split(',')]

        occupied_by_this = set()
        for x in range(sx, ex+1):
            for y in range(sy, ey+1):
                for z in range(sz, ez+1):
                    occupied_by_this.add((x, y, z))
        new_brick = Brick(occupied_by_this)
        bricks.append(new_brick)
        for coord in occupied_by_this:
            grid[coord] = new_brick  
    for brick in bricks:
        brick.find_supporting_bricks(grid)
    return bricks, grid


def move_bricks(bricks, grid):
    i = 0
    for b in bricks:
        while True:
            if not b.is_something_below(grid):
                b.drop(grid)
                print(f'{i} dropping by one')
            else:
                b.find_supporting_bricks(grid)
                b.stop()
                break
        i += 1

with open('inp', mode='r', encoding='utf-8') as inp:
    actual_data = inp.read()

test_bricks, grid = make_bricks(TEST_DATA)
bricks = sorted(test_bricks, key=lambda brick: min(coord[2] for coord in brick.coords))
move_bricks(bricks, grid)
boomable = 0
for i, brick in enumerate(bricks):
    print('Checking', i)
    supported = len(brick.supports)
    if not supported:
        boomable += 1
        continue
    else:
        others = [len(other.supported_by) > 1 for other in brick.supports]
        if all(others):
            boomable += 1

print(boomable)

'''ITERUJ PRZEZ BRICKI
- CZY TEN BRICK NIKOGO NIE SUPPORTUJE? DEZINTEGRUJ
- CZY TEN BRICK KOGOŚ SUPPORTUJE:
    CZY KOGOŚ MA SUPPORTED_BY DŁUŻSZE NIŻ 1? ZDEZINTEGRUJ'''