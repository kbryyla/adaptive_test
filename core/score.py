import numpy as np


# tekrar dön

def compute_final_score(theta):

    score = 100 / (1 + np.exp(-theta / 1.1))
    return float(np.clip(score, 0, 100))



def compute_global_theta(theta_by_topic, weights=None):




    return None
