from collections import defaultdict, deque
from enum import Enum
from itertools import cycle

print('Day 16 of Advent of Code!')


class Dirs(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


class Fields(Enum):
    EMPTY = '.'
    MIRROR_RIGHT = '\\'
    MIRROR_LEFT = '/'
    SPLITTER_HORIZONTAL = '-'
    SPLITTER_VERTICAL = '|'


class Beam:
    def __init__(self, x=0, y=0, direction=Dirs.RIGHT):
        self.x = x
        self.y = y
        self.directions = cycle([Dirs.RIGHT, Dirs.DOWN, Dirs.LEFT, Dirs.UP])

        current_direction = next(self.directions)
        while current_direction != direction:
            current_direction = next(self.directions)
        self.direction = current_direction

    def turn_right(self):
        self.direction = next(self.directions)

    def turn_left(self):
        for _ in range(3):
            self.direction = next(self.directions)

    def step(self):
        self.x += self.direction.value[0]
        self.y += self.direction.value[1]

    def __repr__(self):
        return f'x:{self.x}, y:{self.y}, {self.direction}'


def evaluate_field(beam, q, space):
    field = space[beam.x][beam.y]

    if field == Fields.EMPTY.value or \
        field == Fields.SPLITTER_VERTICAL.value and beam.direction in (Dirs.UP, Dirs.DOWN) or \
        field == Fields.SPLITTER_HORIZONTAL.value and beam.direction in (Dirs.LEFT, Dirs.RIGHT):
        q.appendleft(beam)
    elif field == Fields.MIRROR_LEFT.value and beam.direction in (Dirs.RIGHT, Dirs.LEFT) or \
            field == Fields.MIRROR_RIGHT.value and beam.direction in (Dirs.UP, Dirs.DOWN):
        beam.turn_left()
        q.appendleft(beam)
    elif field == Fields.MIRROR_LEFT.value and beam.direction in (Dirs.UP, Dirs.DOWN) or \
            field == Fields.MIRROR_RIGHT.value and beam.direction in (Dirs.RIGHT, Dirs.LEFT):
        beam.turn_right()
        q.appendleft(beam)
    elif field == Fields.SPLITTER_HORIZONTAL.value and beam.direction in (Dirs.UP, Dirs.DOWN):
        new_beam = Beam(x=beam.x, y=beam.y, direction=beam.direction)
        beam.turn_left()
        new_beam.turn_right()
        q.appendleft(beam)
        q.append(new_beam)
    elif field == Fields.SPLITTER_VERTICAL.value and beam.direction in (Dirs.RIGHT, Dirs.LEFT):
        new_beam = Beam(x=beam.x, y=beam.y, direction=beam.direction)
        beam.turn_left()
        new_beam.turn_right()
        q.appendleft(beam)
        q.append(new_beam)
    return q


def run_beams(start_x, start_y, start_dir, space):
    max_x = len(space) - 1
    max_y = len(space[0]) - 1
    first_beam = Beam(start_x, start_y, start_dir)

    q = deque([first_beam])

    visited = defaultdict(list)
    visited[(first_beam.x, first_beam.y)].append(first_beam.direction)
    beam = q.popleft()
    
    # turn and split if necessary when the first field is a mirror or splitter
    q = evaluate_field(beam, q, space)

    while q:
        beam = q.popleft()

        # we are facing the edge of the map, no further movement
        if beam.x == 0 and beam.direction == Dirs.UP \
            or beam.x == max_x and beam.direction == Dirs.DOWN \
            or beam.y == 0 and beam.direction == Dirs.LEFT \
            or beam.y == max_y and beam.direction == Dirs.RIGHT:
            continue

        beam.step()
        current_position = (beam.x, beam.y)

        # we have already been here facing the same direction
        if beam.direction in visited[current_position]:
            continue
        
        # add to visited, then turn and split if necessary
        visited[current_position].append(beam.direction)
        q = evaluate_field(beam, q, space)    

    return len(visited)


def run_all_positions(space):
    max_x = len(space)
    max_y = len(space[0])

    down = max((run_beams(x, y, Dirs.DOWN, space) for x, y in [(0, y) for y in range(max_y)]))
    up = max((run_beams(x, y, Dirs.UP, space) for x, y in [(max_x-1, y) for y in range(max_y)]))
    right = max((run_beams(x, y, Dirs.RIGHT, space) for x, y in [(x, 0) for x in range(max_x)]))
    left = max((run_beams(x, y, Dirs.LEFT, space) for x, y in [(x, max_y-1) for x in range(max_x)]))

    return max((down, up, right, left))


TEST_DATA = r'''.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....'''


print('Testing...')
test_space = [list(line) for line in TEST_DATA.splitlines()]
print('Part 1:', run_beams(0, 0, Dirs.RIGHT, test_space) == 46)
print('Part 2:', run_all_positions(test_space) == 51)

with open('inp', mode='r', encoding='utf-8') as inp:
    print('Solution...')
    actual_data = inp.read()
    actual_space = [list(line) for line in actual_data.splitlines()]
    print('Part 1:', run_beams(0, 0, Dirs.RIGHT, actual_space))
    print('Part 2:', run_all_positions(actual_space))
