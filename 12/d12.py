import functools

print('Day 12 of Advent of Code!')

### wouldn't have made it without a great tutorial by StaticMoose
### https://www.reddit.com/r/adventofcode/comments/18hbbxe/2023_day_12python_stepbystep_tutorial_with_bonus/


def parse_data(data, repetitions):
    raw_data = []
    for line in data.splitlines():
        raw_chars, raw_numbers = line.split()
        chars = ''
        numbers = []
        for _ in range(repetitions):
            chars += raw_chars
            chars += '?'
            numbers.extend((int(num) for num in raw_numbers.split(',')))
        raw_data.append((chars[:-1], tuple(numbers)))
    return raw_data


@functools.cache
def calculate(chars, numbers):
    def pound():
        if chars[:nxt_grp].count('?') + chars[:nxt_grp].count('#') != nxt_grp:
            return 0

        if len(chars) == nxt_grp:
            return len(numbers) == 1

        if chars[nxt_grp] in '?.':
            return calculate(chars[nxt_grp+1:], numbers[1:])

        return 0

    def dot():
        return calculate(chars[1:], numbers)

    if not numbers:
        return '#' not in chars

    if not chars:
        return 0

    nxt_grp = numbers[0]

    if chars[0] == '#':
        return pound()

    elif chars[0] == '.':
        return dot()

    elif chars[0] == '?':
        return pound() + dot()


def sum_arrangements(data):
    return sum((calculate(chars, numbers) for chars, numbers in data))


TEST_DATA = '''???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1'''

print('Testing...')
print('Part 1:', sum_arrangements(parse_data(TEST_DATA, 1)) == 21)
print('Part 2:', sum_arrangements(parse_data(TEST_DATA, 5)) == 525152)

with open('inp', mode='r', encoding='utf-8') as inp:
    print('Solution...')
    actual_data = inp.read()
    print('Part 1:', sum_arrangements(parse_data(actual_data, 1)))
    print('Part 2:', sum_arrangements(parse_data(actual_data, 5)))
