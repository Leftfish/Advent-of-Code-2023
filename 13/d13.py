from math import ceil

print('Day 13 of Advent of Code!')

def parse_data(raw_data):
    return [pattern.splitlines() for pattern in raw_data.split('\n\n')]


def get_hashes(parsed_data):
    '''Transforms lines and cols into hashes because I thought 
    it was easier. Must use something else for part 2.'''

    line_hashes = [hash(line) for line in parsed_data]

    col_hashes = []
    for j in range(len(parsed_data[0])):
        col = []
        for i in range(len(parsed_data)):
            col.append(parsed_data[i][j])
        col_hashes.append(hash("".join(col)))

    return line_hashes, col_hashes


def find_reflection(data):
    '''Find reflections by traversing columns and lines separately'''

    def traverse_pattern(idx_to_hash):
        '''Go from top to bottom or left to right. If you find neighboring 
        lines/cols that are the same, expand your search. If you keep finding 
        identical pairs when you reach the border of the pattern, this is your 
        range of mirror reflection. Then calculate the score.'''

        i, j = 0, 1
        while True:
            if idx_to_hash[i] != idx_to_hash[j]: # if no pair at indexes i and j, advance forward
                if j - i == 1: # necessary for edge cases in which we have four identical rows/cols
                    j += 1
                i = j - 1
                if not (i >= 0 and j < len(idx_to_hash)): # at border, no reflection tracked
                    return 0
            else: # if pair found at i and j, advance back and forward
                i -= 1
                j += 1
                if not (i >= 0 and j < len(idx_to_hash)): # at border, tracking a reflection
                    return ceil((i+j)/2)

    line_hashes, col_hashes = get_hashes(data)
    idx_to_hash_line = {idx: hsh for idx, hsh in enumerate(line_hashes)}
    idx_to_hash_cols = {idx: hsh for idx, hsh in enumerate(col_hashes)}

    line = traverse_pattern(idx_to_hash_line) * 100
    cols = traverse_pattern(idx_to_hash_cols)

    return line + cols


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
print('Part 1:', sum((find_reflection(data) for data in parse_data(TEST_DATA))) == 405)

with open('inp', mode='r', encoding='utf-8') as inp:
    print('Solution...')
    actual_data = inp.read()
    #print('Part 1:', sum((find_reflection(data) for data in parse_data(actual_data))))

# for part 2 to work - comparing hashes will not work. converting 
# lines/cols to binary numbers and then bitwise ops, maybe?
