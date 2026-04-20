import networkx as nx
from scipy.optimize import Bounds, LinearConstraint, minimize
import numpy as np


class Bracket:
    def __init__(self, node, brackets_list, adj_list):
        self.node = node
        self.branches = []
        self.adj_nodes = []
        self.edges = []
        # в списках branches, edges, adj_nodes равное число элементов
        for br, adj_node in zip(brackets_list, adj_list):
            self.branches.append(br)
            self.adj_nodes.append(adj_node)
            self.edges.append(G.edges[node, adj_node]['num'])

    def print(self, indentation=0):
        print(' ' * indentation, '[')
        print(' ' * indentation, f'Вершина {self.node}:')
        print(' ' * indentation, f'Число развилок: {len(self.branches)}')
        for i in range(len(self.branches)):
            print(' ' * indentation, f'Ребро #{self.edges[i]} в {self.adj_nodes[i]}')
            self.branches[i].print(indentation + 1)
        print(' ' * indentation, ']')


def backtracking(G, source, current, stack):
    if current == source:
        return Bracket(source, [], [])

    brackets_list = []
    adj_list = []
    for u in G.adj[current]:
        if u not in stack:
            stack.append(u)
            res = backtracking(G, source, u, stack)
            stack.pop()
            if res is not None:
                brackets_list.append(res)
                adj_list.append(u)
    if len(brackets_list) == 0:
        return None
    else:
        br = Bracket(current, brackets_list, adj_list)
        return br

def get_bracket(G, source, destination):
    return backtracking(G, source, destination, [destination])

def tree_search(br, coefs, product, lam_count, uniform_lambdas, lambdas=None, lambdas_groups=None, verbose=False, indentation=0, suboptimal_lambdas=None, nodes_var=None, sub_coefs=None):
    # TODO: передать еще префикс маршрута, чтобы узнать, что значит конкретная lambda
    # TODO: написать для этого метод класса Bracket, отвечающий за структуру дерева
    if verbose:
        #print(' ' * indentation, "lam_count =", lam_count)
        print(' ' * indentation, f"Вершина {br.node}: {len(br.branches)} разветвлений: ребра {br.edges} в вершины {br.adj_nodes}")
        #print(coefs, product)
    if len(br.branches) == 0:
        return 0.0, 0, np.zeros(len(G.edges)), 0.0, np.zeros(len(G.edges))
    if lambdas is None:
        uniform_lam = 1.0 / len(br.branches)
    num_coef = 0
    if len(br.branches) > 1:
        if verbose:
            for i in range(len(br.branches)):
                print(' ' * indentation, f"lambda[{lam_count + i}] ", end='')
            print()
        num_coef += len(br.branches)
        for i in range(len(br.branches)):
            uniform_lambdas.append(0.0)
        if lambdas_groups is not None:
            lambdas_groups.append(len(br.branches))
    branch_coefs = np.zeros((len(br.branches), len(G.edges)))
    lambda_ind = [0.0] * len(br.branches)


    #if sub_coefs is not None:
    #    sub_coefs = [0.0] * len(G.edges)

    cur_coefs = [0.0] * len(G.edges)

    sum_var = 0.0  # TODO: убрать эту переменную

    for i in range(len(br.branches)):
        if lambdas is None:
            lam = uniform_lam
        else:
            if len(br.branches) == 1:
                lam = 1.0
            else:
                lam = lambdas[lam_count + i]
        if len(br.branches) > 1:
            uniform_lambdas[lam_count + i] = lam
        coefs[br.edges[i]] += product * lam

        cur_coefs[br.edges[i]] += product * lam

        #if sub_coefs is not None:
        #    sub_coefs[br.edges[i]] += product * lam
        #cur_coefs[br.edges[i]] += product * lam

        #branch_coefs[br.edges[i]] += product * lam
        if len(br.branches) > 1:
            new_lam_count = lam_count + len(br.branches)
        else:
            new_lam_count = lam_count
        #num_coef += tree_search(br.branches[i], coefs, product * lam, new_lam_count, uniform_lambdas, lambdas, lambdas_groups, verbose, indentation + 1)[1]
        res = tree_search(br.branches[i], coefs, product * lam, lam_count + num_coef, uniform_lambdas, lambdas, lambdas_groups, verbose, indentation + 1, suboptimal_lambdas, nodes_var=nodes_var, sub_coefs=sub_coefs)
        #coefs[br.edges[i]] += product * lam
        #print("lam = ", lam)
        if suboptimal_lambdas is None:
            #print("res[2] =", res[2])
           # print("res[3] =", res[3])
            sum_var += (res[3] + 1) * lam ** 2
            cur_coefs += res[4]

        #if sub_coefs is not None:
        #    sub_coefs[br.edges[i]] -= product * lam
            #sub_coefs[br.edges[i]] += product * lam


        num_coef += res[1]
        if suboptimal_lambdas is not None:
            #print(res[2])
            branch_coefs[i, :] = res[2]
            branch_coefs[i, br.edges[i]] += 1
            lambda_ind[i] = lam_count + i
    if suboptimal_lambdas is None:
        #print("node =", br.node, " coefs =", coefs)
        if sub_coefs is not None:
            #print("sum_var =", sum_var)
            #nodes_var[br.node].append(float(sum([x ** 2 for x in sub_coefs])))
            #nodes_var[br.node].append(float(sum_var))
            nodes_var[br.node].append(float(sum([x ** 2 for x in cur_coefs])))
        return sum([x ** 2 for x in coefs]), num_coef, None, sum_var, np.array(cur_coefs)
    else:
        # находим субоптимальные lambda[k]
        new_coefs = np.zeros(len(G.edges))
        # new_coefs = sum_j ( branch_coefs[j, :] * lam[lambda_ind[j]] )
        # требуется заполнить значения suboptimal_lambdas[lambda_ind[i]] и new_coefs
        # аккуратно посчитать дисперсию = sum([x ** 2 for x in new_coefs])

        # TODO: попробовать решить задачу оптимизации аналитически
        def g(lam_coefs):
            # --- lam_coefs - вектор размерности (len(br.branches) - 1) ---
            # --- lam_coefs - вектор размерности len(br.branches)
            ans = 0
            terms = np.zeros(len(G.edges))
            for j in range(len(br.branches)):
                #if j == len(br.branches) - 1:
                #    lam = 1 - np.sum(lam_coefs)
                #else:
                #    lam = lam_coefs[j]
                lam = lam_coefs[j]
                for k in range(len(G.edges)):
                    terms[k] += lam * branch_coefs[j, k]
            #print("lam_coefs =", lam_coefs, "branch_coefs =", branch_coefs)
            #print("terms =", terms, "obj =", np.sum(terms ** 2))
            ans = np.sum(terms ** 2)
            return ans

        lams = np.zeros(len(br.branches))
        lams[0] = 1
        if len(br.branches) > 1:
            # оптимизируем lams
            bounds = Bounds([0] * len(br.branches), [1] * len(br.branches))
            linear_constraint = LinearConstraint([[1] * len(br.branches)], [1], [1])
            method = 'trust-constr'
            res = minimize(g, lams, method=method,
                           constraints=linear_constraint, options={'verbose': 0}, bounds=bounds)
            lams = res.x

        #print(' ' * indentation, "lams =", lams)
        #print(' ' * indentation, "branch_coefs =", branch_coefs)
        new_coefs = np.dot(lams, branch_coefs)
        if len(br.branches) > 1:
            for i in range(len(br.branches)):
                suboptimal_lambdas[lambda_ind[i]] = lams[i]

        """
        # проверка
        print(lambda_ind)
        lam = 1.0 / len(br.branches)
        new_coefs = np.sum(lam * branch_coefs, axis=0)
        if len(br.branches) > 1:
            for i in range(len(br.branches)):
                suboptimal_lambdas[lambda_ind[i]] = lam
        """


        return sum([x ** 2 for x in new_coefs]), num_coef, new_coefs

def calc_variance_uniformly(br):
    coefs = [0.0] * len(G.edges)
    lambdas = []
    ans = tree_search(br, coefs, 1.0, 0, lambdas)[0]
    print(lambdas)
    return ans

def calc_init_lambdas(br):
    coefs = [0.0] * len(G.edges)
    lambdas = []
    groups = []
    nodes_var = [[] for _ in range(len(G.nodes) + 1)]
    tree_search(br, coefs, 1.0, 0, lambdas, None, groups, nodes_var=nodes_var)
    return lambdas, groups

def count_lambdas(br):
    coefs = [0.0] * len(G.edges)
    nodes_var = [[] for _ in range(len(G.nodes) + 1)]
    return tree_search(br, coefs, 1.0, 0, [], verbose=True, nodes_var=nodes_var)[1]

def f(lambdas):
    #print("lambdas =", lambdas)
    coefs = [0.0] * len(G.edges)
    sub_coefs = [0.0] * len(G.edges)
    dummy = []
    nodes_var = [[] for _ in range(len(G.nodes) + 1)]
    return tree_search(br, coefs, 1.0, 0, dummy, lambdas, verbose=False, nodes_var=nodes_var, sub_coefs=sub_coefs)[0]


def calc_suboptimal_lambdas(br, lambdas_count):
    coefs = [0.0] * len(G.edges)
    uniform_lambdas = []
    lambdas = np.zeros(lambdas_count)
    variance, num_coef, new_coefs = tree_search(br, coefs, 1.0, 0, uniform_lambdas, None, suboptimal_lambdas=lambdas, verbose=False)
    print("new_coefs =", new_coefs)
    print("variance =", variance)
    print("lambdas =", lambdas)
    return lambdas


G = nx.Graph()

G.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8, 9])
G.add_edges_from([(1, 2), (2, 3), (2, 4), (4, 5), (3, 5),
                  (5, 6), (6, 7), (7, 8), (8, 9), (1, 9), (4, 8)])


"""
G.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
G.add_edges_from([(1, 2), (1, 3), (2, 4), (1, 4), (1, 5), (2, 3), (2, 6),
                  (3, 4), (3, 6), (4, 5), (4, 6), (5, 6), (5, 9), (5, 11),
                  (7, 8), (7, 10), (7, 9), (8, 9), (8, 10), (9, 10),
                  (11, 12), (11, 14), (12, 14), (13, 14), (11, 13), (12, 13)])
"""

#G = nx.karate_club_graph()


# нумерация ребер графа
edges_list = []
for i, e in enumerate(G.edges):
    G.edges[e]['num'] = i
    edges_list.append(e)

br = get_bracket(G, 1, 7)
#br.print()
print("Рёбра:", G.edges)
#print(calc_variance_uniformly(br))

num_lambdas = count_lambdas(br)
init_lambdas, lambdas_groups = calc_init_lambdas(br)
#print(init_lambdas, lambdas_groups)
print(num_lambdas)


print("Субоптимальное решение:")
print(f(calc_suboptimal_lambdas(br, num_lambdas)))

print("Оптимальное решение:")
bounds = Bounds([0] * num_lambdas, [1] * num_lambdas)

A = []
num_coef = 0
for gr in lambdas_groups:
    row = [0] * num_lambdas
    for i in range(num_coef, num_coef + gr):
        row[i] = 1
    num_coef += gr
    A.append(row)
#print(A)
#print(lambdas_groups)
if len(lambdas_groups) == 0:
    linear_constraint = None
    method = 'Nelder-Mead'
else:
    linear_constraint = LinearConstraint(A, [1] * len(lambdas_groups), [1] * len(lambdas_groups))
    method = 'trust-constr'

print("init = ", f(init_lambdas))

res = minimize(f, init_lambdas, method=method,
               constraints=linear_constraint, options={'verbose': 1}, bounds=bounds)
print(res.fun)
np.set_printoptions(precision=3, suppress=True)
print(res.x)

nodes_var = [[] for _ in range(len(G.nodes) + 1)]
coefs = [0.0] * len(G.edges)
sub_coefs = [0.0] * len(G.edges)
dummy = []
ans = tree_search(br, coefs, 1.0, 0, dummy, res.x, verbose=False, nodes_var=nodes_var, sub_coefs=sub_coefs)
print("nodes_var =", nodes_var)
print("cur_coefs =", ans[4])
#print(sum(x ** 2 for x in ans[4]))


"""

np.set_printoptions(precision=3, suppress=True)
mat = np.zeros((len(G.nodes), len(G.nodes)))
for v1 in G.nodes:
    for v2 in G.nodes:
        if v1 == v2:
            continue
        br = get_bracket(G, v1, v2)
        br.print()
        num_lambdas = count_lambdas(br)
        init_lambdas, lambdas_groups = calc_init_lambdas(br)

        bounds = Bounds([0] * num_lambdas, [1] * num_lambdas)
        A = []
        num_coef = 0
        for gr in lambdas_groups:
            row = [0] * num_lambdas
            for i in range(num_coef, num_coef + gr):
                row[i] = 1
            num_coef += gr
            A.append(row)
        if len(lambdas_groups) == 0:
            linear_constraint = None
            method = 'Nelder-Mead'
        else:
            linear_constraint = LinearConstraint(A, [1] * len(lambdas_groups), [1] * len(lambdas_groups))
            method = 'trust-constr'
        res = minimize(f, init_lambdas, method=method,
            constraints=linear_constraint, options={'verbose': 0}, bounds=bounds)
        print(v1, v2, res.fun)
        mat[v1 - 1, v2 - 1] = res.fun

        #f_init = f(init_lambdas)
        #print(v1, v2, f_init)
        #mat[v1 - 1, v2 - 1] = f_init
        #mat[v1, v2] = f_init
print(mat)

"""
