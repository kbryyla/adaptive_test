import numpy as np
from scipy.optimize import minimize
from core.irt_model import IRTModel

class ThetaEstimator:
    def __init__(self, prior_mean=0.0, prior_std=1.5):
        self.mu = prior_mean
        self.sigma = prior_std

    def estimate(self, theta_init, items, responses):
        def loss(theta):
            ll = 0.0
            for item, u in zip(items, responses):
                p = IRTModel.probability(theta, item)
                ll += u * np.log(p) + (1 - u) * np.log(1 - p)

            prior = (theta - self.mu)**2 / (2 * self.sigma**2)
            return -ll + prior

        result = minimize(loss, theta_init, bounds=[(-4, 4)])
        return result.x[0]
