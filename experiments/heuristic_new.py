import networkx as nx
from scipy.optimize import Bounds, LinearConstraint, minimize
import numpy as np


G = nx.Graph()

G.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8, 9])
G.add_edges_from([(1, 2), (2, 3), (2, 4), (4, 5), (3, 5),
                  (5, 6), (6, 7), (7, 8), (8, 9), (1, 9), (4, 8)])


# нумерация ребер графа
edges_list = []
for i, e in enumerate(G.edges):
    G.edges[e]['num'] = i
    edges_list.append(e)


#print(G.edges[2, 3]['num'], G.edges[3, 2]['num'])

for v in G.nodes:
    G.nodes[v]['d'] = None
    G.nodes[v]['coef'] = None

start = 1

G.nodes[start]['d'] = 0.0
for v in G.nodes:
    G.nodes[v]['coef'] = [0.0] * len(G.edges)

visited = set()
for i in range(len(G.nodes)):
    min_node = None
    min_d = None
    for v in G.nodes:
        if v in visited:
            continue
        d_list = [G.nodes[u]['d'] for u in G.adj[v] if G.nodes[u]['d'] is not None]
        vert_list = [u for u in G.adj[v] if G.nodes[u]['d'] is not None]
        coef_list = [G.nodes[u]['coef'] for u in G.adj[v] if G.nodes[u]['d'] is not None]
        #print(d_list)
        if not d_list:
            continue
        if not coef_list:
            continue
        #d = np.mean(d_list) + 1  #- это если все коэффициенты равны 1

        # находим оптимальные коэффициенты
        def opt(coef):
            """
            coef - двумерный массив: в каждой строке - коэффициенты на всех рёбрах графа;
              строк столько, сколько входящих связей у текущей вершины
            """

            #print(coef)

            def g(a):
                #print(a)
                c = np.zeros(len(G.edges))
                for j in range(len(coef)):
                    #print(c)
                    #print(np.array(coef[j]) * a[j])
                    c += np.array(coef[j]) * a[j]
                #for e in range(len(G.edges)):
                #print("c_old =", c)
                # здесь нужно прибавить a[j] к c[j] для каждого j-го ребра
                for k in range(len(coef)):
                    u = vert_list[k]
                    j = G.edges[v, u]['num']
                    c[j] += a[k]
                #print("c_new =", c)
                   # print("k =", k, "j =", j, "u =", u)


                        #j = G.edges[v, u]['num']
                        #print(j)
                        #c[j] += a[vert_list.index(u)]


                    #u = G.edges.data()
                    #print(u)

                ans = np.sum(c ** 2)
                return ans

            bounds = Bounds([0] * len(coef), [1] * len(coef))
            linear_constraint = LinearConstraint([[1] * len(coef)], [1], [1])
            method = 'trust-constr'
            a0 = np.zeros(len(coef))
            a0[0] = 1.0
            res = minimize(g, a0, method=method,
                constraints=linear_constraint, options={'verbose': 0}, bounds=bounds)
            best_coef = res.x
            disp = res.fun

            coef_edges = np.zeros(len(G.edges))
            for j in range(len(coef)):
                coef_edges += np.array(coef[j]) * best_coef[j]
            # здесь нужно прибавить a[j] к c[j] для каждого j-го ребра
            for k in range(len(coef)):
                u = vert_list[k]
                j = G.edges[v, u]['num']
                coef_edges[j] += best_coef[k]

            return disp, best_coef, coef_edges

        d, _, cc = opt(coef_list)
        #print(d, cc)

        if min_d is None or d < min_d:
            min_d = d
            min_node = v
            min_cc = cc
        #d = np.mean([G.nodes[u]['d'] for u in G.adj[v] if G.nodes[u]['d'] is not None])
    #        if G.nodes[v]['d'] is not None and (min_d is None or d < min_d):
    #            min_d = d
    #            min_node = v

    print("min_d =", min_d, "min_cc =", min_cc)

    G.nodes[min_node]['d'] = min_d
    visited.add(min_node)
    G.nodes[min_node]['coef'] = min_cc
    print(min_node, "<-", min_d)
