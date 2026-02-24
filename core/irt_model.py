import numpy as np
from scipy.optimize import minimize_scalar

def irt_3pl(theta, a, b, c=0.2):
    z = np.clip(a * (theta - b), -35, 35)
    p = c + (1 - c) / (1 + np.exp(-z))
    return p


def mle(items,responses):
    def nll(theta):
        ll = 0
        for u,item in zip(responses, items):
            a, b, c = item.a, item.b, item.c
            p = irt_3pl(theta, a,b,c)
            #protection: prevent log(0)
            p = np.clip(p, 1e-10, 1 - 1e-10)
            ll += u * np.log(p) + (1-u) * np.log(1 - p)
        return -ll

    res = minimize_scalar(
        nll,
        bounds=(-3, 3),
        method='bounded'
    )
    return res.x


def fisher_information_3pl(theta, a, b, c=0.2):
    p = irt_3pl(theta, a, b, c)
    p = np.clip(p, 1e-6, 1 - 1e-6)
    return (a**2 * (1 - p) * (p - c)**2) / ((1 - c)**2 * p)

def standard_error(theta, items):
    if not items:
        return np.inf
    total_info = sum(fisher_information_3pl(theta, i.a, i.b, i.c) for i in items)
    if total_info <= 0:
        return np.inf
    return 1 / np.sqrt(total_info)
