from collections import Counter

print('Day 7 of Advent of Code!')

CARDS = 'AKQJT98765432'
CARDS_JOKER = 'AKQT98765432J'
CARD_POINTS = range(len(CARDS), 0, -1)
JOKER = 'J'
STANDARD_SCORES = dict(zip(CARDS, CARD_POINTS))
JOKER_SCORES = dict(zip(CARDS_JOKER, CARD_POINTS))

FIVE_OF_A_KIND = 7
FOUR_OF_A_KIND = 6
FULL_HOUSE = 5
THREE = 4
TWO_PAIRS = 3
PAIR = 2
HIGH_CARD = 1


class Hand:
    def __init__(self, cards_in_hand, joker):
        self.cards = cards_in_hand
        if not joker:
            self.score = [self.__score_hand()] + [STANDARD_SCORES[c] for c in self.cards]
        else:
            self.score = [self.__score_hand_joker()] + [JOKER_SCORES[c] for c in self.cards]

    def __repr__(self):
        return f'{self.cards} [{self.score}]'

    def __lt__(self, other):
        for score_self, score_other in zip(self.score, other.score):
            if score_self < score_other:
                return True
            elif score_self > score_other:
                return False
            else:
                continue

    def __hash__(self) -> int:
        return hash(str(self))

    def __score_hand(self):
        card_count = Counter(self.cards)
        values = card_count.values()

        if max(values) == 5:
            # AAAAA
            return FIVE_OF_A_KIND
        elif max(values) == 4:
            # AAAAQ
            return FOUR_OF_A_KIND
        elif max(values) == 3 and len(card_count) == 2:
            # AAAQQ
            return FULL_HOUSE
        elif max(values) == 3 and len(card_count) == 3:
            # AAAQ2
            return THREE
        elif max(values) == 2 and len(card_count) == 3:
            # AAKK2
            return TWO_PAIRS
        elif max(values) == 2 and len(card_count) == 4:
            # AAKQ2
            return PAIR
        else:
            # 34A6K
            return HIGH_CARD


    def __score_hand_joker(self):
        card_count = Counter(self.cards)
        values = card_count.values()
        joker_present = JOKER in card_count

        if 5 in values:
            # XXXXX JJJJJ
            return FIVE_OF_A_KIND
        elif 4 in values and joker_present:
            # XJJJJ JJJJX XXXXJ four plus joker
            return FIVE_OF_A_KIND
        elif 3 in values and 2 in values and joker_present:
            # JJJXX XXXJJ three plus two jokers or three jokers plus pair
            return FIVE_OF_A_KIND
        elif 4 in values:
            # XXXXY four
            return FOUR_OF_A_KIND
        elif 3 in values and card_count[JOKER] == 1:
            # XXXJY three plus joker
            return FOUR_OF_A_KIND
        elif card_count[JOKER] == 3 and len(card_count) == 3:
            # JJJXY three jokers plus anything
            return FOUR_OF_A_KIND
        elif card_count[JOKER] == 2 and len(card_count) == 3:
            # JJXXY two pairs with two jokers
            return FOUR_OF_A_KIND
        elif max(values) == 3 and len(card_count) == 2 and not joker_present:
            # XXXYY full
            return FULL_HOUSE
        elif card_count[JOKER] == 1 and len(card_count) == 3:
            # XXYYJ two pairs + joker
            return FULL_HOUSE
        elif max(values) == 3 and len(card_count) == 3 and not joker_present:
            # XXXAB three
            return THREE
        elif max(values) == 2 and len(card_count) == 4 and joker_present:
            # XXABJ pair + joker
            return THREE
        elif card_count[JOKER] == 2 and len(card_count) == 4:
            ## JJXYZ pair of jokers
            return THREE
        elif max(values) == 2 and len(card_count) == 3 and not joker_present:
            # XXYYZ two pairs
            return TWO_PAIRS
        elif max(values) == 2 and len(card_count) == 4 and not joker_present:
            # XXABC one pair
            return PAIR
        elif len(values) == 5 and joker_present:
            # ABCDJ high card + joker
            return PAIR
        else:
            return HIGH_CARD


def solve(data, joker_active):
    hands_to_bids = {}
    for line in data.splitlines():
        cards, bid = line.split()
        hands_to_bids[Hand(cards, joker_active)] = int(bid)
    sorted_hands = enumerate(sorted(hands_to_bids.keys()), 1)
    return sum((hands_to_bids[hand] * score for score, hand in sorted_hands))

TEST_DATA = '''32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483'''

print('Testing...')
print('Part 1:', solve(TEST_DATA, joker_active=False) == 6440)
print('Part 2:', solve(TEST_DATA, joker_active=True) == 5905)

with open('inp', mode='r', encoding='utf-8') as inp:
    print('Solution...')
    actual_data = inp.read()
    print('Part 1:', solve(actual_data, joker_active=False))
    print('Part 2:', solve(actual_data, joker_active=True))
