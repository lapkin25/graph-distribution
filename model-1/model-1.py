import networkx as nx

G = nx.Graph()

G.add_nodes_from([1, 2, 3, 4])
G.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 4), (2, 3)])

source = 1
destination = 4


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

    # создать пустой орграф
    G1 = nx.DiGraph()
    # добавить к орграфу ребра неориентированного графа
    for u, v in G.edges():
        G1.add_edge(u, v)
    return G1


def is_orientation_correct(orientation, start, finish):
    """
    Вход: orientation - орграф
          start - начальная вершина
          finish - конечная вершина
    Выход: является ли ориентировка корректной, то есть:
      а) в каждой вершине (кроме start) есть входящие рёбра
      б) в каждой вершине (кроме finish) есть исходящие рёбра
      в) в вершине start нет входящих рёбер
      г) в вершине finish нет исходящих рёбер
      д) вершина finish достижима из вершины start
      е) в графе нет циклов
    """
    # а)
    if not all([orientation.in_degree(v) != 0 for v in orientation.nodes() if v != start]):
        return False
    # б)
    if not all([orientation.out_degree(v) != 0 for v in orientation.nodes() if v != finish]):
        return False
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


def calc_variance(orientation, alpha, start):
    """
    Вход: orientation - орграф (ориентировка)
          alpha - вектор коэффициентов (на всех рёбрах)
          start - начальная вершина
    Выход: variance - вектор дисперсий сигнала во всех вершинах
    """
    pass


def optimize_coefs(orientation, initial_alpha, start, finish):
    """
    Вход: orientation - орграф (ориентировка)
          initial_alpha - начальное приближение для вектора коэффициентов (на всех рёбрах)
          start - начальная вершина
          finish - конечная вершина
    Выход: optimal_alpha - оптимальный вектор коэффициентов, обеспечивающий
      минимум дисперсии сигнала в конечной вершине
    """
    pass


def optimize_orientation(graph, start, finish):
    """
    Вход: graph - неориентированный граф
          start - начальная вершина
          finish - конечная вершина
    Выход: оптимальная ориентировка рёбер, обеспечивающая
      минимум дисперсии сигнала в конечной вершине
    """
    pass



orientation0 = get_initial_orientation(G)
optimal_orientation = optimize_orientation(G, source, destination)


