from collections import defaultdict
from typing import Tuple
from itertools import chain 

print('Day 2 of Advent of Code!')

test_data = '''Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green'''

def parse_game(line: str) -> Tuple[int, dict]:
    game, choices = line.split(': ')
    game_id = int(game.split()[1])
    
    cube_sets = list(chain.from_iterable([cube_set.split(', ') for cube_set in choices.split('; ')]))
    cube_counter = defaultdict(int)

    for cube in cube_sets:
        number, color = cube.split()
        number = int(number)
        if number > cube_counter[color]:
            cube_counter[color] = number

    return game_id, cube_counter


def check_games(data, red, green, blue):
    possible_games = []
    for game in data:
        game_id, cube_counter = parse_game(game)
        checker = all((cube_counter['red'] <= red, cube_counter['green'] <= green, cube_counter['blue'] <= blue))
        
        if checker:
            possible_games.append(game_id)

    return sum(possible_games)

print('Testing...')
print('Part 1:', check_games(test_data.splitlines(), red=12, green=13, blue=14) == 8)

with open('inp', mode='r') as inp:
    print('Solution...')
    data = inp.readlines()
    print('Part 1:', check_games(data, red=12, green=13, blue=14))
