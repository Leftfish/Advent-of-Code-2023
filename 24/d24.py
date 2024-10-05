from itertools import combinations
from collections import deque

print('Day 24 of Advent of Code!')

# Part 1 begins, written in December 2023

def make_two_points(data):
    coords, delta = data.split(' @ ')
    x, y, _ = [int(d) for d in coords.split(',')]
    dx, dy, __ = [int(d) for d in delta.split(',')]
    return (x, y), (x+dx, y+dy), (dx, dy)


def find_intersection(this, other):
    x1, y1 = this[0][0], this[0][1]
    x2, y2 = this[1][0], this[1][1]
    x3, y3 = other[0][0], other[0][1]
    x4, y4 = other[1][0], other[1][1]

    denominator = (x1-x2) * (y3-y4) - (y1-y2) * (x3-x4)

    if denominator == 0:
        return None
        # coincident lines or parallel lines; puzzle rules make the former the only possibility

    px_numerator = (x1*y2 - y1*x2)*(x3-x4) - (x1-x2)*(x3*y4-y3*x4)
    py_numerator = (x1*y2 - y1*x2)*(y3-y4) - (y1-y2)*(x3*y4-y3*x4)

    px = px_numerator/denominator
    py = py_numerator/denominator

    return (px, py)


def count_intersection(pairs, mn, mx):
    count = 0
    for pair in pairs:
        intersection = find_intersection(pair[0], pair[1])
        if intersection:
            x, y = intersection
            if mn <= x <= mx and mn <= y <= mx:
                this_x, othr_x = pair[0][0][0], pair[1][0][0]
                this_growing = pair[0][2][0] >= 0
                othr_growing = pair[1][2][0] >= 0
                this_future, othr_future = False, False

                if not this_growing and x < this_x or this_growing and x >= this_x:
                    this_future = True
                if not othr_growing and x < othr_x or othr_growing and x >= othr_x:
                    othr_future = True

                if this_future and othr_future:
                    count += 1
    return count

# Part 2 begins, written 10 months after part 1

def parse_coordinates(data):
    coords, delta = data.split(' @ ')
    x, y, z = [int(d) for d in coords.split(',')]
    dx, dy, dz = [int(d) for d in delta.split(',')]
    return (x, y, z), (dx, dy, dz)


def generate_xy_offsets(max_num):
    visited = set()
    queue = deque([(0, 0)])
    visited.add((0, 0))

    while queue:
        current_tuple = queue.popleft()
        yield current_tuple

        for i in range(2):
            for delta in [-1, 1]:
                new_tuple = list(current_tuple)
                new_tuple[i] += delta
                new_tuple = tuple(new_tuple)

                if all(-max_num <= x <= max_num for x in new_tuple):
                    if new_tuple not in visited:
                        visited.add(new_tuple)
                        queue.append(new_tuple)


def generate_z_offsets(max_num):
    visited = set()
    queue = deque([0])
    visited.add(0)

    while queue:
        current = queue.popleft()
        yield current

        for _ in range(2):
            for delta in [-1, 1]:
                new_offset = current + delta

                if -max_num <= new_offset <= max_num and new_offset not in visited:
                    visited.add(new_offset)
                    queue.append(new_offset)


def apply_xy_offset(stones, offset):
    offset_stones = []
    for stone in stones:
        x, y, z = stone[0]
        dx, dy, dz = stone[1]
        dx -= offset[0]
        dy -= offset[1]
        new_stone = ((x, y, z), (x + dx, y + dy, z + dz))
        offset_stones.append(new_stone)
    return offset_stones


def check_offset(pairs):
    intersections = set()
    for pair in pairs:
        if not intersections:
            intersections.add(find_intersection(*pair))
        else:
            new_intersection = find_intersection(*pair)
            if new_intersection not in intersections and new_intersection is not None:
                return set()
    return intersections


def get_2d_intersection(stones, max_num):
    for offset in generate_xy_offsets(max_num):
        # apply the offset of dX and dY to each stone -> get list of updates 2D vectors
        vectors = apply_xy_offset(stones, offset)
        # pair each stone with other stones
        pairs = combinations(vectors, 2)
        # find 2d intersections first
        intersections_2d = check_offset(pairs)
        # if found, return (X, Y) and the updates vectors for stones
        if intersections_2d:
            return intersections_2d, vectors


def find_final_z_position(dz, vectors):
    # see if stones can be in the same Z at the moment of X, Y intersection
    final_z = None
    for stone in vectors:
        x = stone[0][0]
        dx = stone[1][0] - x
        z = stone[0][2]
        offset_dz = stone[1][2] - stone[0][2] - dz

        if dx == 0:
            continue

        t = (xs - x) / dx
        calculated_z = z + offset_dz * t

        if final_z is None:
            final_z = calculated_z
        elif final_z != calculated_z:
            return None
    return final_z


def get_zs(vectors, max_num):
    # check where the Z-start must be for the Z-intersection
    for dz in generate_z_offsets(max_num):
        z_start = find_final_z_position(dz, vectors)
        if z_start:
            return z_start

TEST_DATA = '''19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3'''

MAX_NUM = 500

print('Testing...')
lines = [make_two_points(ln) for ln in TEST_DATA.splitlines()]
test_pairs = combinations(lines, 2)
print('Part 1:', count_intersection(test_pairs, 7, 27) == 2)
hailstones = [parse_coordinates(stone) for stone in TEST_DATA.splitlines()]
candidate_intersections, hailstone_vectors = get_2d_intersection(hailstones, MAX_NUM)
xs, ys = candidate_intersections.pop()
zs = get_zs(hailstone_vectors, MAX_NUM)
print('Part 2:', int(xs + ys + zs) == 47)

with open('inp', mode='r', encoding='utf-8') as inp:
    print('Solution...')
    actual_data = inp.read()
    lines = [make_two_points(ln) for ln in actual_data.splitlines()]
    actual_pairs = combinations(lines, 2)
    print('Part 1:', count_intersection(actual_pairs, 200000000000000, 400000000000000))
    hailstones = [parse_coordinates(stone) for stone in actual_data.splitlines()]
    candidate_intersections, hailstone_vectors = get_2d_intersection(hailstones, MAX_NUM)
    xs, ys = candidate_intersections.pop()
    zs = get_zs(hailstone_vectors, MAX_NUM)
    print('Part 2:', int(xs + ys + zs))
