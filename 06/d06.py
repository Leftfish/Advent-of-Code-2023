import re
from math import ceil, floor, sqrt

print('Day 6 of Advent of Code!')


def parse_without_kerning(data):
    times, distances = data.split('\n')
    race_times = [int(race_time) for race_time in list(re.findall('\d+', times))]
    race_distances = [int(race_distance) for race_distance in list(re.findall('\d+', distances))]

    return zip(race_times, race_distances)


def solve_race(race):
    '''Solving (race_time - x) * x > max_distance for minimum and maximum integer solution.'''
    a = -1
    b = race[0]
    c = -race[1]
    delta = b**2 - 4 * a * c

    lo = (-b + sqrt(delta)) / 2 * a
    hi = (-b - sqrt(delta)) / 2 * a

    discrete_lo = ceil(lo) if ceil(lo) != lo else lo + 1
    discrete_hi = floor(hi) if floor(hi) != hi else hi - 1

    return int(discrete_hi - discrete_lo + 1)


def solve_multiple_races(data):
    races = parse_without_kerning(data)
    acc = 1
    for race in races:
        acc *= solve_race(race)
    return acc

TEST_DATA = '''Time:      7  15   30
Distance:  9  40  200'''

print('Testing...')
print(solve_multiple_races(TEST_DATA))

with open('inp', mode='r', encoding='utf-8') as inp:
    print('Solution...')
    actual_data = inp.read()
    print(solve_multiple_races(actual_data))

    