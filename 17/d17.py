from collections import defaultdict
import heapq

print('Day 17 of Advent of Code!')

### Solution strongly inspired by https://github.com/snhansen/adventofcode/blob/master/2023/day17/solution.py
### I immediately knew I needed Dijkstra's algorithm with a twist, but after the fourth attempt to implement 
### a twist failed, I needed to see where I made the mistake. This solution helped me a lot.

UP, DOWN, LEFT, RIGHT = (-1, 0), (1, 0), (0, -1), (0, 1)


def make_grid(data):
    graph = defaultdict(int)
    for i, line in enumerate(data.splitlines()):
        for j, cost in enumerate(line):
            graph[(i,j)] = int(cost)
    corner = (i, j)
    return graph, corner


def dijkstra_with_a_twist(graph, corner):
    visited = set()
    first_pos = (0,0)
    # state = (cost, position, last_dir, hops)

    Q = []
    heapq.heappush(Q, (0, first_pos, RIGHT, 0))
    heapq.heappush(Q, (0, first_pos, DOWN, 0))

    while Q:
        cost, position, last_dir, hops = heapq.heappop(Q)
        if (position, last_dir, hops) in visited:
            continue
        visited.add((position, last_dir, hops))

        if position == corner:
            return cost
        
        # possible turns
        if last_dir in (UP, DOWN):
            dirs = (LEFT, RIGHT)
        if last_dir in (LEFT, RIGHT):
            dirs = (UP, DOWN)
        for new_dir in dirs:
            new_pos = position[0] + new_dir[0], position[1] + new_dir[1]
            if new_pos in graph:
                heapq.heappush(Q, (cost + graph[new_pos], new_pos, new_dir, 1))

        # straight ahead because we still can
        if hops < 3:
            new_pos = position[0] + last_dir[0], position[1] + last_dir[1]
            if new_pos in graph:
                heapq.heappush(Q, (cost + graph[new_pos], new_pos, last_dir, hops+1))


TEST_DATA = '''2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533'''

print('Testing...')
test_graph, test_final = make_grid(TEST_DATA)
print(dijkstra_with_a_twist(test_graph, test_final))

with open('inp', mode='r', encoding='utf-8') as inp:
    print('Solution...')
    actual_data = inp.read()
    actual_graph, actual_final = make_grid(actual_data)
    print(dijkstra_with_a_twist(actual_graph, actual_final))


