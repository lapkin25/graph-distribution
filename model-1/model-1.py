import networkx as nx
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, minimize



G = nx.Graph()

G.add_nodes_from([1, 2, 3, 4, 5])
G.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 4), (2, 3), (4, 5)])

source = 1
destination = 5


"""
Начало раздела "функции"
"""

def get_initial_orientation(G):
    """
    Вход: G - неориентированный граф
    Выход: G' - ориентированный граф, полученный произвольной
      ориентировкой всех рёбер (каждое неориентированное ребро G
      превращается в одно ориентированное ребро G')
    """
    #G1 = nx.DiGraph.to_directed(G)
    # перебрать все рёбра; если есть симметричное, удалить его
    # (это плохая идея)

    # TODO: придётся перевернуть некоторые рёбра, чтобы получилась корректная ориентировка
    # создать пустой орграф
    G1 = nx.DiGraph()
    # добавить к орграфу ребра неориентированного графа
    for u, v, data in G.edges(data=True):
        G1.add_edge(u, v, num=data['num'])
    return G1


def is_orientation_correct(orientation, start, finish):
    """
    Вход: orientation - орграф
          start - начальная вершина
          finish - конечная вершина
    Выход: является ли ориентировка корректной, то есть:
      -- а) в каждой вершине (кроме start) есть входящие рёбра
      -- б) в каждой вершине (кроме finish) есть исходящие рёбра
      в) в вершине start нет входящих рёбер
      г) в вершине finish нет исходящих рёбер
      д) вершина finish достижима из вершины start
      е) в графе нет циклов
    """
    # а)
    #if not all([orientation.in_degree(v) != 0 for v in orientation.nodes() if v != start]):
    #    return False
    # б)
    #if not all([orientation.out_degree(v) != 0 for v in orientation.nodes() if v != finish]):
    #    return False
    # в)
    if orientation.in_degree(start) > 0:
        return False
    # г)
    if orientation.out_degree(finish) > 0:
        return False
    # д)
    if not nx.has_path(orientation, start, finish):
        return False
    # е)
    if not nx.is_directed_acyclic_graph(orientation):
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
        if u != start:
            # во всех вершинах, кроме стартовой, есть входящие рёбра
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


def optimize_orientation(graph, start, finish, initial_orientation, verbose=False):
    """
    Вход: graph - неориентированный граф
          start - начальная вершина
          finish - конечная вершина
          initial_orientation - начальная ориентировка (корректная)
    Выход: оптимальная ориентировка рёбер, обеспечивающая
      минимум дисперсии сигнала в конечной вершине
    """
    # дисперсия при оптимальных коэффициентах (при заданной ориентировке)
    def calc_optimal_variance(orientation):
        initial_alpha = get_initial_alphas(orientation)
        optimal_alpha = optimize_coefs(orientation, initial_alpha, start, finish)
        return calc_variance(orientation, optimal_alpha, start, finish)[finish]

    orientation = initial_orientation.copy()  # начинаем с начальной ориентировки
    # проверка корректности ориентировки
    if not is_orientation_correct(orientation, start, finish):
        raise
    min_variance = calc_optimal_variance(orientation)  # инициализация: минимальная дисперсия
    if verbose:
        print(f"Начальная ориентировка, дисперсия: {min_variance}")
    # Разворачиваем ребра, пока можно уменьшить дисперсию...
    while True:
        orientation_changed = False  # флаг: поменялась ли ориентировка
        best_orientation = None
        for u, v in graph.edges():
            # разворачиваем ребро (u, v) в ориентировке
            modified_orientation = reverse_edge(orientation, u, v)
            # проверка корректности ориентировки
            if is_orientation_correct(modified_orientation, start, finish):
                # если удалось уменьшить дисперсию, запомнить
                modified_variance = calc_optimal_variance(modified_orientation)
                if modified_variance < min_variance:
                    min_variance = modified_variance
                    best_orientation = modified_orientation
                    orientation_changed = True
        if orientation_changed:
            orientation = best_orientation
            if verbose:
                print(f"Улучшена ориентировка, дисперсия: {min_variance}")
        else:
            break
    return orientation


"""
Конец раздела "функции"
"""


# добавить служебную информацию к рёбрам графа
# нумерация ребер графа
edges_list = []
for i, e in enumerate(G.edges):
    G.edges[e]['num'] = i
    edges_list.append(e)


orientation0 = get_initial_orientation(G)
"""
orientation0 = nx.DiGraph()
orientation0.add_nodes_from([1, 2, 3, 4])
orientation0.add_edges_from([(1, 2, {'num': 0}), (1, 3, {'num': 1}), (2, 4, {'num': 2}), (4, 3, {'num': 3}), (2, 3, {'num': 4}), (4, 5, {'num': 5})])
"""
optimal_orientation = optimize_orientation(G, source, destination, orientation0, verbose=True)
#optimal_orientation = orientation0

alpha0 = get_initial_alphas(optimal_orientation)
opt_alpha = optimize_coefs(optimal_orientation, alpha0, source, destination)
print(f"Источник: {source}\nКонечная вершина: {destination}")
print("Коэффициенты alpha на ориентированных рёбрах:")
for i, (u, v) in enumerate(optimal_orientation.edges()):
    print(u, v, "->", opt_alpha[i])
var = calc_variance(optimal_orientation, opt_alpha, source, destination)
print("Дисперсии на вершинах:")
for v in optimal_orientation.nodes():
    print(v, "->", var[v])

#print(optimize_coefs(orientation0, alpha0, 1, 4))
#print(calc_variance(orientation0, [1., 1., 0.5, 0., 0.5], 1, 4))
#print(orientation0.edges())

"""
import matplotlib.pyplot as plt

# Вычисляем позиции узлов (алгоритм spring_layout помогает избежать наложения)
pos = nx.spring_layout(orientation0, seed=42)

# Рисуем граф
nx.draw(
    orientation0,
    pos,
    with_labels=True,  # Показывать метки узлов
    node_color="lightblue",  # Цвет узлов
    node_size=1500,  # Размер узлов
    font_size=12,  # Размер шрифта меток
    font_weight="bold",  # Жирность шрифта
    arrows=True  # Для DiGraph стрелки рисуются по умолчанию
)

# Показываем график
plt.show()
"""
