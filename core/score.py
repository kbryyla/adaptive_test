import numpy as np
from core.irt_model import fisher_information_3pl

def compute_final_score(theta_by_topic, items_by_topic,
                        theta_bounds=(-3,3), score_bounds=(0,100)):
    weighted_sum = 0.0
    total_weight = 0.0

    for topic, theta in theta_by_topic.items():
        items = items_by_topic.get(topic, [])
        if not items:
            continue
        info = sum(fisher_information_3pl(theta, i.a, i.b, i.c) for i in items)
        if info < 1e-6:
            continue
        weighted_sum += theta*info
        total_weight += info

    if total_weight == 0:
        return score_bounds[0]

    theta_global = weighted_sum / total_weight

    theta_min, theta_max = theta_bounds
    score_min, score_max = score_bounds
    score = (theta_global - theta_min)/(theta_max - theta_min)
    score = score_min + score*(score_max - score_min)
    return float(np.clip(score, score_min, score_max))


#Fisher-ağırlıklı global theta

def compute_global_theta(student):
    """
    Topic bazlı theta ve Fisher bilgisine göre ağırlıklı genel theta
    """
    weighted_sum = 0.0
    total_weight = 0.0
    for topic, theta in student.theta_topic.items():
        items = student.asked_items_by_topic.get(topic, [])
        if not items:
            continue
        info = sum(fisher_information_3pl(theta, i.a, i.b, i.c) for i in items)
        if info < 1e-6:
            continue
        weighted_sum += theta * info
        total_weight += info
    if total_weight == 0:
        return 0.0
    return weighted_sum / total_weight
