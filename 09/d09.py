from collections import deque

print('Day 9 of Advent of Code!')


def get_sequences(data):
    return [deque([int(val) for val in line.split()]) for line in data.splitlines()]


def update_sequence(sequence):
    updated = [sequence]
    while any(sequence):
        sequence = deque([sequence[i+1] - sequence[i] for i in range(0, len(sequence)-1)])
        updated.append(sequence)
    return updated


def extrapolate(updated_sequences):
    for i in range(len(updated_sequences)-1, 0, -1):
        current, nxt = updated_sequences[i], updated_sequences[i-1]
        nxt.append(nxt[-1] + current[-1])
        nxt.appendleft(nxt[0] - current[0])
    return updated_sequences[0][0], updated_sequences[0][-1]


TEST_DATA = '''0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45'''

print('Testing...')
extrapolations = [extrapolate(update_sequence(sq)) for sq in get_sequences(TEST_DATA)]
print('Part 1:', sum((extrapolation[1] for extrapolation in extrapolations)) == 114)
print('Part 2:', sum((extrapolation[0] for extrapolation in extrapolations)) == 2)

with open('inp', mode='r', encoding='utf-8') as inp:
    print('Solution...')
    actual_data = inp.read()
    extrapolations = [extrapolate(update_sequence(sq)) for sq in get_sequences(actual_data)]
    print('Part 1:', sum((extrapolation[1] for extrapolation in extrapolations)))
    print('Part 2:', sum((extrapolation[0] for extrapolation in extrapolations)))
