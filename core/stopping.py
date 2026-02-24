import numpy as np
from core.irt_model import fisher_information_3pl, standard_error
from core.theta_estimator import theta_update_general
from session.student import StudentState


# ===========================
# DURDURMA KRİTERİ
# ===========================

def should_stop(
    student,
    asked_items_by_topic,
    se_threshold=0.30,
    max_items=10
):
    total_items = sum(len(v) for v in asked_items_by_topic.values())

    theta = theta_update_general(asked_items_by_topic, responses=student.responses)

    se = standard_error(theta=theta,items = asked_items_by_topic)
    if se < se_threshold:
        return True, "precision reached"

    # max Qs
    if total_items >= max_items:
        return True, "max_items"

    return False, None





