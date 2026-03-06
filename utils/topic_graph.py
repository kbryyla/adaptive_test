from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import numpy as np
from utils.loader import build_item_bank


item_bank = build_item_bank("data/erisim_guvenligi_sorulari.json")
all_sub_topics = [item.sub_topic for item in item_bank]
unique_sub_topics = list(set(all_sub_topics))
skill_ids = {sub_topic: index for index, sub_topic in enumerate(unique_sub_topics, start=1)}
print(skill_ids)

skills_by_domain = {
    "Network Security": [54, 38, 103, 106, 112, 21, 48, 72, 89, 114, 14, 115],
    "DNS Management": [1, 3, 51, 29, 95, 39],
    "Firewall Management": [13, 37, 61, 32, 108, 81, 12, 25, 34, 100, 50, 77, 68],
    "IPS Management": [104, 62, 8, 24, 107, 6],
    "WAF Management": [36, 78, 10, 93, 65, 64, 42, 96],
    "Proxy Management": [90, 80, 47, 110, 31, 92, 73, 55, 99],
    "DDOS Protection": [5, 40, 52, 39, 33, 113],
    "Bot Protection": [87, 85, 27, 101, 59, 99],
    "APT Management": [4, 46, 75, 58, 95, 86, 98],
    "Mobile Security": [2, 105],
    "Identity & Access": [53],
    "Compliance & Standards": [9, 43, 41],
    "Certificates & Protocols": [7, 63, 45],
    "Other Security Knowledge": [76, 28, 30, 82, 15, 70, 91, 88, 97, 16, 69, 44, 35, 114, 18]
}

"""
skill'lere id atandı. şimdi idler üzerinden graph ve propagation düzenlemeleri yapılacak.
"""
G = nx.DiGraph()

# Domain ve skill node ekleme + edge
for domain, skill_list in skills_by_domain.items():
    G.add_node(domain, type="domain")
    for skill_id, domain in skills_to_domain:
        G.add_node(skill_id, type="skill")
        G.add_edge(domain, skill_id, weight=1.0)


domain_edges = [
    ("Network Security", "Application Security", 0.5),
    ("Network Security", "Infrastructure Security", 0.7),
    ("Network Security", "Mobile Security", 0.4),
    ("Application Security", "Security Operations", 0.6),
    ("Infrastructure Security", "Security Operations", 0.5),
    ("Security Operations", "Compliance & Standards", 0.7),
    ("Certificates & Protocols", "Application Security", 0.6),
    ("Certificates & Protocols", "Network Security", 0.5)
]

for d1, d2, w in domain_edges:
    G.add_edge(d1, d2, weight=w)


vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(all_skill_texts)
sim_matrix = cosine_similarity(X)

# Top-K benzer skill (örnek: 5)
TOP_K = 5
n = len(all_skill_ids)

for i in range(n):
    sims = sim_matrix[i]
    top_idx = np.argsort(sims)[-TOP_K-1:-1]  # kendisi hariç
    for j in top_idx:
        neighbor_id = all_skill_ids[j]
        weight = sims[j]
        G.add_edge(all_skill_ids[i], neighbor_id, weight=weight)


def propagate_theta(graph, student, skill_id, alpha=0.2):
    if skill_id not in graph:
        return

    theta_i = student.get_theta(skill_id)
    for neighbor in graph.successors(skill_id):
        weight = graph[skill_id][neighbor]["weight"]
        theta_j = student.get_theta(neighbor)
        new_theta = theta_j + alpha * weight * (theta_i - theta_j)
        student.set_theta(neighbor, new_theta)
