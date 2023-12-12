print('Day 12 of Advent of Code!')


def parse_data(data):
    raw_data = []
    for line in data.splitlines():
        chars, numbers = line.split()
        numbers = [int(num) for num in numbers.split(',')]
        raw_data.append((chars, numbers))
    return raw_data


def count_hashes(line):
    counts = []
    series = ''
    for i in range(len(line)):
        current = line[i]
        if current == '#':
            series += current
        else:
            if series:
                counts.append(len(series))
                series = ''
    if series:
        counts.append(len(series))
    return counts


def generate_patterns(pattern, current_pattern='', index=0):
    result = []

    if index == len(pattern):
        result.append(current_pattern)
        return result

    if pattern[index] == '?':
        result.extend(generate_patterns(pattern, current_pattern + '#', index + 1))
        result.extend(generate_patterns(pattern, current_pattern + '.', index + 1))
    elif pattern[index] in '#.':
        result.extend(generate_patterns(pattern, current_pattern + pattern[index], index + 1))

    return result


def sum_arrangements(data):
    s = 0 
    for pattern, hashes in data:
        for variation in generate_patterns(pattern):
            if count_hashes(variation) == hashes:
                s += 1
    return s


TEST_DATA = '''???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1'''

print('Testing...')
print('Part 1:', sum_arrangements(parse_data(TEST_DATA)))

with open('inp', mode='r', encoding='utf-8') as inp:
    print('Solution...')
    actual_data = inp.read()
    print('Part 1:', sum_arrangements(parse_data(actual_data)))