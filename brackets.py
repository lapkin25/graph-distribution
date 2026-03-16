import networkx as nx


class Bracket:
    def __init__(self, node, brackets_list, adj_list):
        self.node = node
        self.branches = []
        self.adj_nodes = []
        self.edges = []
        # в списках branches, edges, adj_nodes равное число элементов
        for br, adj_node in zip(brackets_list, adj_list):
            self.branches.append(br)
            self.adj_nodes.append(adj_node)
            self.edges.append(G.edges[node, adj_node]['num'])

    def print(self, indentation=0):
        print(' ' * indentation, '[')
        print(' ' * indentation, f'Вершина {self.node}:')
        print(' ' * indentation, f'Число развилок: {len(self.branches)}')
        for i in range(len(self.branches)):
            print(' ' * indentation, f'Ребро #{self.edges[i]} в {self.adj_nodes[i]}')
            self.branches[i].print(indentation + 1)
        print(' ' * indentation, ']')


def backtracking(G, source, current, stack):
    if current == source:
        return Bracket(source, [], [])

    brackets_list = []
    adj_list = []
    for u in G.adj[current]:
        if u not in stack:
            stack.append(u)
            res = backtracking(G, source, u, stack)
            stack.pop()
            if res is not None:
                brackets_list.append(res)
                adj_list.append(u)
    if len(brackets_list) == 0:
        return None
    else:
        br = Bracket(current, brackets_list, adj_list)
        return br

def get_bracket(G, source, destination):
    return backtracking(G, source, destination, [destination])

def tree_search(br, coefs, product):
    print(f"Вершина {br.node}: {len(br.branches)} разветвлений: {br.edges}")
    print(coefs)
    if len(br.branches) == 0:
        return 0.0
    lam = 1.0 / len(br.branches)
    for i in range(len(br.branches)):
        coefs[br.edges[i]] += product * lam
        tree_search(br.branches[i], coefs, product * lam)
    return sum([x ** 2 for x in coefs])

def calc_variance_uniformly(br):
    coefs = [0.0] * len(G.edges)
    return tree_search(br, coefs, 1.0)



G = nx.Graph()

G.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8, 9])
G.add_edges_from([(1, 2), (2, 3), (2, 4), (4, 5), (3, 5),
                  (5, 6), (6, 7), (7, 8), (8, 9), (1, 9), (4, 8)])

# нумерация ребер графа
edges_list = []
for i, e in enumerate(G.edges):
    G.edges[e]['num'] = i
    edges_list.append(e)

br = get_bracket(G, 1, 6)
br.print()
print("Рёбра:", G.edges)
print(calc_variance_uniformly(br))