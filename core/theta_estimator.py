from core.irt_model import mle


def theta_update_general(items, responses):
    return mle(items, responses)

