import re
from collections import defaultdict, deque
from copy import deepcopy

'''Part 1 very strongly inspired by a solution posted by mtpink1:
https://www.reddit.com/r/adventofcode/comments/18o7014/comment/keha96f/?utm_source=reddit&utm_medium=web2x&context=3

My original solution wasn't using the height map and kept spitting out wrong (too high) results.'''

print('Day 22 of Advent of Code!')

class Brick:
    def __init__(self, coords) -> None:
        coords: tuple = coords
        self.xmin, self.ymin, self.zmin = coords[0]
        self.xmax, self.ymax, self.zmax = coords[1]
        self.bottom = min(self.zmin, self.zmax)
        self.top = max(self.zmin, self.zmax)


    def __repr__(self) -> str:
        return f'{self.xmin}, {self.ymin}, {self.zmin} -> {self.xmax}, {self.ymax}, {self.zmax}'


    def fields_on_bottom(self):
        fields = set()
        for x in range(self.xmin, self.xmax+1):
            for y in range(self.ymin, self.ymax+1):
                fields.add((x, y))
        return fields


def make_bricks(data):
    bricks = []
    for line in data.splitlines():
        numbers = re.findall(r'(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)', line)[0]
        start = [int(n) for n in numbers[:3]]
        end = [int(n) for n in numbers[3:]]
        bricks.append(Brick((start, end)))
    return bricks


def drop_bricks(data):
    bricks = make_bricks(data)

    bricks.sort(key=lambda b: b.bottom)

    height_map = defaultdict(lambda: (0, -1))
    supporting = defaultdict(set)
    supported_by = defaultdict(set)

    for i, brick in enumerate(bricks):
        max_height = 0 # we check from the floor up but will update this value for each sub-brick on the bottom of the main brick

        this_supported_by = set() # set of indexes of bricks supported by this

        for (x, y) in brick.fields_on_bottom():
            height, other_i = height_map[(x, y)]

            # scenario 1: in position (x, y) the height map tells us that something is higher than 0 (or later updated height)!
            # which means that whatever occupies (x, y) will support this brick
            # and we need to update the max_height to calculate the drop distance
            if height > max_height:
                max_height = height
                this_supported_by = {other_i}

            # scenario 2: in position (x, y) the height map tells us that something is exactly on the same height
            # this means that this brick has support from one more!
            elif height == max_height:
                this_supported_by.add(other_i)

        for other_i in this_supported_by:
            supporting[other_i].add(i)
            supported_by[i] = this_supported_by

        # calculate how much the brick can drop
        drop_distance = brick.bottom - max_height - 1

        # update the height map (without changing the brick object)
        # in position (x, y) the new top is initial top minus drop distance
        # and it is occupied by brick i
        for (x, y) in brick.fields_on_bottom():
            height_map[(x, y)] = (brick.top - drop_distance, i)

    redundant = 0

    for i, brick in enumerate(bricks):
        for supported_i in supporting[i]:
            if len(supported_by[supported_i]) == 1:
                break
        else:
            redundant += 1

    return redundant, supported_by, supporting


def simulate_all_falls(data):
    s = 0
    for idx in range(len(data.splitlines())):
        q = deque([idx])
        _, supported_by, supporting = drop_bricks(data)
        falls = 0
        while q:
            removed_brick = q.popleft()
            for supported_brick in supporting[removed_brick]:
                supported_by[supported_brick].remove(removed_brick)
                if not supported_by[supported_brick]:
                    falls += 1
                    q.append(supported_brick)
        s += falls
    return s


TEST_DATA = '''1,0,1~1,2,1
0,0,2~2,0,2
0,0,4~0,2,4
0,2,3~2,2,3
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9'''


print('Testing...')
print('Part 1:', drop_bricks(TEST_DATA)[0] == 5)
print('Part 2:', simulate_all_falls(TEST_DATA) == 7)

with open('inp', mode='r', encoding='utf-8') as inp:
    print('Solution...')
    actual_data = inp.read()
    print('Part 1:', drop_bricks(actual_data)[0])
    print('Part 2:', simulate_all_falls(actual_data))
