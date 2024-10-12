from collections import deque, defaultdict

print('Day 21 of Advent of Code!')

START = 'S'
PLOT = '.'
WALL = '#'

DIRECTIONS = UP, DOWN, LEFT, RIGHT = (-1, 0), (1, 0), (0, -1), (0, 1)

def make_grid(data):
    return [list(line) for line in data.splitlines()]

def find_start(grid):
    for i, line in enumerate(grid):
        for j, _ in enumerate(line):
            if grid[i][j] == START:
                return (i, j)
    return (None, None)


def count_distances(grid, start, max_distance):
    def find_neighbors(point):
        neighbors = set()
        for d in DIRECTIONS:
            candidate = (point[0] + d[0], point[1] + d[1])
            if grid[candidate[1] % 131][candidate[0] % 131] != WALL: # 131 = dimension of the input
                neighbors.add(candidate)
        return neighbors

    reachable_tiles = defaultdict(int)
    visited = set()
    q = deque()
    q.append((0, start))

    while q:
        distance, point = q.popleft()
        if distance == (max_distance + 1) or point in visited:
            continue

        visited.add(point)
        reachable_tiles[distance] += 1

        for neighbor in find_neighbors(point):
            if neighbor not in visited:
                q.append((distance + 1, neighbor))

    return reachable_tiles


with open('inp', mode='r', encoding='utf-8') as inp:
    print('Solution...')
    garden = make_grid(inp.read())
    start = find_start(garden)
    print('Part 1:', sum(v for k, v in count_distances(garden, start, 64).items() if k % 2 == 0))

three_points = [sum(amount for distance, amount in \
                count_distances(garden, find_start(garden), max_steps).items() \
                if distance % 2 == max_steps % 2) for max_steps in (65, 196, 327)]

N = MAGIC_NUMBER = 202300 # another magic number (geometry again!)
c = three_points[0]
a = (three_points[2] - 2 * three_points[1] + three_points[0]) // 2
b = three_points[1] - a - c

print('Part 2:', (a * N**2) + (b * N) + c)

'''
Kudos to CalSimmon (https://github.com/CalSimmon/advent-of-code/blob/main/2023/day_21/solution.py),
Dazbo (https://github.com/derailed-dash/Advent-of-Code/blob/master/src/AoC_2023/Dazbo's_Advent_of_Code_2023.ipynb) and
to villuna (https://github.com/villuna/aoc23/wiki/A-Geometric-solution-to-advent-of-code-2023,-day-21)
for their writeups.
'''

