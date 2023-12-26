# Advent of Code 2023

For the fifth time I'm trying to find out how far I can make it in [Advent of Code](https://adventofcode.com/2023/). Results for previous editions:
* 2018: 9 days
* 2019: 13 days
* [2020](https://github.com/Leftfish/Advent-of-Code-2020): 25 days for the first time!
* [2021](https://github.com/Leftfish/Advent-of-Code-2021): 25 days for the second time!
* [2022](https://github.com/Leftfish/Advent-of-Code-2022): 25 days for the third time!

The wonderful [AoC community on reddit](https://www.reddit.com/r/adventofcode/) helped me a lot, once again. Visualisations on the AoC subreddit pointed me towards the proper algorithm for Day 10 part 2, then debug Day 19. I needed to peek at other participants' attempts to modify Dijkstra's algorithm to solve Day 17, and to change my approach for simulating bricks for Day 22 part 1. Another hint helped me combine Pick's theorem with the shoelace formula for Day 18.

As of December 26: parts 2 of Days 12, 21 and 24 are on the to-do list indefinitely, i.e. until I get an idea how to approach them. Parts 2 of Days 13, 14, and 20 are still to-do because of time constraints, but I think I have the right approach for each; just haven't had the opportunity yet to code them properly.

Things I **L**earned, **R**evised or **I**mproved at in 2023:

* [Day 1 Python](01/d01.py): debugging off-by-one errors (**I**), iterating with two pointers (**R**) and re.findall & re.search (**R**), because I procrastrinated by implementing this one with two methods
* [Day 2 Python](02/d02.py): itertools.chain (**L**)
* [Day 3 Python](03/d03.py): set operations (**R**), first steps with Pylint (**L**)
* [Day 4 Python](04/d04.py): using dictionaries of dictionaries to store data (**R**)
* [Day 5 Python](05/d05.py): using Python as a hand calculator, really...and finding overlaps of intervals in my not-yet-implemented alternative solution (**R**)
* [Day 6 Python](06/d06.py): implementing quadratic equations (**R**)
* [Day 7 Python](07/d07.py): collections.Counter (**R**), creating hashable objects and with custom comparators (**R**), reading comprehension (**OMG**)
* [Day 8 Python](08/d08.py): itertools.cycle (**R**)
* [Day 9 Python](09/d09.py): deque (**R**)
* [Day 10 Python](10/d10.py): the [even-odd algorithm](https://en.wikipedia.org/wiki/Even%E2%80%93odd_rule) (**L**) although the implementation is not perfect (works for the acutal input, gives off-by-one errors on test data)
* [Day 11 Python](11/d11.py): deepcopy (**R**), itertools.combinations (**R**), Manhattan distance (**R**)
* [Day 12 Python](12/d12.py): recursion (**R**) for an ugly brute-force solution of part 1, part 2 TO DO
* [Day 13 Python](13/d13.py): hash() (**R**), part 2 TO DO because hash() turned out to be a wrong design choice...
* [Day 14 Python](14/d14.py): 2d array operations (**R**) for part 1, part 2 TO DO (need to implement cycle detection)
* [Day 15 Python](15/d15.py): dictionaries/hashmaps (**R**), enums (**R**), regex (**R**), getting used to enumerate instead of for-loops (**I**)
* [Day 16 Python](16/d16.py): iterative BFS (**I**)
* [Day 17 Python](17/d17.py): Dijkstra's algorithm (**I**) with a twist!
* [Day 18 Python](18/d18.py): the [shoelace formula](https://en.wikipedia.org/wiki/Shoelace_formula) (**L**) and [Pick's theorem](https://en.wikipedia.org/wiki/Pick%27s_theorem) (**L**)
* [Day 19 Python](19/d19.py): spotting tree structures (**I**) and traversing them with BFS (**I**), deepcopy (**R**)
* [Day 20 Python](20/d20.py): hash() to create hashable objects (**R**), part 2 TO DO
* [Day 21 Python](21/d21.py): Dijkstra's algorithm (**R**), part 2 TO DO
* [Day 22 Python](22/d22.py): defaultdict with a lambda expression in the constructor (**L**), iterative BFS (**R**)
* [Day 23 Python](23/d23.py) iterative and recursive DFS (**R**), topological sorting (**L**), longest path problem (**L**), working with directed acyclic and cyclic graphs (**I**)
* [Day 24 Python](24/d24.py): finding line intersections in Euclidean geometry (**R**), part 2 TO DO
* [Day 25 Python](25/d25.py): networkx (**L**), graphviz (**L**) and argparse (**L**) for a 'smart' solution that requires eyeballing the graph