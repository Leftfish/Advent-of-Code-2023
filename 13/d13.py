print('Day 13 of Advent of Code!')

def parse_data(raw_data):
    '''Parses input string into list of lists'''

    return [pattern.splitlines() for pattern in raw_data.split('\n\n')]


def get_signatures(parsed_data):
    '''Transforms lines and cols into lists of binary digits.'''

    line_signatures = []
    for line in parsed_data:
        signature = [1 if char == '#' else 0 for char in line]
        line_signatures.append(signature)

    col_signatures = []
    for j in range(len(parsed_data[0])):
        signature = []
        for i in range(len(parsed_data)):
            char = parsed_data[i][j]
            signature.append(1 if char == '#' else 0)
        col_signatures.append(signature)
    return line_signatures, col_signatures


def compare_signatures(this, other):
    '''Finds indices where signatures of lines or columns diverge'''
    differences = []
    for idx, pair in enumerate(zip(this, other)):
        if pair[0] != pair[1]:
            differences.append(idx)
    return differences


def find_reflections(signatures):
    '''Starts from pairs of neighbouring lines/cols and goes outward
    until the border. If sum of differing chars == 0: part 1 reflection.
    If sum of differing chars == 1: part 2 reflection'''
    results = [0 ,0]
    starts = [(n, n+1) for n in range(len(signatures)-1)]
    for idx, start in enumerate(starts):
        i, j = start
        sum_of_diffs = 0
        while i >= 0 and j <= len(signatures)-1:
            sum_of_diffs += len(compare_signatures(signatures[i], signatures[j]))
            i -= 1
            j += 1
        if sum_of_diffs == 0:
            results[0] = idx+1
        if sum_of_diffs == 1:
            results[1] = idx+1
    return results


def check_mirror(data):
    '''Returns a tuple of lists: (ln, ls), (cn, cs)
    l: lines
    c: columns
    n: no smudges
    s: with smudges'''
    line_signatures, col_signatures = get_signatures(data)
    return find_reflections(line_signatures), find_reflections(col_signatures)


def find_symmetries(data):
    '''Sums the results for part 1 and part 2'''
    without_smudges, with_smudges = 0, 0
    for mirror in data:
        lines, cols = check_mirror(mirror)
        without_smudges += (100 * lines[0] + cols[0])
        with_smudges += (100 * lines[1] + cols[1])
    return without_smudges, with_smudges


TEST_DATA = '''#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#. 

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#'''

print('Testing...')
p1, p2 = find_symmetries(parse_data(TEST_DATA))
print('Part 1:', p1 == 405)
print('Part 2:', p2 == 400)


with open('inp', mode='r', encoding='utf-8') as inp:
    print('Solution...')
    actual_data = inp.read()
    p1, p2 = find_symmetries(parse_data(actual_data))
    print('Part 1:', p1)
    print('Part 2:', p2)
