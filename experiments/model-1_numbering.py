import networkx as nx
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, minimize
import random
import math



G = nx.Graph()

#G.add_nodes_from([1, 2, 3, 4])
#G.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 4), (2, 3)])

G.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8, 9])
G.add_edges_from([(1, 2), (2, 3), (2, 4), (4, 5), (3, 5),
                  (5, 6), (6, 7), (7, 8), (8, 9), (1, 9), (4, 8)])

#G = nx.karate_club_graph()

source = 2
destination = 8


"""
Начало раздела "функции"
"""


"""
НУМЕРАЦИЯ - что это такое?
Массив, в котором для каждого номера указан id вершины
"""

def get_initial_numbering(G, start, finish):
    """
    Вход: G - неориентированный граф
          start - начальная вершина
          finish - конечная вершина
    Выход: нумерация вершин графа G -
      чтобы соответствующая ориентировка получилась корректной
    """
    # Вычисляем порядок обхода BFS...
    numbering = [0] * len(G.nodes)
    k = 0
    numbering[0] = G.nodes[start]['vert_num']
    for u, v in nx.bfs_edges(G, start):
        k += 1
        numbering[k] = G.nodes[v]['vert_num']
    return numbering


def orientation_by_numbering(G, numbering):
    """
    Вход: G - неориентированный граф
          numbering - нумерация вершин графа
    Выход: G' (орграф) - ориентировка графа G, индуцированная нумерацией
      (дуги орграфа направлены от меньших номеров к большим)
    """
    #print(numbering)
    # Направляем рёбра от меньших номеров к большим...
    G1 = nx.DiGraph()
    # добавить к орграфу ребра неориентированного графа
    for u, v, data in G.edges(data=True):
        u_index = numbering.index(G.nodes[u]['vert_num'])
        v_index = numbering.index(G.nodes[v]['vert_num'])
        if u_index < v_index:
            G1.add_edge(u, v, num=data['num'])
        else:
            G1.add_edge(v, u, num=data['num'])
    return G1


def is_orientation_correct(orientation, start, finish):
    """
    Вход: orientation - орграф
          start - начальная вершина
          finish - конечная вершина
    Выход: является ли ориентировка корректной, то есть:
      а) в каждой вершине (кроме start) есть входящие рёбра
      -- б) в каждой вершине (кроме finish) есть исходящие рёбра
      в) в вершине start нет входящих рёбер
      -- г) в вершине finish нет исходящих рёбер
      д) вершина finish достижима из вершины start
      е) в графе нет циклов
    """
    # а)
    if not all([orientation.in_degree(v) != 0 for v in orientation.nodes() if v != start]):
       # print('а)')
        return False
    # б)
    #if not all([orientation.out_degree(v) != 0 for v in orientation.nodes() if v != finish]):
    #    return False
    # в)
    if orientation.in_degree(start) > 0:
       # print('в)')
        return False
    # г)
    #if orientation.out_degree(finish) > 0:
    #    return False
    # д)
    if not nx.has_path(orientation, start, finish):
       # print('д)')
        return False
    # е)
    if not nx.is_directed_acyclic_graph(orientation):
       # print('е)')
        return False
    # если все условия а)-е) выполняются
    return True


def calc_variance(orientation, alpha, start, finish):
    """
    Вход: orientation - орграф (ориентировка)
          alpha - вектор коэффициентов (на всех рёбрах)
          start - начальная вершина
          finish - конечная вершина
    Выход: variance - вектор дисперсий сигнала во всех вершинах
    """
    # проверить корректность ориентировки
    if not is_orientation_correct(orientation, start, finish):
        print("Некорректная ориентировка!")
        print(orientation.edges())
        print('start = ', start, '; finish = ', finish)
        print("nodes_list = ", nodes_list)
        raise
    # определить порядок обработки вершин графа (топологическая сортировка)
    topsort = list(nx.topological_sort(orientation))

    # Посчитать коэффициенты при шумах на всех рёбрах...
    # словарь "вершина -> массив коэффициентов при шумах на всех рёбрах"
    beta = {start: np.zeros(len(orientation.edges()))}
    # для каждой вершины...
    for u in topsort:
        beta[u] = np.zeros(len(orientation.edges()))
        # перебрать все входящие рёбра
        for v, _, data in orientation.in_edges(u, data=True):
            # v - вершина, из которой идёт ребро в u
            alpha_v = alpha[data['num']]  # коэффициент на ребре (v, u)
            # рассчитываем коэффициенты в вершине u
            beta[u] += alpha_v * beta[v]
            beta[u][data['num']] += alpha_v * 1.0  # единичная дисперсия всех шумов
            # TODO: поменять 1 на произвольные числа на рёбрах

    # Вычислить дисперсии во всех вершинах как сумму квадратов коэффициентов...
    variance = {}  # словарь "вершина -> дисперсия в этой вершине"
    for v in orientation.nodes():
        if v in beta:
            variance[v] = np.sum(beta[v] ** 2)
        else:
            variance[v] = np.inf

    return variance


def get_initial_alphas(orientation):
    """
    Вход: orientation - орграф (ориентировка)
    Выход: alpha - начальное приближение для коэффициентов
      (распределение поровну по рёбрам, входящим в каждую вершину)
    """
    num_alphas = len(orientation.edges())
    alpha = np.zeros(num_alphas)
    for u in orientation.nodes():
        num_incoming = orientation.in_degree(u)
        for v, _, data in orientation.in_edges(u, data=True):
            # v - вершина, из которой идёт ребро в u
            ind = data['num']  # индекс ребра (v, u)
            alpha[ind] = 1. / num_incoming
    return alpha


def optimize_coefs(orientation, initial_alpha, start, finish):
    """
    Вход: orientation - орграф (ориентировка)
          initial_alpha - начальное приближение для вектора коэффициентов (на всех рёбрах)
          start - начальная вершина
          finish - конечная вершина
    Выход: optimal_alpha - оптимальный вектор коэффициентов, обеспечивающий
      минимум дисперсии сигнала в конечной вершине
    """
    # целевая функция для оптимизации
    def objective_function(alpha):
        return calc_variance(orientation, alpha, start, finish)[finish]

    # число переменных - это число рёбер
    len_alpha = len(initial_alpha)
    # ограничения: каждая переменная от 0 до 1
    bounds = Bounds([0] * len_alpha, [1] * len_alpha)
    # линейные ограничения: сумма переменных по входящим рёбрам равна 1
    # - заполняем матрицу A: строки - это ограничения, столбцы - это переменные
    num_constraints = sum([1 for v in orientation.nodes() if orientation.in_degree(v) > 0])
    A = np.zeros((num_constraints, len_alpha))
    k = 0  # счётчик ограничений
    for u in orientation.nodes():
        #if u != start:
        if orientation.in_degree(u) > 0:
            # во всех вершинах, кроме стартовой, есть входящие рёбра
            # ???
            for v, _, data in orientation.in_edges(u, data=True):
                # v - вершина, из которой идёт ребро в u
                ind = data['num']  # индекс ребра (v, u)
                A[k, ind] = 1.0
            k += 1
    # - заполняем вектор правых частей ограничений
    rhs = np.ones(num_constraints)
    # - создаем линейное ограничение типа "равенство"
    linear_constraint = LinearConstraint(A, rhs, rhs)
    # решение задачи оптимизации
    res = minimize(objective_function, initial_alpha, method='trust-constr',
                   constraints=linear_constraint, bounds=bounds)  #, options={'verbose': 1})
    optimal_alpha = res.x

    return optimal_alpha


def reverse_edge(orientation, u, v):
    """
    Вход: orientation - орграф (ориентировка)
          u, v - концы ребра (u, v) или (v, u)
    Выход: new_orientation - ориентировка, в которой развёрнуто ребро (u, v)
    """
    new_orientation = orientation.copy()
    if orientation.has_edge(u, v):
        num = orientation.edges[u, v]['num']
        new_orientation.remove_edge(u, v)
        new_orientation.add_edge(v, u, num=num)
    elif orientation.has_edge(v, u):
        num = orientation.edges[v, u]['num']
        new_orientation.remove_edge(v, u)
        new_orientation.add_edge(u, v, num=num)
    else:
        raise
    return new_orientation


def optimize_numbering(graph, start, finish, initial_numbering, verbose=False):
    """
    Вход: graph - неориентированный граф
          start - начальная вершина
          finish - конечная вершина
          initial_numbering - начальная нумерация
    Выход: оптимальная нумерация вершин, обеспечивающая
      минимум дисперсии сигнала в конечной вершине
    """
    # дисперсия при оптимальных коэффициентах (при заданной нумерации)
    def calc_optimal_variance(numbering):
        try:
            orientation = orientation_by_numbering(graph, numbering)
            initial_alpha = get_initial_alphas(orientation)
            optimal_alpha = optimize_coefs(orientation, initial_alpha, start, finish)
            return calc_variance(orientation, optimal_alpha, start, finish)[finish]
        except:
            return 1e10

    numbering = initial_numbering.copy()  # начинаем с начальной нумерации
    init_variance = calc_optimal_variance(numbering)
    if verbose:
        print(f"Начальная нумерация, дисперсия: {init_variance}")
    min_variance = init_variance
    # Меняем местами соседние вершины, пока можно уменьшить дисперсию...
    while True:
        numbering_changed = False  # флаг: поменялась ли ориентировка
        # TODO: начинать с последнего индекса, обойти массив по кругу
        for i in range(1, len(numbering) - 1):
            for j in range(i + 1, len(numbering) - 1):
                new_numbering = numbering.copy()
                #print(new_numbering)
                new_numbering[i], new_numbering[j] = new_numbering[j], new_numbering[i]
                #print(new_numbering)
                if not is_orientation_correct(orientation_by_numbering(graph, new_numbering), start, finish):
                    continue
                new_variance = calc_optimal_variance(new_numbering)
                if new_variance < min_variance:
                    min_variance = new_variance
                    numbering = new_numbering
                    numbering_changed = True
        if not numbering_changed:
            break
        else:
            if verbose:
                print(f"Улучшена нумерация, дисперсия: {min_variance}")
    return numbering



"""
Конец раздела "функции"
"""


# добавить служебную информацию к рёбрам графа
# нумерация ребер графа
edges_list = []
for i, e in enumerate(G.edges):
    G.edges[e]['num'] = i
    edges_list.append(e)
nodes_list = []
for i, v in enumerate(G.nodes):
    G.nodes[v]['vert_num'] = i + 100
    nodes_list.append(v)


# Расчет матрицы дисперсий при передаче сигнала между всеми парами вершин...
ans = {}
for s in G.nodes():
    for t in G.nodes():
        if s == t:
            continue
        numbering0 = get_initial_numbering(G, s, t)
        optimal_numbering = optimize_numbering(G, s, t, numbering0, verbose=True)
        optimal_orientation = orientation_by_numbering(G, optimal_numbering)
        alpha0 = get_initial_alphas(optimal_orientation)
        opt_alpha = optimize_coefs(optimal_orientation, alpha0, s, t)
        var = calc_variance(optimal_orientation, opt_alpha, s, t)
        ans[s, t] = var[t]
        print(s, t, '->', "дисперсия", var[t])
        print(f"все дисперсии (s = {s}, t = {t}):", var)
        print("ориентировка:", optimal_orientation.edges)
# вывод матрицы
for s in G.nodes():
    for t in G.nodes():
        if s == t:
            r = 0
        else:
            r = ans[s, t]
        print("{:.2f}".format(r), end=' ')
    print()
