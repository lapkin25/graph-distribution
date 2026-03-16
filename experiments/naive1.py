import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

"""
class NodeInfo:
    def __init__(self):
        self.val = 0.0
"""

G = nx.Graph()
"""
G.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8, 9])
G.add_edges_from([(1, 2), (2, 3), (2, 4), (4, 5), (3, 5),
                  (5, 6), (6, 7), (7, 8), (8, 9), (1, 9), (4, 8)])
"""

G.add_nodes_from([1, 2, 3, 4, 5, 6])
G.add_edges_from([(1, 2), (2, 3), (2, 4), (4, 5), (3, 5), (5, 6)])


nx.set_node_attributes(G, None, "val")
G.nodes[1]["val"] = 0
print("t = 0", nx.get_node_attributes(G, "val"))

"""
for t in range(1, 10):
    prev_vals = nx.get_node_attributes(G, "val")
    new_vals = prev_vals.copy()
    for node in G.nodes:
        if any([prev_vals[u] is not None for u in G.adj[node]]):
            new_vals[node] = np.mean([prev_vals[u] for u in G.adj[node] if prev_vals[u] is not None]) + 1
        else:
            new_vals[node] = None
        if prev_vals[node] is not None and (new_vals[node] is None or prev_vals[node] < new_vals[node]):
            new_vals[node] = prev_vals[node]
    nx.set_node_attributes(G, new_vals, "val")
    print(f"t = {t}", nx.get_node_attributes(G, "val"))
"""

"""
for t in range(1, 50):
    prev_vals = nx.get_node_attributes(G, "val")
    new_vals = prev_vals.copy()
    for node in G.nodes:
        if prev_vals[node] is not None:
            new_vals[node] = np.mean([prev_vals[node]] + [prev_vals[u] + 1 for u in G.adj[node] if prev_vals[u] is not None])
        else:
            if any([prev_vals[u] is not None for u in G.adj[node]]):
                new_vals[node] = np.mean([prev_vals[u] + 1 for u in G.adj[node] if prev_vals[u] is not None])
            else:
                new_vals[node] = None
    nx.set_node_attributes(G, new_vals, "val")
    print(f"t = {t}", nx.get_node_attributes(G, "val"))
    if t > 3:
        print([float(new_vals[node] - new_vals[1]) for node in G.nodes])
"""

"""
for t in range(1, 50):
    prev_vals = nx.get_node_attributes(G, "val")
    new_vals = prev_vals.copy()
    for node in G.nodes:
        if prev_vals[node] is not None:
            if any([prev_vals[u] is not None for u in G.adj[node]]):
                #new_vals[node] = np.mean([prev_vals[node]] * (len([u in G.adj[node] for u in G.adj[node] if prev_vals[u] is not None])) + [prev_vals[u] + 1 for u in G.adj[node] if prev_vals[u] is not None])
                new_vals[node] = np.mean([prev_vals[node]] + [prev_vals[u] + 1 for u in G.adj[node] if prev_vals[u] is not None])
            else:
                new_vals[node] = prev_vals[node]
        else:
            if any([prev_vals[u] is not None for u in G.adj[node]]):
                new_vals[node] = np.mean([prev_vals[u] + 1 for u in G.adj[node] if prev_vals[u] is not None])
            else:
                new_vals[node] = None
#        if new_vals[node] is not None and prev_vals[node] is not None and new_vals[node] > prev_vals[node]:
#            new_vals[node] = prev_vals[node]
    nx.set_node_attributes(G, new_vals, "val")
    print(f"t = {t}", nx.get_node_attributes(G, "val"))
    if t > 3:
        print([float(new_vals[node]) for node in G.nodes])

print(nx.betweenness_centrality(G))
"""


for t in range(1, 50):
    prev_vals = nx.get_node_attributes(G, "val")
    new_vals = prev_vals.copy()
    for node in G.nodes:
        if any([prev_vals[u] is not None for u in G.adj[node]]):
            new_vals[node] = float(np.mean([prev_vals[u] + 1 for u in G.adj[node] if prev_vals[u] is not None]) / len([u for u in G.adj[node] if prev_vals[u] is not None]))
        else:
            new_vals[node] = None
        if prev_vals[node] is not None:
            if new_vals[node] is None:
                new_vals[node] = prev_vals[node]
            else:
                if prev_vals[node] < new_vals[node]:
                    new_vals[node] = prev_vals[node]
    nx.set_node_attributes(G, new_vals, "val")
    print(f"t = {t}", nx.get_node_attributes(G, "val"))
    #if t > 3:
    #    print([float(new_vals[node]) for node in G.nodes])

#print(nx.betweenness_centrality(G))

#nx.draw(G)
#plt.show()
