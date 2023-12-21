import heapq

print('Day 21 of Advent of Code!')

START = 'S'
PLOT = '.'
WALL = '#'

DIRECTIONS = UP, DOWN, LEFT, RIGHT = (-1, 0), (1, 0), (0, -1), (0, 1)


def make_grid(data):
    lines = [list(line) for line in data.splitlines()]
    grid = {}
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            grid[(i, j)] = lines[i][j]
    return grid


def find_start(grid):
    for coord, val in grid.items():
        if val == START:
            return coord
    raise ValueError


def dijkstra(grid, start):
    distances = {vertex: float('inf') for vertex in grid if grid[vertex] != WALL}
    distances[start] = 0
    visited = set()

    pq = []
    heapq.heapify(pq)
    heapq.heappush(pq, (0, start))

    while pq:
        _, current = heapq.heappop(pq)
        visited.add(current)

        neighbors = set()
        for d in DIRECTIONS:
            new_coord = (current[0] + d[0], current[1] + d[1])
            if new_coord in grid and grid[new_coord] != WALL:
                neighbors.add(new_coord)

        for neighbor in neighbors - visited:
            old_cost = distances[neighbor]
            new_cost = distances[current] + 1
            if new_cost < old_cost:
                heapq.heappush(pq, (new_cost, neighbor))
                distances[neighbor] = new_cost
    return distances


TEST_DATA = '''...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........'''


print('Testing...')
test_grid = make_grid(TEST_DATA)
print('Part 1:', len([(d, v) for d, v in dijkstra(test_grid, find_start(test_grid)).items() if v <= 6 and not v % 2]) == 16)

with open('inp', mode='r', encoding='utf-8') as inp:
    print('Solution...')
    actual_grid = make_grid(inp.read())
    print('Part 1:', len([(d, v) for d, v in dijkstra(actual_grid, find_start(actual_grid)).items() if v <= 64 and not v % 2]))
