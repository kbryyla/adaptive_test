DOMAIN_GRAPH = {
    "Network Güvenliği": ["Firewall Yönetimi", "IPS Yönetimi", "DDoS Koruma Yönetimi", "Proxy Sistemleri Yönetimi"],
    "Uygulama Güvenliği": ["WAF Yönetimi", "API Security Bilgisi", "Bot Koruma Yönetimi"],
    "Sistem & Platform": ["Linux İşletim Sistemleri", "Microsoft Windows İşletim Sistemleri"],
    "Tehdit & Müdahale": ["APT Yönetimi", "Siber Kriz Yönetimi Bilgisi"],
    "Yönetim & Standartlar": ["ITIL, SOX, COBIT"]
}

def build_domain_graph(domain_graph, intra_weight=0.25):
    graph = {}
    for _, topics in domain_graph.items():
        for t1 in topics:
            graph.setdefault(t1, {})
            for t2 in topics:
                if t1 != t2:
                    graph[t1][t2] = intra_weight
    return graph

TOPIC_GRAPH = build_domain_graph(DOMAIN_GRAPH)

MANUAL_EDGES = {
    "DDoS Koruma Yönetimi": {"Firewall Yönetimi": 0.7, "IPS Yönetimi": 0.8},
    "Firewall Yönetimi": {"WAF Yönetimi": 0.6}
}

for src, targets in MANUAL_EDGES.items():
    TOPIC_GRAPH.setdefault(src, {})
    for dst, w in targets.items():
        TOPIC_GRAPH[src][dst] = max(TOPIC_GRAPH[src].get(dst, 0), w)

def propagate_theta(theta_by_topic, topic_graph, alpha=0.3, min_items_by_topic=None):
    new_theta = dict(theta_by_topic)

    for src, src_theta in theta_by_topic.items():
        if src not in topic_graph:
            continue
        for dst, weight in topic_graph[src].items():
            damping = 1.0
            if min_items_by_topic and min_items_by_topic.get(dst, 0) >= 3:
                damping = 0.3
            # theta’nın işareti propagationa yansır
            new_theta[dst] = new_theta.get(dst, 0.0) + alpha * weight * src_theta * damping

    return new_theta


def get_related_topics(topic):
    return TOPIC_GRAPH.get(topic, {})

def normalize_weights(max_sum=1.0):
    for src, targets in TOPIC_GRAPH.items():
        total = sum(targets.values())
        if total > max_sum:
            for k in targets:
                targets[k] *= max_sum/total
