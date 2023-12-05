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
    else:
        destination, source, _ = map_of_ranges[range_id]
        delta = destination - source
        updated = current + delta
        return updated

def find_smallest(full_data):
    seeds = get_single_seeds(full_data)
    all_maps = get_maps(full_data)
    minimum = -1
    for current in seeds:
        for sth_to_sth in all_maps:
            current = map_numbers(current, sth_to_sth)
        if minimum == -1 or current < minimum:
            minimum = current
    print(minimum)

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

def find_smallest_in_ranges(full_data):
    seed_ranges = get_seed_ranges(full_data)
    all_maps = get_maps(full_data)
    minimum = -1

    start = 3205462501 - 100
    rng = 1000
    
    for rng in [(start, 243224070)]:
    #for rng in seed_ranges:
        print('----------------')
        for current in range(rng[0], rng[0]+rng[1], 1):
            a = current
            for sth_to_sth in all_maps:
                current = map_numbers(current, sth_to_sth)
            if minimum == -1 or current < minimum:
                minimum = current
                print(f'{rng} ...ends at {current} from {a}')

find_smallest(test_maps)
#find_smallest_in_ranges(test_maps)

with open('inp', mode='r', encoding='utf-8') as inp:
    print('Solution...')

    actual_maps = inp.read().split('\n\n')
    find_smallest(actual_maps)
    find_smallest_in_ranges(actual_maps)