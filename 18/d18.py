import re

print('Day 18 of Advent of Code!')

DIRS = {'U': (-1, 0),
              'D': (1, 0), 
              'L': (0, -1), 
              'R': (0, 1)}

REGEX = r'(\w) (\d+) \((#\w+)\)'


def parse_instructions(data):
    instructions = []
    for line in data.splitlines():
        direction, distance = re.findall(REGEX, line)[0][:2]
        instructions.append((direction, int(distance)))
    return instructions


def parse_instructions_again(data):
    instructions = []
    int_to_dir = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}
    for line in data.splitlines():
        hexes = re.findall(REGEX, line)[0][-1]
        direction = int_to_dir[hexes[-1]]
        distance = int('0x' + hexes[1:6], 16)
        instructions.append((direction, distance))
    return instructions


def dig(cmds):
    vertices = [(0,0)]
    border = 0
    for cmd in cmds:
        direction, distance = cmd
        start = vertices[-1]
        end = (start[0] + distance * DIRS[direction][0], start[1] + distance * DIRS[direction][1])
        vertices.append(end)
        border += distance
    return vertices, border


def area(xs, ys, border):
    ### adapted from https://rosettacode.org/wiki/Shoelace_formula_for_polygonal_area
    shoelace = 0.5 * abs(sum(i * j for i, j in zip(xs, ys[1:] + ys[:1]))
               - sum(i * j for i, j in zip(xs[1:] + xs[:1], ys)))
    return shoelace + border / 2 + 1


TEST_DATA = '''R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)'''

print('Testing...')
test_cmds = parse_instructions(TEST_DATA)
new_test_cmds = parse_instructions_again(TEST_DATA)
test_vertices, test_border = dig(test_cmds)
print('Part 1:', int(area(*zip(*test_vertices), test_border)) == 62)
test_vertices, test_border = dig(new_test_cmds)
print('Part 2:', int(area(*zip(*test_vertices), test_border)) == 952408144115)

with open('inp', mode='r', encoding='utf-8') as inp:
    print('Solution...')
    actual_data = inp.read()
    actual_cmds = parse_instructions(actual_data)
    new_actual_cmds = parse_instructions_again(actual_data)
    actual_vertices, actual_border = dig(actual_cmds)
    print('Part 1:', int(area(*zip(*actual_vertices), actual_border)))
    actual_vertices, actual_border = dig(new_actual_cmds)
    print('Part 2:', int(area(*zip(*actual_vertices), actual_border)))
