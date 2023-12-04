import re

print('Day 4 of Advent of Code!')

TEST_DATA = '''Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11'''

lines = TEST_DATA.splitlines()

def part1(lines):
    sum = 0
    for line in lines:
        winning, has = line.split('|')
        winning = list(map(int, re.findall(r'\d+', winning)))[1:]
        player_numbers = set(map(int, re.findall(r'\d+', has)))

        power = len(player_numbers & set(winning)) - 1
        
        if power >= 0:
            sum += 2 ** power
    print(sum)



print('Testing...')
part1(lines)

with open('inp', mode='r', encoding='utf8') as inp:
    print('Solution...')
    data = inp.readlines()
    part1(data)