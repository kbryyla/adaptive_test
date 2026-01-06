import numpy as np

def theta_update_single_item(
    theta,
    item,
    response,
    lr=0.8,
    max_step=1.0,
    use_map=False,
    prior_var=1.5
):
    a, b, c = item.a, item.b, item.c

    # Numerik stabilite
    z = np.clip(a * (theta - b), -10, 10)
    P = c + (1 - c) / (1 + np.exp(-z))

    # Likelihood gradient
    grad = a * (response - P)

    # MAP desteği (opsiyonel)
    if use_map:
        grad -= theta / prior_var

    delta = lr * grad
    delta = np.clip(delta, -max_step, max_step)

    return delta
