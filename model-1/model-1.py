import networkx as nx

G = nx.Graph()

G.add_nodes_from([1, 2, 3, 4])
G.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 4), (2, 3)])


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
    pass


def calc_variance(orientation, alpha, start):
    """
    Вход: orientation - орграф (ориентировка)
          alpha - вектор коэффициентов (на всех рёбрах)
          start - начальная вершина
    Выход: variance - вектор дисперсий сигнала во всех вершинах
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
#print(orientation0)

