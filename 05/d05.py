print('Day 5 of Advent of Code!')

def get_single_seeds(lines):
    return [int(seed) for seed in lines[0].split(': ')[1].split()]


def get_seed_ranges(lines):
    all_ranges = lines[0].split(': ')[1].split()
    seed_ranges = []
    for i in range(0, len(all_ranges)-1, 2):
        seed_from, seed_to = int(all_ranges[i]), int(all_ranges[i+1])
        seed_ranges.append((seed_from, seed_to))
    return seed_ranges


def get_map(lines, map_id):
    data = lines[map_id]
    map_of_ranges = {}
    for map_id, dataset in enumerate(data.split('\n')[1:]):
        map_of_ranges[map_id] = [int(number) for number in dataset.split()]
    return map_of_ranges


def get_maps(full_data):
    return [get_map(full_data, map_id) for map_id in range(1,8)]


def get_seed_range_id(seed, map_of_ranges):
    for range_id, data in map_of_ranges.items():
        _, source, length = data
        if source <= seed < source + length:
            return range_id
    return -1


def map_numbers(current, map_of_ranges):
    range_id = get_seed_range_id(current, map_of_ranges)
    if range_id == -1:
        return current

    destination, source, _ = map_of_ranges[range_id]
    delta = destination - source

    return current + delta


def find_smallest(full_data):
    seeds = get_single_seeds(full_data)
    all_maps = get_maps(full_data)
    minimum = -1

    for current in seeds:
        for sth_to_sth in all_maps:
            current = map_numbers(current, sth_to_sth)
        if minimum == -1 or current < minimum:
            minimum = current

    return minimum


def hacky_find_smallest_in_range(rng, all_maps, step):
    minimum = (-1, -1)
    for current in range(rng[0], rng[0]+rng[1], step):
        tested_seed = current
        for sth_to_sth in all_maps:
            current = map_numbers(current, sth_to_sth)
        if minimum[0] == -1 or current < minimum[0]:
            minimum = (current, tested_seed)
    return minimum


def hacky_hacky_find_smallest_in_ranges(full_data):
    seed_ranges = get_seed_ranges(full_data)
    all_maps = get_maps(full_data)
    minimum = -1

    step = 100_000_000
    stop_step = 10_000

    while step >= stop_step:
        for rng in seed_ranges:
            range_minimum = hacky_find_smallest_in_range(rng, all_maps, step)
            if minimum == -1 or range_minimum < minimum:
                minimum = range_minimum
        candidate_range = (minimum[1] - step, step * 10)
        seed_ranges = [candidate_range]
        step //= 10

    final_candidate = (seed_ranges[0][0] - step, step * 10)

    return hacky_find_smallest_in_range(final_candidate, all_maps, 1)[0]


TEST_DATA = '''seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4'''

print('Testing...')
test_maps = TEST_DATA.split('\n\n')
print('Part 1:', find_smallest(test_maps) == 35)

with open('inp', mode='r', encoding='utf-8') as inp:
    print('Solution...')

    actual_maps = inp.read().split('\n\n')
    print('Part 1:', find_smallest(actual_maps))
    print('Part 2:', hacky_hacky_find_smallest_in_ranges(actual_maps))
