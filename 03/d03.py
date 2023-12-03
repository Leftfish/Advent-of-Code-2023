from functools import reduce
from operator import mul
from typing import List, Set, Tuple

print('Day 3 of Advent of Code!')


ADJACENTS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
EMPTY = '.'
GEAR = '*'
MINIMUM_ADJACENT_TO_GEAR = 2


def build_schematics(schematics_string: str) -> List[List[str]]:
    '''Builds a list of lists from the data string'''
    return [list(row) for row in schematics_string.splitlines()]


def parse_schematics(schematics: List[List[str]]) -> Tuple[List[Tuple[int, Set[Tuple[int, int]]]], Set[Tuple[int, int]], Set[int]]:
    '''Parses the schematics to create: a list of number data (tuple of numbers and sets of 
    coordinates of adjacent fields, a set of coords adjacent to parts and a set of gear ratios'''
    width = len(schematics[0])
    height = len(schematics)

    numbers = []
    parts_coordinates = set()
    gear_candidates = set()
    gear_ratios = set()

    number_builder = ''
    adjacent_to_number = set()

    for i in range(width):
        for j in range(height):
            current = schematics[i][j]

            if current.isdigit():
                number_builder += current
                for coordinate in ADJACENTS:
                    adjacent_to_number.add((i + coordinate[0], j + coordinate[1]))

            else:
                if number_builder:
                    numbers.append((int(number_builder), adjacent_to_number))

                    number_builder = ''
                    adjacent_to_number = set()

                if current != EMPTY:
                    parts_coordinates.add((i, j))

                if current == GEAR:
                    gear_candidates.add((i, j))

    for gear in gear_candidates:
        adjacent_numbers = [number for number, adjacents in numbers if gear in adjacents]

        if len(adjacent_numbers) >= MINIMUM_ADJACENT_TO_GEAR:
            gear_ratios.add(reduce(mul, adjacent_numbers))

    return numbers, parts_coordinates, gear_ratios


TEST_DATA = '''467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..'''

print('Testing...')
nums, parts, gears = parse_schematics(build_schematics(TEST_DATA))
print('Part 1:', sum(num for num, adjacents in nums if adjacents & parts) == 4361)
print('Part 2:', sum(gears) == 467835)

with open('inp', mode='r', encoding='utf8') as inp:
    print('Solution...')
    data = inp.read()
    nums, parts, gears = parse_schematics(build_schematics(data))
    print('Part 1:', sum(num for num, adjacents in nums if adjacents & parts))
    print('Part 2:', sum(gears))
