import re

from collections import defaultdict, deque
from copy import deepcopy
from operator import gt, lt

print('Day 19 of Advent of Code!')


OPERATORS = {'>': gt, '<': lt}
ACCEPT = 'A'
REJECT = 'R'
FINISH = 'END'
XMAS_TO_ID = {'x': 0, 'm': 1, 'a': 2, 's': 3}


class Range:
    def __init__(self, nxt, x=None, m=None, a=None, s=None):
        self.x = x if x else [1,4000]
        self.m = m if m else [1,4000]
        self.a = a if a else [1,4000]
        self.s = s if s else [1,4000]
        self.nxt = nxt

    def sum(self):
        x = self.x[1] - self.x[0] + 1
        m = self.m[1] - self.m[0] + 1
        a = self.a[1] - self.a[0] + 1
        s = self.s[1] - self.s[0] + 1
        return x*m*a*s

    def __repr__(self):
        return f'x: {self.x} m: {self.m} a: {self.a} s: {self.s} nxt: {self.nxt}'


def make_rulebook(workflows):
    rulebook = defaultdict(dict)

    for workflow in workflows.splitlines():
        name, raw_rules = re.findall(r'(.+){(.+)}', workflow)[0]
        all_rules = raw_rules.split(',')
        rulebook[name] = defaultdict(dict)

        for idx, rule in enumerate(all_rules[:-1]):
            what, where = rule.split(':')
            parameter = what[0]
            op = OPERATORS[what[1]]
            value = int(what[2:])
            rulebook[name][idx] = (parameter, op, value, where)

        last_rule_id = max(rulebook[name]) + 1
        rulebook[name][last_rule_id] = (FINISH, None, None, all_rules[-1])

    return rulebook


def read_ratings(ratings):
    inventory = defaultdict(dict)
    for idx, rating in enumerate(ratings.splitlines()):
        features = re.findall(r'{(.+)}', rating)[0].split(',')
        for feature in features:
            parameter, value = feature.split('=')
            inventory[idx][parameter] = int(value)
    return inventory


def get_next(rating, rulebook, name):
    for param, op, rule_value, nxt in rulebook[name].values():
        if param != FINISH:
            if op(rating[param], rule_value):
                return nxt
        else:
            return nxt


def evaluate_parts(rulebook, ratings):
    s = 0
    for rating in ratings.values():
        result = 'in'
        while result not in (ACCEPT, REJECT):
            result = get_next(rating, rulebook, result)
        if result == ACCEPT:
            s += sum(rating.values())
    return s


def evaluate_rulebook(rulebook):
    start = Range(nxt='in')
    q = deque([start])
    accepted = []

    while q:
        current = q.popleft()

        rules_to_check = rulebook[current.nxt]
        rng_not_covered = [current.x, current.m, current.a, current.s]

        for rule_id in rules_to_check:
            param, op, value, next_step = rules_to_check[rule_id]
            rng_to_update = deepcopy(rng_not_covered)

            if param != FINISH:
                param_idx = XMAS_TO_ID[param]
                if op == lt:
                    if rng_to_update[param_idx][1] > value:
                        rng_to_update[param_idx][1], rng_not_covered[param_idx][0] = value-1, value
                if op == gt:
                    if rng_to_update[param_idx][0] < value:
                        rng_to_update[param_idx][0], rng_not_covered[param_idx][1] = value+1, value

                new_state = Range(next_step, *rng_to_update)
                if next_step == ACCEPT:
                    accepted.append(new_state)
                else:
                    q.append(new_state)

            elif param == FINISH:
                new_state = Range(next_step, *rng_not_covered)
                if next_step == ACCEPT:
                    accepted.append(new_state)
                else:
                    q.append(new_state)
    return accepted


TEST_DATA = '''px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}'''

print('Testing...')
raw_workflows, raw_ratings = TEST_DATA.split('\n\n')
test_rulebook = make_rulebook(raw_workflows)
test_ratings = read_ratings(raw_ratings)
print('Part 1:', evaluate_parts(test_rulebook, test_ratings) == 19114)
print('Part 2:', sum((rng.sum() for rng in evaluate_rulebook(test_rulebook))) == 167409079868000)


with open('inp', mode='r', encoding='utf-8') as inp:
    print('Solution...')
    actual_data = inp.read()
    raw_workflows, raw_ratings = actual_data.split('\n\n')
    actual_rulebook = make_rulebook(raw_workflows)
    actual_ratings = read_ratings(raw_ratings)
    print('Part 1:', evaluate_parts(actual_rulebook, actual_ratings))
    print('Part 2:', sum((rng.sum() for rng in evaluate_rulebook(actual_rulebook))))
