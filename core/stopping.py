import numpy as np
from core.irt_model import fisher_information_3pl

def standard_error(theta, items):
    if not items:
        return np.inf
    total_info = sum(fisher_information_3pl(theta, i.a, i.b, i.c) for i in items)
    if total_info <= 0:
        return np.inf
    return 1/np.sqrt(total_info)

def topic_converged(theta, items, se_threshold=0.30, min_items=1):
    if len(items) < min_items:
        return False
    se = standard_error(theta, items)
    return se < se_threshold
def should_stop(student, asked_items_by_topic, se_threshold=0.30,
                min_items_per_topic=3, max_items=30):
    """
    CAT durdurma kriteri:
    1. Maksimum soru sayısına ulaşıldı mı?
    2. Her topic minimum soruya ulaşıp, theta SE eşik değerinin altında mı?
    3. Genel theta SE eşik değerinin altında mı?
    """
    total_asked = sum(len(v) for v in asked_items_by_topic.values())

    # 1️⃣ max_items kontrolü
    if total_asked >= max_items:
        return True, "max_items"

    # 2️⃣ topic bazlı konverjans kontrolü
    for topic, items in asked_items_by_topic.items():
        theta = student.get_theta(topic)
        se = student.get_se(topic)  # her topic için SE al
        if not topic_converged(theta, items, se_threshold, min_items_per_topic):
            return False, None
        if se > se_threshold:  # topic SE yüksekse durdurma
            return False, None

    # 3️⃣ genel theta SE kontrolü (opsiyonel)
    general_se = student.get_general_se()
    if general_se > se_threshold:
        return False, None

    # Tüm kriterler sağlanmışsa test durur
    return True, "converged"
