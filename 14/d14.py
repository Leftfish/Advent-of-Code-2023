from itertools import cycle

print('Day 14 of Advent of Code!')

STONE = 'O'
BLOCK = '#'

UP = 'U'
DOWN = 'D'
LEFT = 'L'
RIGHT = 'R'

DIRECTIONS = cycle((UP, LEFT, DOWN, RIGHT))


def parse_grid(data):
    grid = {}
    lines = data.splitlines()

    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            grid[(i,j)] = char
    return grid, len(lines), len(lines[0])


def get_rows(grid, i, j):
    rows = []
    for row in range(i):
        rows.append(([grid[row,col] for col in range(j)]))
    return rows


def get_cols(grid, i, j):
    cols = []
    for col in range(j):
        cols.append([grid[row, col] for row in range(i)])
    return cols


def hash_grid(grid):
    return hash(str(grid.items()))


def parse_col_or_row(colrow, direction):
    stones = []
    blocks = []
    for idx, item in enumerate(colrow):
        if item == STONE:
            stones.append(idx)
        if item == BLOCK:
            blocks.append(idx)
    if direction == UP or direction == LEFT:
        blocks.insert(0, -1)
    elif direction == DOWN or direction == RIGHT:
        blocks.append(len(colrow))
    return stones, blocks


def move_rocks(grid, idx, colrows, direction):
    stones, blocks = parse_col_or_row(colrows[idx], direction)

    if not stones:
        return stones, grid

    # remove stones first
    if direction == UP or direction == DOWN:
        for stone_pos in stones:
            grid[stone_pos, idx] = '.'
    elif direction == LEFT or direction == RIGHT:
        for stone_pos in stones:
            grid[idx, stone_pos] = '.'

    # move stones
    if direction == UP or direction == LEFT:
        for i in range(len(stones)):
            for j in range(len(blocks)-1, -1, -1):
                if blocks[j] < stones[i]:
                    stones[i] = blocks[j] + 1
                    blocks[j] += 1
                    break
    elif direction == DOWN or direction == RIGHT:
        for i in range(len(stones)-1, -1, -1):
            for j in range(0, len(blocks), 1):
                if blocks[j] > stones[i]:
                    stones[i] = blocks[j] - 1
                    blocks[j] -= 1
                    break

    # put the stones back in grid
    if direction == UP or direction == DOWN:
        for stone_pos in stones:
            grid[stone_pos, idx] = 'O'
    elif direction == LEFT or direction == RIGHT:
        for stone_pos in stones:
            grid[idx, stone_pos] = 'O'

    return stones, grid


def count_load(columns):
    s = 0
    for col in columns:
        stones, _ = parse_col_or_row(col, UP)
        max_score = len(col)
        scores = [max_score - stone for stone in stones]
        s += sum(scores)
    return s


def spin_cycle(data):
    grid, i, j = parse_grid(data)

    rounds = 0
    hashes = {}
    hashes[rounds] = hash_grid(grid)

    scores = {}
    scores[rounds] = count_load(get_cols(grid, i, j))

    cycle_start = None
    cycle_lenght = None

    while True:
        for _ in range(4):
            next_dir = next(DIRECTIONS)
            if next_dir == UP or next_dir == DOWN:
                colrows = get_cols(grid, i, j)
            elif next_dir == LEFT or next_dir == RIGHT:
                colrows = get_rows(grid, i, j)
            for idx in range(len(colrows)):
                _, grid = move_rocks(grid, idx, colrows, next_dir)

        rounds += 1
        current_hash = hash_grid(grid)

        for rd, hsh in hashes.items():
            if not cycle_start and hsh == current_hash:
                cycle_start = rd
            if cycle_start and current_hash == hashes[cycle_start]:
                cycle_lenght = rounds - cycle_start

        hashes[rounds] = current_hash
        scores[rounds] = count_load(get_cols(grid, i, j))

        if cycle_start and cycle_lenght:
            proper_id = cycle_start + ((1000000000 - cycle_start) % cycle_lenght)
            return scores[proper_id]


TEST_DATA = '''O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....'''


print('Testing...')
test_grid, h, w = parse_grid(TEST_DATA)
test_cols = get_cols(test_grid, h, w)
for col_idx in range(len(test_cols)):
    _, test_grid = move_rocks(test_grid, col_idx, test_cols, UP)
print('Part 1:', count_load(get_cols(test_grid, w, h)) == 136)
print('Part 2:', spin_cycle(TEST_DATA) == 64)

with open('inp', mode='r', encoding='utf-8') as inp:
    print('Solution...')
    actual_data = inp.read()
    actual_grid, w, h = parse_grid(actual_data)
    actual_cols = get_cols(actual_grid, w, h)
    for col_idx in range(len(actual_cols)):
        _, actual_grid = move_rocks(actual_grid, col_idx, actual_cols, UP)
    print('Part 1:', count_load(get_cols(actual_grid, w, h)))
    print('Part 2:', spin_cycle(actual_data))
