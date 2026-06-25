from scipy.optimize import Bounds, LinearConstraint, minimize
import numpy as np


params = ['213', '211', '332', '331', '402', '403']

bounds = Bounds([0] * len(params), [1] * len(params))
linear_constraint = LinearConstraint([[1, 1, 0, 0, 0, 0], [0, 0, 1, 1, 0, 0], [0, 0, 0, 0, 1, 1]], [1, 1, 1], [1, 1, 1])
method = 'trust-constr'

def g(lam):
    l221 = 1.0
    l341 = 1.0
    l213 = lam[params.index('213')]
    l211 = lam[params.index('211')]
    l332 = lam[params.index('332')]
    l331 = lam[params.index('331')]
    l402 = lam[params.index('402')]
    l403 = lam[params.index('403')]
    return ((l402 * l211 + l403 * l332 * l221) ** 2 +
            (l403 * l331 + l402 * l213 * l341) ** 2 +
            l402 ** 2 +
            l403 ** 2 +
            (l403 * l332 + l402 * l213) ** 2)


lam = np.array([0, 1, 1, 0, 0, 1])
res = minimize(g, lam, method=method,
               constraints=linear_constraint, options={'verbose': 0}, bounds=bounds)
lam = res.x
for i, v in enumerate(params):
    print(f"lam[{v}] = {lam[i]}")
