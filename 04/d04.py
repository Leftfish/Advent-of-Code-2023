from typing import Dict
import re

print('Day 4 of Advent of Code!')


def parse_cards(lines: str) -> Dict[int, Dict[str, int]]:
    '''Makes a dictionary of cards with IDs as keys, storing how many numbers are winning
    and how many copies of each card the player has'''
    cards = {}
    for line in lines:
        card = {}
        first_half, second_half = line.split('|')
        id_and_winning = list(map(int, re.findall(r'\d+', first_half)))
        player_numbers = set(map(int, re.findall(r'\d+', second_half)))
        card_id, winning = int(id_and_winning[0]), set(id_and_winning[1:])
        matching = len(player_numbers & set(winning))

        card['matching'] = matching if matching >= 1 else 0
        card['quantity'] = 1
        card['makes_copies_of'] = [card_id + i for i in range(1, card['matching'] + 1)]

        cards[card_id] = card

    return cards


def make_copies(cards: Dict[int, Dict[str, int]]) -> Dict[int, Dict[str, int]]:
    '''Iterates over the cards and for each instance of each cards, generates the copies of cards
    with N subsequent ids where N is the number of winning (matching) numbers'''
    for card_id in cards:
        for _ in range(cards[card_id]['quantity']):
            for new_copy_id in cards[card_id]['makes_copies_of']:
                cards[new_copy_id]['quantity'] += 1
    return cards


def sum_powers(cards: Dict[int, Dict[str, int]]) -> int:
    total = 0
    for card_id in cards:
        power = cards[card_id]['matching'] - 1
        if power >= 0:
            total += 2 ** power
    return total


def sum_copies(cards: Dict[int, Dict[str, int]]) -> int:
    return sum([cards[card_id]['quantity'] for card_id in cards])


TEST_DATA = '''Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11'''

print('Testing...')
test_cards = parse_cards(TEST_DATA.splitlines())
print('Card powers:', sum_powers(test_cards) == 13)
print('Total copies:', sum_copies(make_copies(test_cards)) == 30)

with open('inp', mode='r', encoding='utf8') as inp:
    print('Solution...')
    data = inp.readlines()
    actual_cards = parse_cards(data)
    print('Card powers:', sum_powers(actual_cards))
    print('Total copies:', sum_copies(make_copies(actual_cards)))
