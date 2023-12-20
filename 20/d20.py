from collections import deque

print('Day 20 of Advent of Code!')


FLIPFLOP = '%'
CONJUNCTION = '&'
BROADCAST = 'broadcast'

HIGH_PULSE = 1
LOW_PULSE = 0

ON = True
OFF = False


class Module:
    def __init__(self, name) -> None:
        self.name = name
        self.module_inp = []
        self.module_out = []


    def process(self, signal):
        raise NotImplementedError


    def __hash__(self) -> int:
        return hash(self.name)


    def __repr__(self) -> str:
        return f'{self.name}'


class Output(Module):
    def __init__(self, name) -> None:
        super().__init__(name)


    def process(self, signal):
        #print(f'OUTPUT: {signal}')
        return None


class Flipflop(Module):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.mode = False


    def process(self, signal):
        value = signal[1]
        if value == HIGH_PULSE:
            pass
        elif value == LOW_PULSE:
            if self.mode == OFF:
                self.mode = ON
                return HIGH_PULSE
            elif self.mode == ON:
                self.mode = OFF
                return LOW_PULSE


class Conjunction(Module):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.last = {node: LOW_PULSE for node in self.module_inp}

    def process(self, signal):
        sending_node, value = signal
        self.last[sending_node] = value
        if all(self.last.values()):
            return LOW_PULSE
        else:
            return HIGH_PULSE

class Broadcaster(Module):
    def __init__(self, name) -> None:
        super().__init__(name)

    def process(self, signal):
        sending_node, value = signal
        return value


def parse_data(data):
    raw_modules = []
    all_modules = {}
    for line in data.splitlines():
        module_name, destinations = line.split(' -> ')
        destinations = destinations.split(', ')
        proper_name = module_name
        if module_name.startswith(BROADCAST):
            new_module = Broadcaster(module_name)
        elif module_name.startswith(FLIPFLOP):
            proper_name = proper_name[1:]
            new_module = Flipflop(proper_name)
        elif module_name.startswith(CONJUNCTION):
            proper_name = proper_name[1:]
            new_module = Conjunction(proper_name)
        raw_modules.append([proper_name, destinations])
        all_modules[proper_name] = new_module

    for module in raw_modules:
        name, destinations = module
        for destination in destinations:
            if destination not in all_modules:
                all_modules[name].module_out.append(Output(destination))
            else:
                all_modules[name].module_out.append(all_modules[destination])

    for this in raw_modules:
        for other in raw_modules:
            if this != other and this[0] in other[1]:
                all_modules[this[0]].module_inp.append(all_modules[other[0]])
                if 'Conjunction' in type(all_modules[this[0]]).__name__:
                    all_modules[this[0]].last = {node: LOW_PULSE for node in all_modules[this[0]].module_inp}

    return all_modules


def push_button(modules, debug=True):
    first_signal = (None, LOW_PULSE)
    first_module = modules['broadcaster']
    first_state = (first_module, first_signal)

    q = deque([first_state])

    hi, lo = 0, 0

    if debug:
        for v in q:
            print(v)

    while q:
        current, signal = q.popleft()

        if debug:
            print(f'PROCESSING {signal[0]} -> {signal[1]} -> {current}')

        signal_sent = signal[1]
        if signal_sent == HIGH_PULSE:
            hi += 1
        elif signal_sent == LOW_PULSE:
            lo += 1

        processed_value = current.process(signal)

        if debug:
            print(f'After processing: {current} -> {processed_value} TO {current.module_out}')
        if processed_value is None:
            if debug:
                print('IGNORING')
            continue

        for receiver in current.module_out:
            new_signal = (current, processed_value)
            new_state = (receiver, new_signal)
            q.append(new_state)

        if debug:
            print('Queue after cycle:')
            for v in q:
                print(v)
    return hi, lo


def run_pulses(clicks, modules, debug):
    hi, lo = 0, 0
    for _ in range(clicks):
        current_hi, current_lo = push_button(modules, debug)
        hi += current_hi
        lo += current_lo
    return hi * lo

TEST_DATA_SIMPLE = r'''broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a'''

TEST_DATA_SECOND = r'''broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output'''

print('Testing...')
print('Part 1 example 1:', run_pulses(1000, parse_data(TEST_DATA_SIMPLE), False) == 32000000)
print('Part 1 example 2:', run_pulses(1000, parse_data(TEST_DATA_SECOND), False) == 11687500)

with open('inp', mode='r', encoding='utf-8') as inp:
    print('Solution...')
    actual_data = inp.read()
    print('Part 1:', run_pulses(1000, parse_data(actual_data), False))
