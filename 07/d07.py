from collections import Counter

print('Day 7 of Advent of Code!')

CARDS = 'AKQJT98765432'
CARDS_JOKER = 'AKQT98765432J'
CARD_POINTS = range(len(CARDS), 0, -1)
JOKER = 'J'
STANDARD_SCORES = dict(zip(CARDS, CARD_POINTS))
JOKER_SCORES = {card: score for card, score in zip(CARDS_JOKER, CARD_POINTS)}


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
            # five XXXXX
            hand_score = 7
        elif max(values) == 4:
            # four XXXXY
            hand_score = 6
        elif max(values) == 3 and len(card_count) == 2:
            # full XXXZZ
            hand_score = 5
        elif max(values) == 3 and len(card_count) == 3:
            # three XXXYZ
            hand_score = 4
        elif max(values) == 2 and len(card_count) == 3:
            # two pairs XXPPZ
            hand_score = 3
        elif max(values) == 2 and len(card_count) == 4:
            # one pair XXPZU
            hand_score = 2
        else:
            # high card 34567
            hand_score = 1

        return hand_score


    def __score_hand_joker(self):
        card_count = Counter(self.cards)
        values = card_count.values()

        if 5 in values or (4 in values and JOKER in card_count):
            # XXXXX JJJJJ XJJJJ JJJJX XXXXJ five with/without joker
            hand_score = 7
        elif 3 in values and 2 in values and JOKER in card_count:
            # JJJXX XXXJJ five with joker
            hand_score = 7
        elif 4 in values or (3 in values and card_count[JOKER] == 1):
            # XXXXY XXXJY four or three plus joker = four
            hand_score = 6
        elif card_count[JOKER] == 3 and len(card_count) == 3:
            # JJJXY three jokers plus anything = four
            hand_score = 6
        elif card_count[JOKER] == 2 and len(card_count) == 3:
            # JJXXY two pairs with two jokers = four
            hand_score = 6
        elif 3 in values and 2 in values and JOKER not in card_count:
            # XXXYY full
            hand_score = 5
        elif card_count[JOKER] == 1 and len(card_count) == 3:
            # XXYYJ two pairs + joker = full
            hand_score = 5
        elif max(values) == 3 and len(card_count) == 3 and JOKER not in card_count:
            # XXXAB three
            hand_score = 4
        elif max(values) == 2 and len(card_count) == 4 and JOKER in card_count:
            # XXABJ pair + joker = three
            hand_score = 4
        elif card_count[JOKER] == 2 and len(card_count) == 4:
            ## JJXYZ pair of jokers and nothing else = three
            hand_score = 4
        elif max(values) == 2 and len(card_count) == 3  and JOKER not in card_count:
            # XXYYZ two pairs
            hand_score = 3
        elif max(values) == 2 and len(card_count) == 4 and JOKER not in card_count:
            # XXABC one pair
            hand_score = 2
        elif len(values) == 5 and JOKER in card_count:
            # ABCDJ high card + joker = pair
            hand_score = 2
        else:
            hand_score = 1

        return hand_score

def get_hands_to_bids(data, joker_active):
    hands_to_bids = {}
    for line in data:
        cards, bid = line.split()
        hands_to_bids[Hand(cards, joker_active)] = int(bid)
    return hands_to_bids

TEST_DATA = '''32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483'''

print('Testing...')
test_without_J = get_hands_to_bids(TEST_DATA.splitlines(), joker_active=False)
print('Part 1:', sum((test_without_J[hand] * score for score, hand in enumerate(sorted(test_without_J.keys()), 1))) == 6440)
test_with_J = get_hands_to_bids(TEST_DATA.splitlines(), joker_active=True)
print('Part 2:', sum((test_with_J[hand] * score for score, hand in enumerate(sorted(test_with_J.keys()), 1))) == 5905)

with open('inp', mode='r', encoding='utf-8') as inp:
    print('Solution...')
    actual_data = inp.readlines()
    actual_without_J = get_hands_to_bids(actual_data, joker_active=False)
    print('Part 1:', sum((actual_without_J[hand] * score for score, hand in enumerate(sorted(actual_without_J.keys()), 1))))
    actual_with_J = get_hands_to_bids(actual_data, joker_active=True)
    print('Part 2:', sum((actual_with_J[hand] * score for score, hand in enumerate(sorted(actual_with_J.keys()), 1))))
