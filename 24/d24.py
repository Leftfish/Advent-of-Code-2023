from itertools import combinations

print('Day 24 of Advent of Code!')


def make_two_points(data):
    coords, delta = data.split(' @ ')
    x, y, _ = [int(d) for d in coords.split(',')]
    dx, dy, __ = [int(d) for d in delta.split(',')]
    return (x, y), (x+dx, y+dy), (dx, dy)


def find_intersection(this, other):
    x1, y1 = this[0]
    x2, y2 = this[1]
    x3, y3 = other[0]
    x4, y4 = other[1]

    denominator = (x1-x2) * (y3-y4) - (y1-y2) * (x3-x4)

    if denominator == 0:
        return None

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

TEST_DATA = '''19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3'''

print('Testing...')
lines = [make_two_points(ln) for ln in TEST_DATA.splitlines()]
test_pairs = combinations(lines, 2)
print('Part 1:', count_intersection(test_pairs, 7, 27) == 2)


with open('inp', mode='r', encoding='utf-8') as inp:
    print('Solution...')
    actual_data = inp.read()
    lines = [make_two_points(ln) for ln in actual_data.splitlines()]
    actual_pairs = combinations(lines, 2)
    print('Part 1:', count_intersection(actual_pairs, 200000000000000, 400000000000000))
