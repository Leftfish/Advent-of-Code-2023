from collections import Counter

print('Day 7 of Advent of Code!')

CARDS = 'AKQJT98765432'
CARDS_JOKER = 'AKQT98765432J'
POINTS = range(len(CARDS), 0, -1)
JOKER = 'J'
SCORES = dict(zip(CARDS, POINTS))
SCORES_JOKER = {card: score for card, score in zip(CARDS_JOKER, POINTS)}

class Hand:
    def __init__(self, cards_in_hand, joker):
        self.cards = cards_in_hand
        if not joker:
            self.score = [self.__score_hand()] + [SCORES[c] for c in self.cards]
        else:
            self.score = [self.__score_hand_joker()] + [SCORES_JOKER[c] for c in self.cards]

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
        scores = Counter(self.cards)

        first_level = len(scores)
        second_level = min(scores.values())
        third_level = max(scores.values())

        if first_level == 1:
            modifier = first_level
        elif first_level == 2 and second_level == 1:
            modifier = first_level
        elif first_level == 2 and second_level != 1:
            modifier = first_level + 1
        elif first_level == 3 and third_level == 3:
            modifier = first_level + 1
        elif first_level == 3 and third_level != 3:
            modifier = first_level + 2
        elif first_level == 4:
            modifier = first_level + 2
        else:
            modifier = first_level + 2

        hand_score = -modifier

        return hand_score
    
    def __score_hand_joker(self):
        scores = Counter(self.cards)
        values = scores.values()
        
        if 5 in values or (4 in values and JOKER in scores):
            # XXXXX JJJJJ XJJJJ JJJJX XXXXJ five with/without joker
            hand_score = 7
        elif 3 in values and 2 in values and JOKER in scores:
            # JJJXX XXXJJ five with joker
            hand_score = 7
        elif 4 in values or (3 in values and scores[JOKER] == 1):
            # XXXXY XXXJY four or three plus joker = four
            hand_score = 6
        elif scores[JOKER] == 3 and len(scores) == 3:
            # JJJXY three jokers plus anything = four
            hand_score = 6
        elif scores[JOKER] == 2 and len(scores) == 3:
            # JJXXY two pairs with two jokers = four
            hand_score = 6
        elif 3 in values and 2 in values and JOKER not in scores:
            # XXXYY full
            hand_score = 5
        elif scores[JOKER] == 1 and len(scores) == 3:
            # XXYYJ two pairs + joker = full
            hand_score = 5
        elif max(values) == 3 and len(scores) == 3 and JOKER not in scores:
            # XXXAB three
            hand_score = 4
        elif max(values) == 2 and len(scores) == 4 and JOKER in scores:
            # XXABJ pair + joker = three
            hand_score = 4
        elif scores[JOKER] == 2 and len(scores) == 4:
            ## JJXYZ pair of jokers and nothing else = three
            hand_score = 4
        elif max(values) == 2 and len(scores) == 3  and JOKER not in scores:
            # XXYYZ two pairs
            hand_score = 3
        elif max(values) == 2 and len(scores) == 4 and JOKER not in scores:
            # XXABC one pair
            hand_score = 2
        elif len(values) == 5 and JOKER in scores:
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
test_hands_to_bids = get_hands_to_bids(TEST_DATA.splitlines(), joker_active=False)
test_hands = list(test_hands_to_bids.keys())
hand_ranking = enumerate(sorted(test_hands), 1)
print('Part 1:', sum((test_hands_to_bids[hand] * score for score, hand in hand_ranking)))
test_hands_to_bids = get_hands_to_bids(TEST_DATA.splitlines(), joker_active=True)
test_hands = list(test_hands_to_bids.keys())
hand_ranking = enumerate(sorted(test_hands), 1)
print('Part 2:', sum((test_hands_to_bids[hand] * score for score, hand in hand_ranking)))

with open('inp', mode='r', encoding='utf-8') as inp:
    print('Solution...')
    actual_data = inp.readlines()
    actual_hands_to_bids = get_hands_to_bids(actual_data, joker_active=False)
    actual_hands = list(actual_hands_to_bids.keys())
    hand_ranking = enumerate(sorted(actual_hands), 1)
    print('Part 1:', sum((actual_hands_to_bids[hand] * score for score, hand in hand_ranking)))
    
    actual_hands_to_bids = get_hands_to_bids(actual_data, joker_active=True)
    actual_hands = list(actual_hands_to_bids.keys())
    hand_ranking = enumerate(sorted(actual_hands), 1)
    
    print('Part 2:', sum((actual_hands_to_bids[hand] * score for score, hand in hand_ranking)))

    
