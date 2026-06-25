from scipy.optimize import Bounds, LinearConstraint, minimize
import numpy as np


params = ['31', '32', '43', '42']

bounds = Bounds([0] * len(params), [1] * len(params))
linear_constraint = LinearConstraint([[1, 1, 0, 0], [0, 0, 1, 1]], [1, 1], [1, 1])
method = 'trust-constr'

def g(alph):
    a31 = alph[params.index('31')]
    a32 = alph[params.index('32')]
    a43 = alph[params.index('43')]
    a42 = alph[params.index('42')]
    return (a42 + a43 * a32) ** 2 + (a43 * a31) ** 2 + (a43) ** 2 + (a43 * a32) ** 2 + (a42) ** 2

alph = np.array([0, 1, 1, 0])
res = minimize(g, alph, method=method,
               constraints=linear_constraint, options={'verbose': 0}, bounds=bounds)
alph = res.x
for i, v in enumerate(params):
    print(f"alpha[{v}] = {alph[i]}")
