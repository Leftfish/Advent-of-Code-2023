from itertools import cycle
from math import lcm

print('Day 8 of Advent of Code!')


START = 'AAA'
END = 'ZZZ'
DIRS = {'L': 0, 'R': 1}


def get_nodes_and_instructions(data):
    instruction_data, node_data = data.split('\n\n')

    instructions = cycle(instruction_data)
    nodes = {}

    for node in node_data.splitlines():
        node_id, node_targets = node.split(' = ')
        node_targets = node_targets[1:-1].split(', ')
        nodes[node_id] = node_targets

    return instructions, nodes


def is_start(node):
    return node[-1] == 'A'

def is_end(node):
    return node[-1] == 'Z'


def is_finish(nodes):
    return all((is_end(node) for node in nodes))


def steps_human(instructions, nodes):
    current = START
    steps = 0
    while current != END:
        current = nodes[current][DIRS[next(instructions)]]
        steps += 1
    return steps


def find_one_cycle(instructions, node, nodes):
    steps = 0
    current = node

    while True:
        current = nodes[current][DIRS[next(instructions)]]
        steps += 1

        if is_end(current):
            return steps

def find_cycles(instructions, start_nodes, nodes):
    return [find_one_cycle(instructions, node, nodes) for node in start_nodes]


TEST_DATA = '''RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)'''

TEST_DATA2 = '''LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)'''


print('Testing...')
parsed_instructions, parsed_nodes = get_nodes_and_instructions(TEST_DATA)
print('Part 1:', steps_human(*get_nodes_and_instructions(TEST_DATA)) == 2)
parsed_instructions, parsed_nodes = get_nodes_and_instructions(TEST_DATA2)
current_nodes = [node for node in parsed_nodes if is_start(node)]
print('Part 2:', lcm(*find_cycles(parsed_instructions, current_nodes, parsed_nodes)) == 6)

with open('inp', mode='r', encoding='utf-8') as inp:
    print('Solution...')
    actual_data = inp.read()
    print('Part 1:', steps_human(*get_nodes_and_instructions(actual_data)))
    parsed_instructions, parsed_nodes = get_nodes_and_instructions(actual_data)
    current_nodes = [node for node in parsed_nodes if is_start(node)]
    print('Part 2:', lcm(*find_cycles(parsed_instructions, current_nodes, parsed_nodes)))
