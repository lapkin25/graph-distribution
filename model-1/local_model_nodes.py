import networkx as nx
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, minimize
import random



G = nx.Graph()

G.add_nodes_from([1, 2, 3, 4])
G.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 4), (2, 3)])

#G.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8, 9])
#G.add_edges_from([(1, 2), (2, 3), (2, 4), (4, 5), (3, 5),
#                  (5, 6), (6, 7), (7, 8), (8, 9), (1, 9), (4, 8)])

#G = nx.karate_club_graph()
# https://networkx.org/documentation/stable/auto_examples/algorithms/plot_girvan_newman.html


"""
G.add_nodes_from(list(range(1, 37)))
G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
                  (1, 7), (2, 8), (3, 9), (4, 10), (5, 11), (6, 12),
                  (7, 8), (8, 9), (9, 10), (10, 11), (11, 12),
                  (7, 13), (8, 14), (9, 15), (10, 16), (11, 17), (12, 18),
                  (13, 14), (14, 15), (15, 16), (16, 17), (17, 18),
                  (13, 19), (14, 20), (15, 21), (16, 22), (17, 23), (18, 24),
                  (19, 20), (20, 21), (21, 22), (22, 23), (23, 24),
                  (19, 25), (20, 26), (21, 27), (22, 28), (23, 29), (24, 30),
                  (25, 26), (26, 27), (27, 28), (28, 29), (29, 30),
                  (25, 31), (26, 32), (27, 33), (28, 34), (29, 35), (30, 36),
                  (31, 32), (32, 33), (33, 34), (34, 35), (35, 36)])
"""

"""
G.add_nodes_from(list(range(1, 37)))
G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
                  (1, 7), (2, 8), (3, 9), (4, 10), (5, 11), (6, 12),
                  (7, 8), (8, 9), (9, 10), (10, 11), (11, 12),
                  (7, 13), (8, 14), (9, 15), (10, 16), (11, 17), (12, 18),
                  (13, 14), (14, 15), (15, 16), (16, 17), (17, 18),
                  (13, 19), (14, 20), (15, 21), (16, 22), (17, 23), (18, 24),
                  (19, 20), (20, 21), (21, 22), (22, 23), (23, 24),
                  (19, 25), (20, 26), (21, 27), (22, 28), (23, 29), (24, 30),
                  (25, 26), (26, 27), (27, 28), (28, 29), (29, 30),
                  (25, 31), (26, 32), (27, 33), (28, 34), (29, 35), (30, 36),
                  (31, 32), (32, 33), (33, 34), (34, 35), (35, 36),
                  (2, 7), (3, 8), (4, 9), (5, 10), (6, 11),
                  (8, 13), (9, 14), (10, 15), (11, 16), (12, 17),
                  (14, 19), (15, 20), (16, 21), (17, 22), (18, 23),
                  (20, 25), (21, 26), (22, 27), (23, 28), (24, 29),
                  (26, 31), (27, 32), (28, 33), (29, 34), (30, 35)])
"""

"""
G.add_nodes_from(list(range(1, 46)))
G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
                  (1, 7), (2, 8), (3, 9), (4, 10), (5, 11), (6, 12),
                  (7, 8), (8, 9), (9, 10), (10, 11), (11, 12),
                  (7, 13), (8, 14), (9, 15), (10, 16), (11, 17), (12, 18),
                  (13, 14), (14, 15), (15, 16), (16, 17), (17, 18),
                  (13, 19), (14, 20), (15, 21), (16, 22), (17, 23), (18, 24),
                  (19, 20), (20, 21), (21, 22), (22, 23), (23, 24),
                  (19, 25), (20, 26), (21, 27), (22, 28), (23, 29), (24, 30),
                  (25, 26), (26, 27), (27, 28), (28, 29), (29, 30),
                  (25, 31), (26, 32), (27, 33), (28, 34), (29, 35), (30, 36),
                  (31, 32), (32, 33), (33, 34), (34, 35), (35, 36),

                  (36, 37), (37, 38), (38, 39), (37, 40), (38, 41), (39, 42),
                  (40, 41), (41, 42), (40, 43), (41, 44), (42, 45),
                  (43, 44), (44, 45)])
"""

"""
G.add_nodes_from(list(range(1, 46)))
G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
                  (1, 7), (2, 8), (3, 9), (4, 10), (5, 11), (6, 12),
                  (7, 8), (8, 9), (9, 10), (10, 11), (11, 12),
                  (7, 13), (8, 14), (9, 15), (10, 16), (11, 17), (12, 18),
                  (13, 14), (14, 15), (15, 16), (16, 17), (17, 18),
                  (13, 19), (14, 20), (15, 21), (16, 22), (17, 23), (18, 24),
                  (19, 20), (20, 21), (21, 22), (22, 23), (23, 24),
                  (19, 25), (20, 26), (21, 27), (22, 28), (23, 29), (24, 30),
                  (25, 26), (26, 27), (27, 28), (28, 29), (29, 30),
                  (25, 31), (26, 32), (27, 33), (28, 34), (29, 35), (30, 36),
                  (31, 32), (32, 33), (33, 34), (34, 35), (35, 36),

                  (12, 37), (37, 38), (38, 39), (37, 40), (38, 41), (39, 42),
                  (18, 40), (40, 41), (41, 42), (40, 43), (41, 44), (42, 45),
                  (24, 43), (43, 44), (44, 45)])
"""


source = 1

noise_edges = np.ones(2 * len(G.edges))

noise_nodes = np.zeros(len(G.nodes))
#noise_nodes[2] = 1.0



def get_initial_alphas(graph, start):
    """
    Вход: graph - орграф
          start - начальная вершина
    Выход: alpha - начальное приближение для коэффициентов
             (распределение поровну по рёбрам, входящим в каждую вершину)
           beta - матрица коэффициентов шумов:
             beta[v, e] - это коэффициент сигнала, пришедшего в вершину v, при шуме на ребре e
           gamma - матрица коэффициентов шумов в вершинах:
             gamma[v, u] - это коэффициент сигнала, пришедшего в вершину v, при шуме в вершине u
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
    gamma = np.ones((len(graph.nodes()), len(graph.nodes())))
    gamma[graph.nodes[start]['vert_num'], :] = np.zeros(len(graph.nodes()))  # ??? источник шума не создает
    for v, _, data in graph.in_edges(start, data=True):
        alpha[data['num']] = 0.0
    return alpha, beta, gamma


def improve_alphas(graph, start, cur_alpha, cur_beta, cur_gamma):
    """
    Итоговый шум сигнала в вершине графа складывается из шумов
      вследствие помех передачи по ребрам и шумов вследствие зашумления сигнала в вершинах

    Вход: graph - орграф
          cur_alpha - коэффициенты на всех ребрах
          cur_beta - матрица шумовых коэффициентов (на всех ребрах) в каждой вершине
          cur_gamma - матрица шумовых коэффициентов (в каждой вершине)
    Выход: new_alpha - улучшенные коэффициенты на всех рёбрах
           new_beta - улучшенная матрица шумовых коэффициентов
           new_gamma - улучшенная матрица шумовых коэффициентов в вершинах
    """
    new_alpha = cur_alpha[:]
    new_beta = cur_beta[:, :]
    new_gamma = cur_gamma[:, :]
    nodes_list = list(graph.nodes())
    random.shuffle(nodes_list)
    for v in nodes_list:
        if v == start:
            continue

        # оптимизируем коэффициенты при сигналах, пришедших в вершину v ...
        num_alphas = graph.in_degree(v)

        def calc_beta_gamma(alpha_v):
            beta_v = np.zeros(len(graph.edges()))
            gamma_v = np.zeros(len(graph.nodes()))
            for i, (u, _, data) in enumerate(graph.in_edges(v, data=True)):
                beta_v += alpha_v[i] * new_beta[graph.nodes[u]['vert_num'], :]
                beta_v[data['num']] += alpha_v[i]
                gamma_v += alpha_v[i] * new_gamma[graph.nodes[u]['vert_num'], :]
            gamma_v[graph.nodes[v]['vert_num']] += 1.0
            # TODO: вывести посчитанный вектор gamma_v, проверить значение в источнике
            return beta_v, gamma_v

        def calc_variance(alpha_v):
            beta_v, gamma_v = calc_beta_gamma(alpha_v)
            return np.dot(noise_edges, beta_v ** 2) + np.dot(noise_nodes, gamma_v ** 2)

        # TODO: добавить gamma - вектор коэффициентов при дополнительных шумах в вершинах графа
        # TODO: сделать дисперсии на ребрах не только единичными (чтобы они задавались)

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
        (new_beta[graph.nodes[v]['vert_num'], :],
         new_gamma[graph.nodes[v]['vert_num'], :]) = calc_beta_gamma(alpha_v)
        # TODO: сразу же обновить beta во всех других вершинах (кроме start)?

    return new_alpha, new_beta, new_gamma



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

alpha0, beta0, gamma0 = get_initial_alphas(digraph, source)
print(digraph.edges())
print(alpha0)
print(beta0)
print(gamma0)
alpha = alpha0[:]
beta = beta0[:, :]
gamma = gamma0[:, :]

num_steps = 30

for step in range(num_steps):
    print(f"Шаг {step + 1}")
    alpha, beta, gamma = improve_alphas(digraph, source, alpha, beta, gamma)
    print("alpha = ", alpha)
    #print("beta = ", beta)
    print("gamma = ", gamma)
    #print("variance = ", np.sum(beta ** 2, axis=1))
    print("variance = ", np.dot(noise_edges, beta.T ** 2) + np.dot(noise_nodes, gamma.T ** 2))
print("\nОтвет:")
print(digraph.edges())
print("alpha = ", alpha)
#print("beta = ", beta)
#print("variance = ", np.sum(beta ** 2, axis=1))
print("variance = ", np.dot(noise_edges, beta.T ** 2) + np.dot(noise_nodes, gamma.T ** 2))
# TODO: вычислить расстояние между предыдущим и следующим приближениями


# Расчет матрицы дисперсий между всеми парами вершин...
"""
var_matrix = np.zeros((len(G.nodes), len(G.nodes)))  # матрица дисперсий
nodes_list = []  # все вершины графа в порядке перечисления
cnt = 0
for src in G.nodes():
    print("\n\nИсточник =", src)
    # вычисление начальных приближений для коэффициентов
    alpha0, beta0 = get_initial_alphas(digraph, src)
    alpha = alpha0[:]
    beta = beta0[:, :]
    # итерации...
    print("Шаги: ")
    for step in range(num_steps):
        print(f" {step + 1}", end='')
        alpha, beta = improve_alphas(digraph, src, alpha, beta)
    var_matrix[cnt, :] = np.sum(beta ** 2, axis=1)  # TODO: поправить с gamma
    nodes_list.append(src)
    cnt += 1
    #print("alpha = ", alpha)
    #print("beta = ", beta)
    #print("variance = ", np.sum(beta ** 2, axis=1))
print("Матрица дисперсий:")
print(var_matrix)
print("Вершины:")
print(nodes_list)
print("Средние дисперсии для разных источников:")
print(np.mean(var_matrix, axis=1))
"""
