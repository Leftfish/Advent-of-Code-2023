import re

print('Day 15 of Advent of Code!')


def apply_hash(sequence):
    current = 0
    for char in sequence:
        current += ord(char)
        current *= 17
        current %= 256
    return current


def parse_command(sequence):
    regex = r'(\w+)([-=])(\d*)'
    label, operation, focal_length = re.findall(regex, sequence)[0]
    return label, apply_hash(label), operation, focal_length


def swap_boxes(boxes, sequences):
    for command in sequences:
        label, box, operation, focal_length = parse_command(command)
        if operation == '-':
            for lens in boxes[box]:
                if label == lens[0]:
                    boxes[box].remove(lens)
        elif operation == '=':
            swap = False
            for lens in boxes[box]:
                if label == lens[0]:
                    lens[1] = int(focal_length)
                    swap = True
            if not swap:
                boxes[box].append([label, int(focal_length)])
    return boxes


def score_lenses(boxes):
    total = 0
    for box in boxes:
        for idx, lens in enumerate(boxes[box], 1):
            lens_score = (1 + box) * idx * lens[1]
            total += lens_score
    return total


TEST_DATA = 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'

print('Testing...')
test_sequences = TEST_DATA.split(',')
test_boxes = swap_boxes({n: [] for n in range(256)}, test_sequences)
print('Part 1:', (sum(apply_hash(seq) for seq in test_sequences)) == 1320)
print('Part 2:', score_lenses(test_boxes) == 145)

with open('inp', mode='r', encoding='utf-8') as inp:
    print('Solution...')
    actual_data = inp.read()
    actual_sequences = actual_data.split(',')
    actual_boxes = swap_boxes({n: [] for n in range(256)}, actual_sequences)
    print('Part 1:', (sum(apply_hash(seq) for seq in actual_sequences)))
    print('Part 2:', score_lenses(actual_boxes))
