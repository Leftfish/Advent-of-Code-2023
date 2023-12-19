from collections import defaultdict
import re
from operator import gt, lt

print('Day 19 of Advent of Code!')


OPERATORS = {'>': gt, '<': lt}
ACCEPT = 'A'
REJECT = 'R'
EOL = 'END'


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
            rulebook[name][idx] = {parameter: (op, value, where)}
        last = max(rulebook[name]) + 1
        rulebook[name][last] = {EOL: all_rules[-1]}
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
    for rule in rulebook[name].values():
        param = list(rule.keys())[0]
        if param != EOL:
            rating_value = rating[param]
            rule_op = rule[param][0]
            rule_value = rule[param][1]
            if rule_op(rating_value, rule_value):
                return rule[param][2]
        else:
            return rule[param]


def sort_naive(rulebook, ratings):
    s = 0
    for rating in ratings.values():
        result = 'in'
        while result not in (ACCEPT, REJECT):
            result = get_next(rating, rulebook, result)
        if result == ACCEPT:
            s += sum(rating.values())
    return s


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
print('Part 1:', sort_naive(test_rulebook, test_ratings) == 19114)


with open('inp', mode='r', encoding='utf-8') as inp:
    print('Solution...')
    actual_data = inp.read()
    raw_workflows, raw_ratings = actual_data.split('\n\n')
    actual_rulebook = make_rulebook(raw_workflows)
    actual_ratings = read_ratings(raw_ratings)
    print('Part 1:', sort_naive(actual_rulebook, actual_ratings))
