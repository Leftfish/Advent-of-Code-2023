from collections import defaultdict, deque
import heapq

print('Day 17 of Advent of Code!')

class Graph:
    def __init__(self, data):
        self.number_of_vertices = len(data[0]) * len(data)
        self.edges_horizontal = defaultdict(list)
        self.edges_vertical = defaultdict(list)
        self.edges = defaultdict(list)

        for i in range(len(data)):
            for j in range(len(data[0])):
                for (adj_i, adj_j) in [(i-1, j), (i+1, j)]: # one up, down
                    if len(data) > adj_i >= 0 and len(data[0]) > adj_j >= 0:
                        neighbor_coords = (adj_i, adj_j)
                        neighbor_weight = data[adj_i][adj_j]
                        self.edges_vertical[(i, j)].append((neighbor_coords, neighbor_weight))

                for (adj_i, adj_j) in [(i, j-1), (i, j+1)]: # one left, right
                    if len(data) > adj_i >= 0 and len(data[0]) > adj_j >= 0:
                        neighbor_coords = (adj_i, adj_j)
                        neighbor_weight = data[adj_i][adj_j]
                        self.edges_horizontal[(i, j)].append((neighbor_coords, neighbor_weight))
                
                adj_i, adj_j = i-2, j # two up
                if len(data) > adj_i >= 0 and len(data[0]) > adj_j >= 0:
                    neighbor_coords = (adj_i, adj_j)
                    neighbor_weight = data[adj_i][adj_j] + data[adj_i + 1][adj_j]
                    self.edges_vertical[(i, j)].append((neighbor_coords, neighbor_weight))

                adj_i, adj_j = i+2, j # two down
                if len(data) > adj_i >= 0 and len(data[0]) > adj_j >= 0:
                    neighbor_coords = (adj_i, adj_j)
                    neighbor_weight = data[adj_i][adj_j] + data[adj_i - 1][adj_j]
                    self.edges_vertical[(i, j)].append((neighbor_coords, neighbor_weight))

                adj_i, adj_j = i, j-2 # two left
                if len(data) > adj_i >= 0 and len(data[0]) > adj_j >= 0:
                    neighbor_coords = (adj_i, adj_j)
                    neighbor_weight = data[adj_i][adj_j] + data[adj_i][adj_j + 1]
                    self.edges_horizontal[(i, j)].append((neighbor_coords, neighbor_weight))

                adj_i, adj_j = i, j+2 # two right
                if len(data) > adj_i >= 0 and len(data[0]) > adj_j >= 0:
                    neighbor_coords = (adj_i, adj_j)
                    neighbor_weight = data[adj_i][adj_j] + data[adj_i][adj_j - 1]
                    self.edges_horizontal[(i, j)].append((neighbor_coords, neighbor_weight))

                adj_i, adj_j = i-3, j # three up
                if len(data) > adj_i >= 0 and len(data[0]) > adj_j >= 0:
                    neighbor_coords = (adj_i, adj_j)
                    neighbor_weight = data[adj_i][adj_j] + data[adj_i + 2][adj_j] + data[adj_i + 1][adj_j]
                    self.edges_vertical[(i, j)].append((neighbor_coords, neighbor_weight))

                adj_i, adj_j = i+3, j # three down
                if len(data) > adj_i >= 0 and len(data[0]) > adj_j >= 0:
                    neighbor_coords = (adj_i, adj_j)
                    neighbor_weight = data[adj_i][adj_j] + data[adj_i - 2][adj_j]+ data[adj_i - 1][adj_j]
                    self.edges_vertical[(i, j)].append((neighbor_coords, neighbor_weight))

                adj_i, adj_j = i, j-3 # three left
                if len(data) > adj_i >= 0 and len(data[0]) > adj_j >= 0:
                    neighbor_coords = (adj_i, adj_j)
                    neighbor_weight = data[adj_i][adj_j] + data[adj_i][adj_j + 2] + data[adj_i][adj_j + 1]
                    self.edges_horizontal[(i, j)].append((neighbor_coords, neighbor_weight))

                adj_i, adj_j = i, j+3 # three right
                if len(data) > adj_i >= 0 and len(data[0]) > adj_j >= 0:
                    neighbor_coords = (adj_i, adj_j)
                    neighbor_weight = data[adj_i][adj_j] + data[adj_i][adj_j - 2] + data[adj_i][adj_j - 1]
                    self.edges_horizontal[(i, j)].append((neighbor_coords, neighbor_weight))

        for k, v in self.edges_vertical.items():
            self.edges[k].extend(v)
        for k, v in self.edges_horizontal.items():
            self.edges[k].extend(v)
           
    
    def bfs(self, start, start_dir):
        distances = {vertex: float('inf') for vertex in self.edges}
        distances[start] = 0
        visited = defaultdict(int)

        q = deque([])
        q.appendleft((0, start, start_dir))
        visited[start] = 0

        while q:
            dist_so_far, current, direction_horizontal = q.popleft()
            visited[current] = dist_so_far
            if direction_horizontal:
                neighbors = self.edges_horizontal
                next_dir = False
            else:
                neighbors = self.edges_vertical
                next_dir = True
            for neighbor in neighbors[current]:
                
                neighbor_coord, neighbor_cost = neighbor
                cost_to_move = dist_so_far + neighbor_cost

                if neighbor_coord not in visited:
                    distances[neighbor_coord] = cost_to_move
                    q.append((cost_to_move, neighbor_coord, next_dir))
                else:
                    if cost_to_move < distances[neighbor_coord]:
                        distances[neighbor_coord] = cost_to_move
                        q.append((cost_to_move, neighbor_coord, next_dir))

        return distances



TEST_DATA = '''2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533'''

test_data = [[int(dig) for dig in line] for line in TEST_DATA.splitlines()]
g = Graph(test_data)
a = g.bfs((0,0), True)[(12,12)]
b = g.bfs((0,0), False)[(12,12)]
print(min(a,b))

print('Testing...')


with open('inp', mode='r', encoding='utf-8') as inp:
    print('Solution...')
    actual_data = inp.read()
    test_data = [[int(dig) for dig in line] for line in actual_data.splitlines()]
