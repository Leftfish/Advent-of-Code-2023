from collections import defaultdict, deque
from itertools import count
from math import lcm


print('Day 20 of Advent of Code!')


FLIPFLOP = '%'
CONJUNCTION = '&'
BROADCAST = 'broadcaster'

HIGH_PULSE = 1
LOW_PULSE = 0

ON, OFF = 1, 0

MAX_PUSHES_PART_1 = 1000 + 1


def parse_data(data):
    machine = defaultdict(list)
    flip_flops = {}
    counters = {}
    for line in data.splitlines():
        module_name, destinations = line.split(' -> ')
        destinations = destinations.split(', ')
        if module_name.startswith(BROADCAST):
            machine[module_name] = destinations
        elif module_name.startswith(FLIPFLOP):
            proper_name = module_name[1:]
            machine[proper_name] = destinations
            flip_flops[proper_name] = OFF
        elif module_name.startswith(CONJUNCTION):
            proper_name = module_name[1:]
            machine[proper_name] = destinations
            counters[proper_name] = {}

    for other, destinations in machine.items():
        for module in counters:
            if module in destinations:
                counters[module][other] = LOW_PULSE

    return machine, flip_flops, counters


def run_machine(machine, flip_flops, counters):
    final_node = [node for node in machine if 'rx' in machine[node]].pop()
    final_counters = {module: [] for module in machine if final_node in machine[module]}

    cycles = []
    hi, lo = 0, 0

    for push in count(1):
        if all([len(pings) >= 2 for pings in final_counters.values()]):
            for receiver, pings in final_counters.items():
                if pings[-1] / pings[0] == 2:
                    cycles.append(pings[0])
            print('Part 2:', lcm(*cycles))
            break

        if push == MAX_PUSHES_PART_1:
            print('Part 1:', hi * lo)

        q = deque([(None, BROADCAST, LOW_PULSE)])

        while q:
            sender, receiver, signal = q.popleft()
            new_signal = None

            if signal == HIGH_PULSE:
                hi += 1
            elif signal == LOW_PULSE:
                lo += 1

            if receiver == BROADCAST:
                new_signal = LOW_PULSE

            elif receiver in flip_flops:
                if signal == LOW_PULSE:
                    current_status = flip_flops[receiver]
                    if current_status == ON:
                        flip_flops[receiver] = OFF
                        new_signal = LOW_PULSE
                    elif current_status == OFF:
                        flip_flops[receiver] = ON
                        new_signal = HIGH_PULSE
                elif signal == HIGH_PULSE:
                    pass

            elif receiver in counters:
                counters[receiver][sender] = signal
                if all(counters[receiver].values()):
                    new_signal = LOW_PULSE
                else:
                    new_signal = HIGH_PULSE

                if receiver in final_counters and new_signal == HIGH_PULSE:
                    final_counters[receiver].append(push)

            for next_node in machine[receiver]:
                if new_signal is not None:
                    new_state = (receiver, next_node, new_signal)
                    q.append(new_state)


with open('inp', mode='r', encoding='utf-8') as inp:
    print('Solution...')
    run_machine(*parse_data(inp.read()))
