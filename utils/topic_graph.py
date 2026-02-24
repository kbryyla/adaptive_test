DOMAIN_GRAPH = {
    "Network Güvenliği": [
        "Firewall Yönetimi",
        "IPS Yönetimi",
        "DDoS Koruma Yönetimi",
        "Proxy Sistemleri Yönetimi"
    ],
    "Uygulama Güvenliği": [
        "WAF Yönetimi",
        "API Security Bilgisi",
        "Bot Koruma Yönetimi"
    ],
    "Sistem & Platform": [
        "Linux İşletim Sistemleri",
        "Microsoft Windows İşletim Sistemleri"
    ],
    "Tehdit & Müdahale": [
        "APT Yönetimi",
        "Siber Kriz Yönetimi Bilgisi"
    ],
    "Yönetim & Standartlar": [
        "ITIL, SOX, COBIT"
    ]
}


def build_domain_graph(domain_graph, intra_weight=0.25, back_factor=0.5):
    """
    Aynı domain içindeki topic'ler arasında
    ASİMETRİK (yönlü) bağ kurar.

    t1 -> t2 : intra_weight
    t2 -> t1 : intra_weight * back_factor
    """
    graph = {}

    #to do

    return graph


TOPIC_GRAPH = build_domain_graph(DOMAIN_GRAPH)


def propagate_theta(
    theta_by_topic,
    topic_graph,
    alpha=0.2,
    min_items_by_topic=None,
    min_src_items=1,
    min_dst_items=3,
    max_delta=0.4
):
    #to do

    return None

def get_related_topics(topic):
    return TOPIC_GRAPH.get(topic, {})


def normalize_weights(max_sum=1.0):
    """
    İsteğe bağlı: Her kaynak topic için
    toplam çıkış ağırlığını sınırlar.
    """
    for src, targets in TOPIC_GRAPH.items():
        total = sum(targets.values())
        if total > max_sum:
            for k in targets:
                targets[k] *= max_sum / total
