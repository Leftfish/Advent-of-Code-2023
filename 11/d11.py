from copy import deepcopy
from itertools import combinations

print('Day 11 of Advent of Code!')

GALAXY = '#'
VOID = '.'


def get_galaxy_map(data):
    return [list(line) for line in data.splitlines()]


def find_galaxies(galaxy_map):
    galaxies = []
    for i, line in enumerate(galaxy_map):
        for j, char in enumerate(line):
            if char == GALAXY:
                galaxies.append([i, j])

    return galaxies


def find_empty_space(galaxy_map):
    empty_lines = [i for i, line in enumerate(galaxy_map) if set(line) == {VOID}]
    empty_columns = []
    for j in range(len(galaxy_map[0])):
        if set([galaxy_map[i][j] for i in range(len(galaxy_map))]) == {VOID}:
            empty_columns.append(j)
    return empty_lines, empty_columns


def find_offset(galaxies, offset_distance, empty_lines, empty_columns):
    new_galaxies = deepcopy(galaxies)
    for galaxy in new_galaxies:
        offset_line = sum([offset_distance-1 for line in empty_lines if line < galaxy[0]])
        offset_column = sum([offset_distance-1 for column in empty_columns if column < galaxy[1]])
        galaxy[0] += offset_line
        galaxy[1] += offset_column
    return new_galaxies


def manhattan(first, second):
    return abs(first[0] - second[0]) + abs(first[1] - second[1])


TEST_DATA = '''...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....'''

print('Testing...')
test_map = get_galaxy_map(TEST_DATA)
test_galaxies = find_galaxies(test_map)
part1_galaxies = find_offset(test_galaxies, 2, *find_empty_space(test_map))
part2_galaxies = find_offset(test_galaxies, 10, *find_empty_space(test_map))
print('Part 1:', sum([manhattan(*pair) for pair in combinations(part1_galaxies, 2)]) == 374)
print('Part 2:', sum([manhattan(*pair) for pair in combinations(part2_galaxies, 2)]) == 1030)

with open('inp', mode='r', encoding='utf-8') as inp:
    print('Solution...')
    actual_map = get_galaxy_map(inp.read())
    actual_galaxies = find_galaxies(actual_map)
    part1_galaxies = find_offset(actual_galaxies, 2, *find_empty_space(actual_map))
    part2_galaxies = find_offset(actual_galaxies, 1_000_000, *find_empty_space(actual_map))
    print('Part 1:', sum([manhattan(*pair) for pair in combinations(part1_galaxies, 2)]))
    print('Part 2:', sum([manhattan(*pair) for pair in combinations(part2_galaxies, 2)]))
