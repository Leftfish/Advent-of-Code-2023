from itertools import combinations

print('Day 11 of Advent of Code!')

GALAXY = '#'
VOID = '.'

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


def find_offset(galaxies, empty_lines, empty_columns):
    for galaxy in galaxies:
        offset_line = sum([1 for line in empty_lines if line < galaxy[0]])
        offset_column = sum([1 for column in empty_columns if column < galaxy[1]])
        galaxy[0] += offset_line
        galaxy[1] += offset_column

def manhattan(first, second):
    return abs(first[0] - second[0]) + abs(first[1] - second[1])


test_map = get_galaxy_map(TEST_DATA)
test_galaxies = find_galaxies(test_map)
empty_lines, empty_columns = find_empty_space(test_map)
find_offset(test_galaxies, empty_lines, empty_columns)

pairs = list(combinations(test_galaxies, 2))
manhattans = [manhattan(*pair) for pair in pairs]
print(sum(manhattans))

print('Testing...')

with open('inp', mode='r', encoding='utf-8') as inp:
    print('Solution...')
    actual_data = inp.read()
    test_map = get_galaxy_map(actual_data)
    test_galaxies = find_galaxies(test_map)
    empty_lines, empty_columns = find_empty_space(test_map)
    find_offset(test_galaxies, empty_lines, empty_columns)

    pairs = list(combinations(test_galaxies, 2))
    manhattans = [manhattan(*pair) for pair in pairs]
    print(sum(manhattans))

