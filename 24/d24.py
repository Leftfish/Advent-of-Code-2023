from itertools import combinations, cycle

print('Day 24 of Advent of Code!')


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
        return None # coincident lines or parallel lines; puzzle rules make the former the only possibility

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
    #actual_pairs = combinations(lines, 2)
    #print('Part 1:', count_intersection(actual_pairs, 200000000000000, 400000000000000))


'''
1. sparsuj
2. zbierz dane  w zbiorze

DLA KAŻDEGO ZESTAWU OFFSETÓW:

1. iteruj przez dane
    - każdemu dodaj offset
    - i zrób z nich wektor
    - i dodaj do zbioru

2. idź przez zbiór
    - znajdź intersection x i y każdemu z każdym
    - dodaj intersection do zbioru
    - jeśli zbiór osiągnie rozmiar > 1: przerwij
    - jeśli skończysz iść przez zbiór: dodaj intersekcję do zbioru

3. idź przez zbiór intersekcji
    - dla każdego odcinka policz t, w którym by tam był; potem na tej podstawie oblicz z
    - jak tylko z okaże się inne (rozmiar zbioru koordów "z" > 1) - przerwij
    - jak skończyłeś, to tutaj
'''

def parse_coordinates(data):
    coords, delta = data.split(' @ ')
    x, y, z = [int(d) for d in coords.split(',')]
    dx, dy, dz = [int(d) for d in delta.split(',')]
    return (x, y, z), (dx, dy, dz)

def apply_xy_offset(stones, offset):
    offset_stones = []
    for stone in stones:
        x, y, z = stone[0]
        dx, dy, dz = stone[1]
        dx -= offset[0]
        dy -= offset[1]
        dz -= offset[2]
        new_stone = ((x, y, z), (x + dx, y + dy, z + dz))
        offset_stones.append(new_stone)
    return offset_stones

def check_xy_intersections(stones):
    succesful_offsets = set()
    for x in range(MIN_X,MAX_X+1,1):
        for y in range(MIN_Y,MAX_Y+1,1):
            for z in range(MIN_Z,MAX_Z+1,1):
                offset = (x,y,z)
                intersections = check_offset(stones, offset)
                if intersections:
                    succesful_offsets.add((offset, intersections.pop()))
    return succesful_offsets

def check_zs(offset, stones):
    new_stones = apply_xy_offset(stones, offset[0])
    intersection = offset[1]
    xs = intersection[0]
    times = set()
    for stone in new_stones:
        x = stone[0][0]
        dx = stone[1][0] - x
        z = stone[0][2]
        dz = stone[1][2] - z
        t = (xs - x) / dx
        zs = z + t * dz

        if times and zs not in times:
            return set()
        else:
            times.add(zs)
    return times

data = TEST_DATA.splitlines()
data = actual_data.splitlines()
stones = [parse_coordinates(stone) for stone in data]

from collections import deque

def generate_xy_offsets(MAX_NUM):
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
                
                if all(-MAX_NUM <= x <= MAX_NUM for x in new_tuple):
                    if new_tuple not in visited:
                        visited.add(new_tuple)
                        queue.append(new_tuple)

def generate_z_offsets(MAX_NUM):
    visited = set()
    queue = deque([0])
    visited.add(0)
    
    while queue:
        current = queue.popleft()  
        yield current
        
        for i in range(2):
            for delta in [-1, 1]:
                new_offset = current + delta
                
                if -MAX_NUM <= new_offset <= MAX_NUM and new_offset not in visited:
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
                #print(f'UNABLE: {new_intersection} not in {intersections}')
                return set()
    return intersections

MAX_NUM = 500
for i, offset in enumerate(generate_xy_offsets(MAX_NUM)):
    vectors = apply_xy_offset(stones, offset) # apply the offset of dX and dY to each stone -> get list of updates 2D vectors
    pairs = combinations(vectors, 2) # pair each stone with other stones
    
    intersections_2d = check_offset(pairs)
    
    if intersections_2d:
        print(intersections_2d, offset)
        break
xs, ys = intersections_2d.pop()

print('int', xs, ys, offset)

def check_z(dz, vectors):
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
            #print('new z', final_z)
        elif final_z == calculated_z:
            pass
            #print('still going', calculated_z)
        else:
            #print('stop',calculated_z)
            return None
    return final_z

for dz in generate_z_offsets(MAX_NUM):
    zs = check_z(dz, vectors)
    if zs:
        print(xs, ys, zs, sum((xs, ys, zs)))
        break

'''
total = None
for offset in check_xy_intersections(stones):
    z = check_zs(offset, stones)
    if z:
        total = [*offset[1], z.pop()]
        print(total, sum(total))
        break
if not total:
    print("No solution")


# potrzebne optymalizacje
# zacznij od przechodzenia przez same X, Y, potem dopiero Z ???
# i sprawdz te wzory
# https://old.reddit.com/r/adventofcode/comments/18pptor/2023_day_24_part_2java_is_there_a_trick_for_this/keps780/?context=3
# https://www.reddit.com/r/adventofcode/comments/18pnycy/comment/kfjfifl/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
# bruteforce w increasing magnitude
#


# candidate_coords = lambda limit: [c for row in zip([n for n in range(limit+1)], [-n for n in range(limit+1)]) for c in row]

def get_2d(stones):
    flat_intersects = set()
    for x in range(MIN_X,MAX_X+1,1):
        for y in range(MIN_Y,MAX_Y+1,1):
            offset = (x,y,0)
            
            if x % 100 == 0: print('checking', offset)
            intersections = check_offset(stones, offset)
            if intersections:
                flat_intersects.add((offset, intersections.pop()))
                continue
            else:
                #print('fail')
                continue
    return flat_intersects

MIN_X, MAX_X = -500, 500
MIN_Y, MAX_Y = -500, 500
MIN_Z, MAX_Z = -5, 5

#data = TEST_DATA.splitlines()
data = actual_data.splitlines()
stones = [parse_coordinates(stone) for stone in data]
#print(get_2d(stones))
#{((192, 210, 0), (187016878804004.0, 175507140888229.0))}


offset = ((192, 210, 0), (187016878804004.0, 175507140888229.0))

three_d_offsets = [((192, 210, z), (187016878804004.0, 175507140888229.0)) for z in range(-500, 500)]

for offset in three_d_offsets:
    new_stones = apply_xy_offset(stones, offset[0])
    intersection = offset[1]
    xs = intersection[0]
    times = set()
    for stone in new_stones:
        x = stone[0][0]
        dx = stone[1][0] - x
        z = stone[0][2]
        dz = stone[1][2] - z
        t = (xs - x) / dx
        zs = z + t * dz

        if times and zs not in times:
            break
        else:
            times.add(zs)
            print(times)
'''