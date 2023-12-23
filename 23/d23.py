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


def adjacency_with_slides(grid, first):
    graph = defaultdict(list)
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
                        graph[current].append(new_coord)
                        stack.append((new_coord, direction))
                elif direction != OPPOSITES[last_direction]:
                    new_coord = (current[0] + direction[0], current[1] + direction[1])
                    if new_coord in grid and grid[new_coord] != WALL:
                        graph[current].append(new_coord)
                        stack.append((new_coord, direction))
    return graph


def topsort(graph, first):
    stack = []
    postorder = []
    visited = set()
    stack.append(first)

    while stack:
        current = stack[-1]
        tail = True

        for v in graph[current]:
            if v not in visited:
                tail = False
                visited.add(v)
                stack.append(v)
                break
        if tail:
            stack.pop()
            postorder.append(current)

    return postorder


def find_longest_with_slides(graph, topsorted, origin):
    distances = {vertex: 0 for vertex in graph}
    distances[origin] = 0

    while topsorted:
        nxt = topsorted.pop()
        for adjacent in graph[nxt]:
            if distances[adjacent] < distances[nxt] + 1:
                distances[adjacent] = distances[nxt] + 1
    return distances


def adjacency_without_slides(grid):
    graph = defaultdict(list)
    for fld in grid:
        if fld != WALL:
            for d in DIRECTIONS:
                new_coord = (fld[0] + d[0], fld[1] + d[1])
                if new_coord in grid and grid[new_coord] != WALL:
                    graph[fld].append(new_coord)
    return graph


def compress_graph(origin, target, graph):
    compressed = defaultdict(dict)
    big_nodes = [v for v in graph if len(graph[v]) > 2]

    for node in big_nodes:
        q = deque()
        visited = set()
        for neighbor in graph[node]:
            move = (neighbor, 1)
            q.append(move)
        while q:
            current, steps = q.pop()
            if current in big_nodes and current != node:
                compressed[current][node] = steps
                compressed[node][current] = steps
                continue
            if current in (origin, target):
                compressed[current][node] = steps
                compressed[node][current] = steps
                continue
            visited.add(current)
            for neighbor in graph[current]:
                if neighbor not in visited and neighbor != node:
                    q.append((neighbor, steps+1))
    return compressed


def get_all_paths(origin, target, graph):
    def dfs(target, current_path, visited, graph, path_list):
        current_node = current_path[-1]
        if current_node == target:
            path_list.append(list(current_path))
        else:
            for neighbor in graph[current_node]:
                if neighbor not in visited:
                    current_path.append(neighbor)
                    visited.add(neighbor)
                    dfs(target, current_path, visited, graph, path_list)
                    visited.remove(neighbor)
                    current_path.pop()
        return path_list

    return dfs(target, [origin], set(origin), graph, list())


def find_longest_without_slides(paths):
    distances = []
    for p in paths:
        d = 0
        for this, nxt in zip(p, p[1:]):
            d += proper_adj[this][nxt]
        distances.append(d)
    return max(distances)


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
test_graph = adjacency_with_slides(test_grid, start)
test_topsorted = topsort(test_graph, start)
end = test_topsorted[0]
proper_adj = compress_graph(start, end, adjacency_without_slides(test_graph))
print('Part 1:', find_longest_with_slides(test_graph, test_topsorted, start)[end] == 94)
print('Part 2:', find_longest_without_slides(get_all_paths(start, end, proper_adj)) == 154)


with open('inp', mode='r', encoding='utf-8') as inp:
    print('Solution...')
    actual_grid = make_grid(inp.read())
    start = (0, 1)
    actual_graph = adjacency_with_slides(actual_grid, start)
    actual_topsorted = topsort(actual_graph, start)
    end = actual_topsorted[0]
    proper_adj = compress_graph(start, end, adjacency_without_slides(actual_graph))
    print('Part 1:', find_longest_with_slides(actual_graph, actual_topsorted, start)[end])
    print('Part 2:', find_longest_without_slides(get_all_paths(start, end, proper_adj)))
