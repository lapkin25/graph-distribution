import networkx as nx
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, minimize
import random



G = nx.Graph()

#G.add_nodes_from([1, 2, 3, 4])
#G.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 4), (2, 3)])

#G.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8, 9])
#G.add_edges_from([(1, 2), (2, 3), (2, 4), (4, 5), (3, 5),
#                  (5, 6), (6, 7), (7, 8), (8, 9), (1, 9), (4, 8)])

#G = nx.karate_club_graph()
# https://networkx.org/documentation/stable/auto_examples/algorithms/plot_girvan_newman.html

"""
# пример из статьи: Li et al. Efficient algorithms for finding diversified
# top-k structural hole spanners in social networks (2022)
G.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30])
G.add_edges_from([(1, 11), (1, 10), (1, 5), (1, 6),
                  (2, 5), (2, 6), (2, 7),
                  (3, 8), (3, 27), (3, 28),
                  (4, 9), (4, 27), (4, 13),
                  (5, 16), (5, 17), (5, 18),
                  (6, 19), (6, 20), (6, 21),
                  (7, 9), (7, 23), (7, 8), (7, 24),
                  (8, 23), (8, 24),
                  (9, 24),
                  (10, 14), (10, 15), (10, 11),
                  (11, 12), (11, 15),
                  (12, 14),
                  (13, 25), (13, 26),
                  (14, 15),
                  (16, 17),
                  (19, 21),
                  (20, 22),
                  (21, 22),
                  (23, 24),
                  (25, 26),
                  (27, 28), (27, 29), (27, 30),
                  (28, 29), (28, 30),
                  (29, 30)])
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

G = nx.krackhardt_kite_graph()

"""
G.add_nodes_from(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o'])
G.add_edges_from([('a', 'd'), ('b', 'd'), ('b', 'e'), ('c', 'e'), ('d', 'e'), ('d', 'f'),
                  ('e', 'g'), ('f', 'h'), ('g', 'h'), ('h', 'i'),
                  ('i', 'j'), ('i', 'k'), ('i', 'l'), ('j', 'k'),
                  ('l', 'm'), ('l', 'n'), ('l', 'o')])
"""

source = 3  #'a'



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

        # TODO: добавить gamma - вектор коэффициентов при дополнительных шумах в вершинах графа
        # TODO: сделать дисперсии на ребрах не только единичными (чтобы они задавались)

        alpha_v = np.array([new_alpha[graph.edges[u, v]['num']] for u, _ in graph.in_edges(v)])
        # оптимизируем alpha_v
        bounds = Bounds([0] * len(alpha_v), [1] * len(alpha_v))
        A = np.ones((1, len(alpha_v)))
        rhs = np.ones(1)
        linear_constraint = LinearConstraint(A, rhs, rhs)
        res = minimize(calc_variance, alpha_v, method='SLSQP', # method='trust-constr',
                       constraints=linear_constraint)  #, bounds=bounds)  #, options={'verbose': 1})
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
# TODO: вычислить расстояние между предыдущим и следующим приближениями

for i in range(len(digraph.edges())):
    print(list(digraph.edges())[i], '->', alpha[i])


# Расчет матрицы дисперсий между всеми парами вершин...

var_matrix = np.zeros((len(G.nodes), len(G.nodes)))  # матрица дисперсий
nodes_list = []  # все вершины графа в порядке перечисления
cnt = 0
alpha_history = []
beta_history = [[] for _ in range(len(G.nodes()))]
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
    alpha_history.append(alpha)
    src_ind = digraph.nodes[src]['vert_num']
    beta_history[src_ind] = beta
    var_matrix[cnt, :] = np.sum(beta ** 2, axis=1)
    nodes_list.append(src)
    cnt += 1
    #print("alpha = ", alpha)
    #print("beta = ", beta)
    #print("variance = ", np.sum(beta ** 2, axis=1))
print("\nМатрица дисперсий:")
print(var_matrix)
print("Вершины:")
print(nodes_list)
print("Средние дисперсии для разных источников:")
print(np.mean(var_matrix, axis=1))  # TODO: разобраться, axis=1 - это усреднение по источникам или стокам?
print("Коэффициенты alpha:")
for line in alpha_history:
    print(line)
print("Средние alpha:")
print(np.mean(np.vstack(alpha_history), axis=1))
#beta_mean = np.mean(np.vstack(beta_history), axis=1)
#print("Средние beta:")
#print(beta_mean)

"""
rho = np.zeros((len(G.nodes()), len(G.nodes())))
# Расчет суммы beta по исходящим ребрам
for src in digraph.nodes():
    for v in digraph.nodes():
        for v, w, data in digraph.out_edges(v, data=True):
            # w - вершина, в которую идет ребро из v
            src_ind = digraph.nodes[src]['vert_num']
            v_ind = digraph.nodes[v]['vert_num']
            edge_ind = data['num']
            rho[src, v] += beta_history[src_ind][v_ind, edge_ind]

print("rho = ")
print(rho)
print("mean rho =", np.mean(rho, axis=1))
# какой будет средняя ошибка на графе, если источником будет выбранная вершина?
"""


# Расчет для каждого ребра e средней величины beta[v, e], где u - источник
# (среднее участие ребра при передаче информации по графу - аналог betweenness)
avg_beta = np.zeros(len(digraph.edges()))
avg_beta_2 = np.zeros(len(digraph.edges()))
for edge_ind in range(len(digraph.edges())):
    avg_beta[edge_ind] = np.mean(np.array(
        [[beta_history[src_ind][v_ind, edge_ind] for v_ind in range(len(digraph.nodes()))] for src_ind in range(len(digraph.nodes()))]))
    avg_beta_2[edge_ind] = np.mean(np.array(
        [[beta_history[src_ind][v_ind, edge_ind] ** 2 for v_ind in range(len(digraph.nodes()))] for src_ind in range(len(digraph.nodes()))]))
print("Ребра ", digraph.edges())
print("avg_beta = ", avg_beta)
for i, (val, val2) in enumerate(zip(avg_beta, avg_beta_2)):
    print(edges_list[i], '->', val, ';', val2)



"""
import pandas as pd
from centralities import compute_centralities, calc_ranking

df = pd.DataFrame()
df['vert'] = nodes_list
df['our'] = np.mean(var_matrix, axis=1)
df['our_rank'] = calc_ranking(df['our'], method="descending")

df1 = compute_centralities(G, nodes_list)
df = pd.concat([df, df1], axis=1)

df.to_excel('result.xlsx', sheet_name='Лист1', index=False)
"""

import matplotlib.pyplot as plt

# Вычисляем позиции узлов (алгоритм spring_layout помогает избежать наложения)
pos = nx.spring_layout(G, seed=42)

# Рисуем граф
nx.draw(
    G,
    pos,
    with_labels=True,  # Показывать метки узлов  # убрать, если надо поменять метки
    node_color="lightblue",  # Цвет узлов
    node_size=600,  # Размер узлов
    font_size=12,  # Размер шрифта меток
    font_weight="bold",  # Жирность шрифта
    arrows=True  # Для DiGraph стрелки рисуются по умолчанию
)

# Теперь добавляем метки
#nx.draw_networkx_labels(G, pos=pos, labels=dict(zip(range(0, 10), range(1,11))), font_size=10)

plt.savefig("fig2.eps", format='eps')
# Показываем график
plt.show()
