print('Day 14 of Advent of Code!')

STONE = 'O'
BLOCK = '#'

def get_columns(raw_data):
    data = raw_data.splitlines()
    return [[data[y][x ] for y in range(len(data))] for x in range(len(data[0]))]

def parse_column(column):
    stones = []
    blocks = [-1]
    for idx, item in enumerate(column):
        if item == STONE:
            stones.append(idx)
        if item == BLOCK:
            blocks.append(idx)
    return stones, blocks

def move_rocks_north(column):
    stones, blocks = parse_column(column)
    if not stones:
        return stones, blocks
    for i in range(len(stones)):
        for j in range(len(blocks)-1, -1, -1):
            if blocks[j] < stones[i]:
                stones[i] = blocks[j] + 1
                blocks[j] += 1
                break
    return stones, blocks

def score_columns(columns):
    s = 0
    for col in columns:
        stones, _ = move_rocks_north(col)
        max_score = len(col)
        scores = [max_score - stone for stone in stones]
        s += sum(scores)
    return s

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
columns = get_columns(TEST_DATA)
print('Part 1:', score_columns(columns) == 136)

with open('inp', mode='r', encoding='utf-8') as inp:
    print('Solution...')
    actual_data = inp.read()    
    columns = get_columns(actual_data)
    print('Part 1:', score_columns(columns))
