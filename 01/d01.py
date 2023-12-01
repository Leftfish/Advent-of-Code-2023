import re

print('Day 1 of Advent of Code!')


def get_values(line: str, part: int) -> int:
    digits = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 
            'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9'}

    if part == 1:
        values = [char for char in line if char.isdigit()]

    elif part == 2:
        values = []
        i, j = 0, 0
  
        while j < len(line):
            if line[j].isdigit():
                values.append(line[j])
            buffer = line[i:j+1]
            for k, v in digits.items():
                if k in buffer:
                    values.append(v)
                    i = j
            j += 1

    return int(values[0] + values[-1])


def get_values_alternative(line):
    digits = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 
            'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9'}
    regex = r'one|two|three|four|five|six|seven|eight|nine'

    first = re.findall(regex + '|\d', line)[0]
    last = re.findall(regex[::-1] + '|\d', line[::-1])[0][::-1]

    return int(''.join([token if token.isdigit() else digits[token] for token in [first, last]]))

test_data_1 = '''1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet'''

test_data_2 = '''two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen'''

print('Testing...')
print('Part 1:', sum(get_values(line, 1) for line in test_data_1.splitlines()) == 142)
print('Part 2:', sum(get_values(line, 2) for line in test_data_2.splitlines()) == 281)
print('Testing alternative option for part 2...')
print('Part 2:', sum(get_values_alternative(line) for line in test_data_2.splitlines()) == 281)

with open('inp', mode='r') as inp:
    print('Solution...')
    data = inp.readlines()
    print('Part 1:', sum(get_values(line, 1) for line in data))
    print('Part 2:', sum(get_values(line, 2) for line in data))
    print('And now part 2 with regex...')
    print('Part 2:', sum(get_values_alternative(line) for line in data))