print('Day 10 of Advent of Code!')

START = 'S'

VERTICAL = '|'
HORIZONTAL = '-'
NORTHEAST = 'L'
NORTHWEST = 'J'
SOUTHWEST = '7'
SOUTHEAST = 'F'
GROUND = '.'

TOP, DOWN, LEFT, RIGHT = (-1, 0), (1, 0), (0, -1), (0, 1)

MOVES = {VERTICAL: {TOP: (VERTICAL, SOUTHEAST, SOUTHWEST, START),
                    DOWN: (VERTICAL, NORTHEAST, NORTHWEST, START),},
         HORIZONTAL: {LEFT: (HORIZONTAL, NORTHEAST, SOUTHEAST, START),
                      RIGHT: (HORIZONTAL, NORTHWEST, SOUTHWEST, START)},
         NORTHEAST: {TOP: (VERTICAL, SOUTHWEST, SOUTHEAST, START),
                     RIGHT: (HORIZONTAL, SOUTHWEST, NORTHWEST, START)},
         NORTHWEST: {TOP: (VERTICAL, SOUTHWEST, SOUTHEAST, START),
                     LEFT: (HORIZONTAL, SOUTHEAST, NORTHEAST, START)},
         SOUTHWEST: {DOWN: (VERTICAL, NORTHWEST, NORTHEAST, START),
                     LEFT: (HORIZONTAL, SOUTHEAST, NORTHEAST, START)},
         SOUTHEAST: {DOWN: (VERTICAL, NORTHWEST, NORTHEAST, START),
                     RIGHT: (HORIZONTAL, SOUTHWEST, NORTHWEST, START)},
         START: {TOP: (VERTICAL, SOUTHWEST, SOUTHEAST),
                 LEFT: (HORIZONTAL, SOUTHEAST, NORTHEAST),
                 DOWN: (VERTICAL, NORTHWEST, NORTHEAST),
                 RIGHT: (HORIZONTAL, SOUTHWEST, NORTHWEST)}}


class Pipes:
    def __init__(self, data) -> None:
        self.schematic = [list(line) for line in data.splitlines()]
        self.width = len(self.schematic[0])
        self.length = len(self.schematic)
        self.start = self.__find_start()


    def __find_start(self):
        for i in range(self.length):
            for j in range(self.width):
                if self.schematic[i][j] == START:
                    return (i, j)
        return (0, 0)


    def __repr__(self) -> str:
        s = ''
        for line in self.schematic:
            s += "".join(line)
            s += '\n'
        return s


class Animal:
    def __init__(self, i, j, pipes) -> None:
        self.i = i
        self.j = j
        self.loop = 0
        self.steps = 0
        self.visited = set()
        self.visited.add((i, j))
        self.pipes = pipes


    def __repr__(self) -> str:
        return f'i: {self.i}, j: {self.j}'


    def get_legal_moves(self):
        current = self.pipes.schematic[self.i][self.j]
        candidates = []

        if TOP in MOVES[current] and 0 < self.i and\
            self.pipes.schematic[self.i-1][self.j] in MOVES[current][TOP]:
            candidates.append((self.i-1, self.j))

        if DOWN in MOVES[current] and self.i < self.pipes.width -2 and\
            self.pipes.schematic[self.i+1][self.j] in MOVES[current][DOWN]:
            candidates.append((self.i+1, self.j))

        if LEFT in MOVES[current] and 0 < self.j and \
            self.pipes.schematic[self.i][self.j-1] in MOVES[current][LEFT]:
            candidates.append((self.i, self.j-1))

        if RIGHT in MOVES[current] and self.j < self.pipes.length -2 and \
            self.pipes.schematic[self.i][self.j+1] in MOVES[current][RIGHT]:
            candidates.append((self.i, self.j+1))
        return candidates


    def get_next_move(self):
        candidate_moves = self.get_legal_moves()
        for move in candidate_moves:
            if move not in self.visited or self.steps > 1 \
                and self.pipes.schematic[move[0]][move[1]] == START:
                return move

    def move(self):
        next_position = self.get_next_move()
        self.i, self.j = next_position
        self.visited.add(next_position)
        self.update_steps()

    def update_steps(self):
        self.steps += 1
        if (self.i, self.j) == self.pipes.start:
            self.loop = self.steps // 2

def move_in_loop(animal):
    while animal.get_next_move():
        animal.move()

TEST_DATA = '''-L|F7
7S-7|
L|7||
-L-J|
L|-JF'''

print('Testing...')
test_pipes = Pipes(TEST_DATA)
lab_rat = Animal(*test_pipes.start, test_pipes)
move_in_loop(lab_rat)
print('Part 1:', lab_rat.loop == 4)

with open('inp', mode='r', encoding='utf-8') as inp:
    print('Solution...')
    actual_data = inp.read()
    actual_pipes = Pipes(actual_data)
    proper_rat = Animal(*actual_pipes.start, actual_pipes)
    move_in_loop(proper_rat)
    print('Part 1:', proper_rat.loop)
