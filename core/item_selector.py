import math

from numpy import random

from core.irt_model import fisher_information_3pl
from utils.topic_graph import get_related_topics


def select_next_item_graph_aware(
    student,
    item_bank,
    used_item_ids,
    top_k=8,
    alpha=0.6,
    beta=0.3,
    gamma=0.1
):
    scored_items = []

    # ===========================
    # 1️⃣ HİÇ SORULMAMIŞ TOPIC
    # ===========================
    all_topics = {item.sub_topic for item in item_bank}

    untouched_topics = {
        topic for topic in all_topics
        if len(student.asked_items_by_topic.get(topic, [])) == 0
    }

    for topic in untouched_topics:
        candidates = [
            item for item in item_bank
            if item.sub_topic == topic and item.id not in used_item_ids
        ]
        if candidates:
            candidates.sort(key=lambda x: abs(x.b))
            return random.choice(candidates[:min(3, len(candidates))])


    # NORMAL SCORING

    for item in item_bank:
        if item.id in used_item_ids:
            continue

        topic = item.sub_topic
        theta = student.theta_topic.get(topic, 0.0)

        # ZOR SORUYA GEÇİŞ FİLTRESİ
        if theta > 0.5 and item.b < theta - 0.2:
            continue

        fisher = fisher_information_3pl(theta, item.a, item.b, item.c)

        # ZOR SORU TEŞVİKİ
        difficulty_gap = item.b - theta
        hard_bonus = 0.0

        if theta > 0.4 and difficulty_gap > 0:
            hard_bonus = 0.5 * difficulty_gap

        asked = len(student.asked_items_by_topic.get(topic, []))
        coverage = 1 / (1 + asked)

        se = 1 / math.sqrt(fisher + 1e-6)
        uncertainty = se

        graph_bonus = 0.0
        for related, w in get_related_topics(topic).items():
            related_theta = student.theta_topic.get(related, 0.0)
            graph_bonus += w * math.exp(-abs(related_theta))



        score = (
                alpha * fisher +
                beta * uncertainty +
                gamma * coverage +
                0.2 * graph_bonus +
                hard_bonus
        )

        scored_items.append((score, item))

    if not scored_items:
        return None

    scored_items.sort(key=lambda x: x[0], reverse=True)
    top_items = scored_items[:top_k]
    return random.choice([item for _, item in top_items])
