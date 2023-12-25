import argparse
import graphviz
import networkx as nx

print('Day 25 of Advent of Code!')


def parse_data(data):
    edges = []
    for line in data.splitlines():
        this, others = line.split(': ')
        others = others.split(' ')
        for other in others:
            edges.append((this, other))
    return nx.Graph(edges)


def make_cut(graph, to_remove):
    for removed_edge in to_remove:
        graph.remove_edge(*removed_edge)

    first_start, second_start = to_remove[0]
    first_part, second_part = set(), set()

    for edge in nx.edge_dfs(graph, first_start):
        first_part.add(edge[0])
        first_part.add(edge[1])

    for edge in nx.edge_dfs(graph, second_start):
        second_part.add(edge[0])
        second_part.add(edge[1])

    return len(first_part) * len(second_part)


TEST_DATA = '''jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr'''

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", help="use only test data", action="store_true")
    parser.add_argument("--dot", help="make a .dot file for Graphviz and visualize the graph")
    parser.add_argument("--cut", help="cut the wires and calculate the answer")
    args = parser.parse_args()

    if args.test:
        print('Testing...')
        data = TEST_DATA
    else:
        with open('inp', mode='r', encoding='utf-8') as inp:
            print('Solution...')
            data = inp.read()

    graph = parse_data(data)

    if args.cut:
        # to remove in test data: pzl-hfx;nvd-jqt;cmg-bvb
        # to remove in actual data: lnr-pgt;tjz-vph;zkt-jhq
        to_remove = []
        for pair in args.cut.split(';'):
            first, second = pair.split('-')
            to_remove.append((first, second))
        print('Part 1:', make_cut(graph, to_remove))

    if args.dot:
        visual_graph = graphviz.Graph(args.dot, format='png')
        for edge in graph.edges:
            visual_graph.edge(*edge)
        visual_graph.engine = 'neato'
        visual_graph.render().replace('\\', '/')

main()
