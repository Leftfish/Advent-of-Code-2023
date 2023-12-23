from collections import defaultdict, deque

print('Day 23 of Advent of Code!')

WALL = '#'
FLOOR = '.'
SLIDE_RIGHT = '>'
SLIDE_DOWN = 'v'
SLIDE_UP = '^'
SLIDE_LEFT = '<'

DIRECTIONS = UP, DOWN, LEFT, RIGHT = (-1, 0), (1, 0), (0, -1), (0, 1)

FIELD_TO_DIR = {FLOOR: (UP, DOWN, LEFT, RIGHT),
                SLIDE_UP: (UP,),
                SLIDE_DOWN: (DOWN,),
                SLIDE_RIGHT: (RIGHT,),
                SLIDE_LEFT: (LEFT,)}


SLIDES = (SLIDE_DOWN, SLIDE_UP, SLIDE_LEFT, SLIDE_RIGHT)

OPPOSITES = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}


def make_grid(data):
    grid = {}
    for i, line in enumerate(data.splitlines()):
        for j, char in enumerate(line):
            grid[(i, j)] = char
    return grid

def remove_slides(grid):
    new_grid = {}
    for k, v in grid.items():
        if v in SLIDES:
            new_grid[k] = FLOOR
        else:
            new_grid[k] = grid[k]
    return new_grid

def adjacency(grid, first):
    adj = defaultdict(list)
    visited = set()
    stack = []
    stack.append((first, DOWN))

    while stack:
        current, last_direction = stack.pop()
        if current not in visited:
            visited.add(current)
            current_field = grid[current]
            for direction in FIELD_TO_DIR[current_field]:
                if current_field in SLIDES:
                    new_coord = (current[0] + direction[0], current[1] + direction[1])
                    if new_coord in grid and grid[new_coord] != WALL:
                        adj[current].append(new_coord)
                        stack.append((new_coord, direction))
                elif direction != OPPOSITES[last_direction]:
                    new_coord = (current[0] + direction[0], current[1] + direction[1])
                    if new_coord in grid and grid[new_coord] != WALL:
                        adj[current].append(new_coord)
                        stack.append((new_coord, direction))
    return adj


def topsort(adj, first):
    stack = []
    postorder = deque()
    visited = set()
    stack.append(first)

    while stack:
        cur = stack[-1]
        tail = True

        for v in adj[cur]:
            if v not in visited:
                tail = False
                visited.add(v)
                stack.append(v)
                break
        if tail:
            stack.pop()
            postorder.append(cur)

    return postorder


def find_longest(adj, topsorted, first):
    distances = {vertex: 0 for vertex in adj}
    distances[first] = 0

    s = topsorted.copy()
    while s:
        nxt = s.pop()
        for adjacent in adj[nxt]:
            if distances[adjacent] < distances[nxt] + 1:
                distances[adjacent] = distances[nxt] + 1
    return distances


TEST_DATA = '''#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#'''

print('Testing...')
test_grid = make_grid(TEST_DATA)
start = (0, 1)
test_graph = adjacency(test_grid, start)
test_topsorted = topsort(test_graph, start)
print('Part 1:', find_longest(test_graph, test_topsorted, start)[test_topsorted[0]] == 94)

with open('inp', mode='r', encoding='utf-8') as inp:
    print('Solution...')
    actual_data = inp.read()
    actual_grid = make_grid(actual_data)
    start = (0, 1)
    actual_graph = adjacency(actual_grid, start)
    actual_topsorted = topsort(actual_graph, start)
    print('Part 1:', find_longest(actual_graph, actual_topsorted, start)[actual_topsorted[0]])
