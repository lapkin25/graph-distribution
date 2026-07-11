import networkx as nx
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, minimize
import random



G = nx.Graph()

#G.add_nodes_from([1, 2, 3, 4])
#G.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 4), (2, 3)])

G.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8, 9])
G.add_edges_from([(1, 2), (2, 3), (2, 4), (4, 5), (3, 5),
                  (5, 6), (6, 7), (7, 8), (8, 9), (1, 9), (4, 8)])

#G = nx.karate_club_graph()
# https://networkx.org/documentation/stable/auto_examples/algorithms/plot_girvan_newman.html

source = 2



def get_initial_alphas(graph, start):
    """
    Вход: graph - орграф
          start - начальная вершина
    Выход: alpha - начальное приближение для коэффициентов
             (распределение поровну по рёбрам, входящим в каждую вершину)
           beta - матрица коэффициентов шумов:
             beta[v, e] - это коэффициент сигнала, пришедшего в вершину v, при шуме на ребре e
    """
    num_alphas = len(graph.edges())
    alpha = np.zeros(num_alphas)
    for u in graph.nodes():
        num_incoming = graph.in_degree(u)
        for v, _, data in graph.in_edges(u, data=True):
            # v - вершина, из которой идёт ребро в u
            ind = data['num']  # индекс ребра (v, u)
            alpha[ind] = 1. / num_incoming
    # пока заглушка - нулевая матрица beta
    #beta = np.zeros((len(graph.nodes()), len(graph.edges())))
    beta = np.ones((len(graph.nodes()), len(graph.edges())))
    beta[graph.nodes[start]['vert_num'], :] = np.zeros(len(graph.edges()))
    for v, _, data in graph.in_edges(start, data=True):
        alpha[data['num']] = 0.0
    return alpha, beta


def improve_alphas(graph, start, cur_alpha, cur_beta):
    """
    Вход: graph - орграф
          cur_alpha - коэффициенты на всех ребрах
          cur_beta - матрица шумовых коэффициентов (на всех ребрах) в каждой вершине
    Выход: new_alpha - улучшенные коэффициенты на всех рёбрах
           new_beta - улучшенная матрица шумовых коэффициентов
    """
    new_alpha = cur_alpha[:]
    new_beta = cur_beta[:, :]
    nodes_list = list(graph.nodes())
    random.shuffle(nodes_list)
    for v in nodes_list:
        if v == start:
            continue

        # оптимизируем коэффициенты при сигналах, пришедших в вершину v ...
        num_alphas = graph.in_degree(v)

        def calc_beta(alpha_v):
            beta_v = np.zeros(len(graph.edges()))
            for i, (u, _, data) in enumerate(graph.in_edges(v, data=True)):
                beta_v += alpha_v[i] * new_beta[graph.nodes[u]['vert_num'], :]
                beta_v[data['num']] += alpha_v[i] * 1.0  # единичная дисперсия всех шумов
            return beta_v

        def calc_variance(alpha_v):
            beta_v = calc_beta(alpha_v)
            return sum(beta_v ** 2)

        alpha_v = np.array([new_alpha[graph.edges[u, v]['num']] for u, _ in graph.in_edges(v)])
        # оптимизируем alpha_v
        bounds = Bounds([0] * len(alpha_v), [1] * len(alpha_v))
        A = np.ones((1, len(alpha_v)))
        rhs = np.ones(1)
        linear_constraint = LinearConstraint(A, rhs, rhs)
        res = minimize(calc_variance, alpha_v, method='trust-constr',
                       constraints=linear_constraint, bounds=bounds)  #, options={'verbose': 1})
        alpha_v = res.x
        for i, (u, _) in enumerate(graph.in_edges(v)):
            new_alpha[graph.edges[u, v]['num']] = alpha_v[i]
        new_beta[graph.nodes[v]['vert_num'], :] = calc_beta(alpha_v)
        # TODO: сразу же обновить beta во всех других вершинах (кроме start)?

    return new_alpha, new_beta



# создать такой же орграф
digraph = G.to_directed()

# добавить служебную информацию к рёбрам графа
# нумерация ребер графа
# (у двух симметричных ребер разные номера num)
edges_list = []
for i, e in enumerate(digraph.edges):
    digraph.edges[e]['num'] = i
    edges_list.append(e)
for i, v in enumerate(digraph.nodes):
    digraph.nodes[v]['vert_num'] = i

alpha0, beta0 = get_initial_alphas(digraph, source)
print(digraph.edges())
print(alpha0)
print(beta0)
alpha = alpha0[:]
beta = beta0[:, :]

num_steps = 30

for step in range(num_steps):
    print(f"Шаг {step + 1}")
    alpha, beta = improve_alphas(digraph, source, alpha, beta)
    print("alpha = ", alpha)
    #print("beta = ", beta)
    print("variance = ", np.sum(beta ** 2, axis=1))
print("\nОтвет:")
print(digraph.edges())
print("alpha = ", alpha)
#print("beta = ", beta)
print("variance = ", np.sum(beta ** 2, axis=1))
