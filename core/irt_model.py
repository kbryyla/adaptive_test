import numpy as np

def irt_3pl(theta, a, b, c=0.2):
    z = np.clip(a * (theta - b), -35, 35)
    p = c + (1 - c) / (1 + np.exp(-z))
    return p

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
