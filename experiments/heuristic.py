import networkx as nx
import numpy as np


G = nx.Graph()

G.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8, 9])
G.add_edges_from([(1, 2), (2, 3), (2, 4), (4, 5), (3, 5),
                  (5, 6), (6, 7), (7, 8), (8, 9), (1, 9), (4, 8)])

"""
# нумерация ребер графа
edges_list = []
for i, e in enumerate(G.edges):
    G.edges[e]['num'] = i
    edges_list.append(e)
"""

#print(G.edges[2, 3]['num'], G.edges[3, 2]['num'])

for v in G.nodes:
    G.nodes[v]['d'] = None

start = 1

d = [None] * len(G.nodes)
G.nodes[start]['d'] = 0.0
visited = set()
for i in range(len(G.nodes)):
    min_node = None
    min_d = None
    for v in G.nodes:
        if v in visited:
            continue
        d_list = [G.nodes[u]['d'] for u in G.adj[v] if G.nodes[u]['d'] is not None]
        #print(d_list)
        if not d_list:
            continue
        d = np.mean(d_list) + 1  #- это если все коэффициенты равны 1

        """
        # находим оптимальные коэффициенты
        def g(a):
            ans = 0
            for j in range(len(br.branches)):
                #if j == len(br.branches) - 1:
                #    lam = 1 - np.sum(lam_coefs)
                #else:
                #    lam = lam_coefs[j]
                lam = lam_coefs[j]
                for k in range(len(G.edges)):
                    terms[k] += lam * branch_coefs[j, k]
            ans = np.sum(terms ** 2)
            return ans
        bounds = Bounds([0] * len(br.branches), [1] * len(br.branches))
        linear_constraint = LinearConstraint([[1] * len(br.branches)], [1], [1])
        method = 'trust-constr'
        res = minimize(g, lams, method=method,
                       constraints=linear_constraint, options={'verbose': 0}, bounds=bounds)
        lams = res.x
        """

        if min_d is None or d < min_d:
            min_d = d
            min_node = v
        #d = np.mean([G.nodes[u]['d'] for u in G.adj[v] if G.nodes[u]['d'] is not None])
#        if G.nodes[v]['d'] is not None and (min_d is None or d < min_d):
#            min_d = d
#            min_node = v
    G.nodes[min_node]['d'] = min_d
    visited.add(min_node)
    print(min_node, "<-", min_d)
