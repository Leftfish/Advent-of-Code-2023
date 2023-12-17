from collections import defaultdict
import heapq

print('Day 17 of Advent of Code!')

### Strongly inspired by https://github.com/snhansen/adventofcode/blob/master/2023/day17/solution.py
### by Stefan Hansen I immediately knew I needed Dijkstra's algorithm with a twist, but after the
### fourth attempt to implement the twist failed, I needed to see where I made the mistake. This
### solution helped me a lot. The idea to use (cost, position, last_dir, hops) as states really made
### everything click. Previously I had trouble implementing the length of current straight move.

UP, DOWN, LEFT, RIGHT = (-1, 0), (1, 0), (0, -1), (0, 1)


def make_grid(data):
    grid = defaultdict(int)
    lines = data.splitlines()
    for i, line in enumerate(lines):
        for j, cost in enumerate(line):
            grid[(i,j)] = int(cost)
    corner = (len(lines)-1, len(lines[0])-1)
    return grid, corner


def dijkstra_with_a_twist(grid, corner, minimum_before_turn, maximum_before_turn):
    visited = set()
    state_queue = [(0, (0,0), RIGHT, 0), (0, (0,0), DOWN, 0)]
    heapq.heapify(state_queue)

    while state_queue:
        cost, position, last_dir, hops = heapq.heappop(state_queue)
        if (position, last_dir, hops) in visited:
            continue
        visited.add((position, last_dir, hops))

        if position == corner and hops >= minimum_before_turn:
            return cost

        # if straight ahead possible
        if hops < maximum_before_turn:
            new_pos = position[0] + last_dir[0], position[1] + last_dir[1]
            if new_pos in grid:
                heapq.heappush(state_queue, (cost + grid[new_pos], new_pos, last_dir, hops+1))

        # if turn possible, switch to vertical if previous horizontal
        if hops >= minimum_before_turn:
            available_dirs = (LEFT, RIGHT) if last_dir in (UP, DOWN) else (UP, DOWN)

            for new_dir in available_dirs:
                new_pos = position[0] + new_dir[0], position[1] + new_dir[1]
                if new_pos in grid:
                    heapq.heappush(state_queue, (cost + grid[new_pos], new_pos, new_dir, 1))


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
test_grid, test_final = make_grid(TEST_DATA)
print('Part 1:', dijkstra_with_a_twist(test_grid, test_final, 0, 3) == 102)
print('Part 2:', dijkstra_with_a_twist(test_grid, test_final, 4, 10) == 94)

with open('inp', mode='r', encoding='utf-8') as inp:
    print('Solution...')
    actual_data = inp.read()
    actual_grid, actual_final = make_grid(actual_data)
    print('Part 1:', dijkstra_with_a_twist(actual_grid, actual_final, 0, 3))
    print('Part 2:', dijkstra_with_a_twist(actual_grid, actual_final, 4, 10))
