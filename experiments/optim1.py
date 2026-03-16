from scipy.optimize import Bounds, LinearConstraint, minimize
import numpy as np


def f(lam):
    term1 = lam[0] * lam[2] * lam[4] + lam[3] * lam[4] + lam[5] * lam[7]
    term2 = lam[3] * lam[4]
    term3 = lam[0] * lam[2] * lam[4] + lam[5] * lam[7]
    term4 = lam[3] * lam[4]
    term5 = lam[2] * lam[4]
    term6 = lam[3] * lam[4]
    term7 = lam[5]
    term8 = lam[5]
    term9 = lam[1] * lam[2] * lam[4] + lam[5] * lam[7]
    term10 = lam[1] * lam[2] * lam[4] + lam[5] * lam[6]
    term11 = lam[1] * lam[2] * lam[4] + lam[5] * lam[6]
    return (term1 ** 2 + term2 ** 2 + term3 ** 2 + term4 ** 2 + term5 ** 2
            + term6 ** 2 + term7 ** 2 + term8 ** 2 + term9 ** 2 + term10 ** 2 + term11 ** 2)

def g(lam):
    """
    term1 = lam[0] * lam[2] * lam[4] + lam[3] * lam[4] + lam[5] * lam[7]
    term2 = lam[3] * lam[4]
    term3 = lam[0] * lam[2] * lam[4] + lam[5] * lam[7]
    term4 = lam[3] * lam[4]
    term5 = lam[2] * lam[4]
    term6 = lam[3] * lam[4]
    term7 = lam[5]
    term8 = lam[5]
    term9 = lam[1] * lam[2] * lam[4] + lam[5] * lam[7]
    term10 = lam[1] * lam[2] * lam[4] + lam[5] * lam[6]
    term11 = lam[1] * lam[2] * lam[4] + lam[5] * lam[6]
    return (term1 ** 2 + term2 ** 2 + term3 ** 2 + term4 ** 2 + term5 ** 2
            + term6 ** 2 + term7 ** 2 + term8 ** 2 + term9 ** 2 + term10 ** 2 + term11 ** 2)
    """

bounds = Bounds([0] * 8, [1] * 8)
linear_constraint = LinearConstraint([[1, 1, 0, 0, 0, 0, 0, 0],
                                      [0, 0, 1, 1, 0, 0, 0, 0],
                                      [0, 0, 0, 0, 1, 1, 0, 0],
                                      [0, 0, 0, 0, 0, 0, 1, 1]], [1] * 4, [1] * 4)

res = minimize(f, [1, 0, 1, 0, 1, 0, 1, 0], method='trust-constr',
               constraints=linear_constraint, options={'verbose': 1}, bounds=bounds)
print(res.fun)
print(res.x)

"""
bounds = Bounds([0] * 4, [1] * 4)
linear_constraint = LinearConstraint([[1, 1, 0, 0],
                                      [0, 0, 1, 1]], [1] * 2, [1] * 2)

res = minimize(g, [1, 0, 1, 0], method='trust-constr',
               constraints=linear_constraint, options={'verbose': 1}, bounds=bounds)
print(res.fun)
print(res.x)
"""