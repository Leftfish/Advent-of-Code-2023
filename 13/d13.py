from math import ceil

print('Day 13 of Advent of Code!')

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

def parse_data(raw_data):
    raw_patterns = raw_data.split('\n\n')
    return [pattern.splitlines() for pattern in raw_patterns]


def get_hashes(parsed_data):
    line_hashes = [hash(line) for line in parsed_data]

    col_hashes = []
    for j in range(len(parsed_data[0])):
        col = []
        for i in range(len(parsed_data)):
            col.append(parsed_data[i][j])
        col_hashes.append(hash("".join(col)))
    
    return line_hashes, col_hashes


def find_reflection(data):
    def is_identical(this, other, idx_to_hash):
        return idx_to_hash[this] == idx_to_hash[other]
    
    def helper(idx_to_hash):
        def idxs_in_range():
            return i >= 0 and j < len(idx_to_hash)
        
        i, j = 0, 1
        while True:
            if not is_identical(i, j, idx_to_hash):
                if j - i == 1:
                    j += 1
                i = j - 1
                if not idxs_in_range():
                    return 0
            elif is_identical(i, j, idx_to_hash):
                i -= 1
                j += 1
                if not idxs_in_range():
                    if idxs_in_range():
                        if is_identical(i, j, idx_to_hash): 
                            return 0
                        else: 
                            return ceil((i+j)/2)
                    else:
                        return ceil((i+j)/2)
    
            
    line_hashes, col_hashes = get_hashes(data)
    idx_to_hash_line = {idx: hsh for idx, hsh in enumerate(line_hashes)}
    idx_to_hash_cols = {idx: hsh for idx, hsh in enumerate(col_hashes)}

    line = helper(idx_to_hash_line) * 100
    cols = helper(idx_to_hash_cols)

    return line + cols


def score_mirrors(raw_data):
    total_score = 0
    for data in parse_data(raw_data):
        total_score += find_reflection(data)
    return total_score


print('Testing...')
print('Part 1:', score_mirrors(TEST_DATA) == 405)

with open('inp', mode='r', encoding='utf-8') as inp:
    print('Solution...')
    actual_data = inp.read()
    print('Part 1:', score_mirrors(actual_data))

# for part 2 to work - comparing hashes will not work. converting lines/cols to binary numbers and then bitwise ops, maybe?