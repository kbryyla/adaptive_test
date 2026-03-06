from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import numpy as np


skills_by_domain = {
    "Network Security": [
        'network - ağ yapılandırması bilgisi',
        'network - ağ altyapı bilgisi',
        'network - ağ mimarisi bilgisi',
        'network - ağ performansı i̇yileştirme araçları bilgisi (network cem ,helix, massive)',
        'network - ağ güvenliği bilgisi',
        'network - ağ güvenlik teknolojileri',
        'network - ağ bakımı bilgisi',
        'network - ağ mimarisi sanallaştırma konsept bilgisi (nfv)',
        'network - data şebekesindeki cihazların ve altyapılıların bilgisi (router, switch, wlan)',
        'ip, mpls ve internet teknolojileri bilgisi'
    ],
    "DNS Management": [
        'dns yönetimi  -  dns güvenlik açıklarını tespit etme ve düzeltme becerisi.',
        'dns yönetimi  -  dns saldırılarını tespit etmek ve önlemek için güvenlik izleme ve uyarı sistemlerini kullanma becerisi',
        'dns yönetimi  -  dns güvenliği konularında bilgi sahibi olma.',
        "dns yönetimi  -  dns'nin çalışma şeklini ve işlevlerini anlama becerisi",
        'dns yönetimi  -  dns güvenliğini sağlamak için güvenlik politikaları ve prosedürleri oluşturma ve uygulama becerisi',
        'dns yönetimi  -  dns güvenliğini sağlamak için kullanılan güvenlik çözümlerini anlama becerisi'
    ],
    "Firewall Management": [
        'firewall yönetimi  -  güvenlik duvarı kayıtlarını analiz etme ve şüpheli aktiviteleri belirleme becerisi',
        'firewall yönetimi  -  farklı firewall çözümlerini konfigüre etme ve yönetme becerisi.',
        'firewall yönetimi  -  ağ trafiğini analiz etme ve şüpheli aktiviteleri belirleme becerisi',
        'firewall yönetimi  -  ağ güvenliği politikalarını ve prosedürlerini oluşturma ve uygulama becerisi',
        'firewall yönetimi  -  ağ güvenliği çözümlerinin performansını izleme ve analiz etme becerisi',
        'firewall yönetimi  -  güvenlik duvarı performansını izleme ve analiz etme becerisi',
        'firewall yönetimi  -  güvenlik duvarı etkinliğini değerlendirme becerisi',
        'firewall yönetimi  -  ağdaki kimlik ve erişim yönetimini anlama becerisi',
        'firewall yönetimi  -  ağ erişim kontrollerini tanımlama ve uygulama becerisi',
        'firewall yönetimi  -  farklı türdeki güvenlik duvarlarının özelliklerini ve yeteneklerini anlama becerisi',
        'firewall yönetimi  -  güvenlik duvarı kurallarını oluşturma, yönetme ve denetleme becerisi',
        'firewall yönetimi  -  ağdaki saldırıları tespit etme ve önleme becerisi',
        'firewall yönetimi  -  ips cihazlarını yapılandırma ve güncelleme becerisi.'
    ],
    "IPS Management": [
        'ips yönetimi  -  ips performansını izleme ve analiz etme becerisi',
        'ips yönetimi  -  ips olaylarını soruşturma ve yanıt verme becerisi',
        'ips yönetimi  -  farklı türdeki ips (örneğin, imza tabanlı, davranışsal) özelliklerini ve yeteneklerini anlama becerisi',
        'ips yönetimi  -  ips kayıtlarını analiz etme ve şüpheli aktiviteleri belirleme becerisi',
        'ips yönetimi  -  ips etkinliğini değerlendirme becerisi',
        'ips yönetimi  -  ips kurallarını oluşturma, yönetme ve denetleme becerisi'
    ],
    "WAF Management": [
        'waf yönetimi  -  farklı türdeki waf (örneğin, statik, dinamik, içerik tabanlı) özelliklerini ve yeteneklerini anlama becerisi',
        'waf yönetimi  -  waf performansını izleme ve analiz etme becerisi',
        'waf yönetimi  -  waf olaylarını soruşturma ve yanıt verme becerisi',
        'waf yönetimi  -  web uygulamalarını koruma stratejilerini belirleme yeteneği',
        'waf yönetimi  -  waf kurallarını oluşturma, yönetme ve denetleme becerisi',
        "waf yönetimi  -  waf'ın konfigürasyonunu ve güncellemelerini yönetme becerisi.",
        'waf yönetimi  -  waf etkinliğini değerlendirme becerisi',
        'waf yönetimi  -  waf kayıtlarını analiz etme ve şüpheli aktiviteleri belirleme becerisi'
    ],
    "Proxy Management": [
        'proxy sistemleri yönetimi  -  i̇nternet trafiğini filtreleme ve yönlendirme yeteneği.',
        'proxy sistemleri yönetimi  -  proxy sunucularını konfigüre etme ve güncelleme becerisi.',
        'proxy sistemleri yönetimi  -  proxy sistem etkinliğini değerlendirme becerisi',
        'proxy sistemleri yönetimi  -  farklı türdeki proxy sistemlerinin (örneğin, http, ftp, dns) özelliklerini ve yeteneklerini anlama becerisi',
        'proxy sistemleri yönetimi  -  proxy sistem performansını izleme ve analiz etme becerisi',
        'proxy sistemleri yönetimi  -  proxy sistemlerini kurma, yapılandırma ve yönetme becerisi',
        'proxy sistemleri yönetimi  -  proxy sistem olaylarını soruşturma ve yanıt verme becerisi'
    ],
    "DDOS Protection": [
        'ddos koruma yönetimi  -  ddos saldırılarına karşı koruma sağlamak için kullanılan güvenlik çözümlerini anlama becerisi',
        'ddos koruma yönetimi  -  ddos saldırılarını tespit etme ve önleme becerisi.',
        'ddos koruma yönetimi  -  ddos koruma çözümlerini konfigüre etme yeteneği.',
        'ddos koruma yönetimi  -  ddos saldırılarının nasıl çalıştığını anlama becerisi',
        'ddos koruma yönetimi  -  ddos saldırılarını tespit etmek ve önlemek için güvenlik izleme ve uyarı sistemlerini kullanma becerisi',
        'ddos koruma yönetimi  -  ddos saldırılarına karşı koruma sağlamak için güvenlik politikaları ve prosedürleri oluşturma ve uygulama becerisi'
    ],
    "Bot Protection": [
        'bot koruma yönetimi  -  zararlı bot trafiğini tespit ve engelleme becerisi.',
        'bot koruma yönetimi  -  botların nasıl çalıştığını anlama becerisi',
        'bot koruma yönetimi  -  botlara karşı koruma sağlamak için kullanılan güvenlik çözümlerini anlama becerisi',
        'bot koruma yönetimi  -  botlara karşı koruma sağlamak için güvenlik politikaları ve prosedürleri oluşturma ve uygulama becerisi',
        'bot koruma yönetimi  -  bot saldırılarını tespit etmek ve önlemek için güvenlik izleme ve uyarı sistemlerini kullanma becerisi',
        'bot koruma yönetimi  -  bot ağlarına karşı koruma stratejilerini geliştirme yeteneği.'
    ],
    "APT Management": [
        "apt yönetimi  -  apt'lere karşı koruma sağlamak için güvenlik politikaları ve prosedürleri oluşturma ve uygulama becerisi",
        "apt yönetimi  -  apt'lere karşı koruma sağlamak için kullanılan güvenlik çözümlerini anlama becerisi",
        "apt yönetimi  -  apt tespiti ve müdahale becerisi.",
        "apt yönetimi  -  özellikle gelişmiş tehditler için kullanılan teknikleri ve taktikleri anlama becerisi",
        "apt yönetimi  -  apt saldırılarını tespit etmek ve önlemek için güvenlik izleme ve uyarı sistemlerini kullanma becerisi",
        "apt yönetimi  -  gelişmiş kalıcı tehditlere karşı savunma stratejilerini belirleme yeteneği."
    ],
    "Mobile Security": [
        'mobil cihaz güvenliği  -  mobil cihaz güvenliği tehditlerini tespit etme ve önleme becerisi.',
        'mobil cihaz güvenliği  -  mobil cihazlar üzerinde güvenlik politikalarını uygulama yeteneği.'
    ],
    "Identity & Access": [
        'kimlik ve erişim yönetimi bilgisi'
    ],
    "Compliance & Standards": [
        'denetim ve uyum bilgisi (iso 27001 vb.)',
        'itil, sox, cobit, btk, kvkk ve iso27001 standartları bilgisi',
        'iso 22301 bilgisi'
    ],
    "Certificates & Protocols": [
        'güvenlik sertifikası yönetimi  -  ssl/tls sertifikalarını yönetme ve güncelleme becerisi.',
        'güvenlik sertifikası yönetimi  -  sertifika tabanlı güvenlik politikalarını uygulama yeteneği.',
        'güvenlik protokolleri bilgisi'
    ],
    "Other Security Knowledge": [
        'uygulama seviyesi güvenlik  -  uygulamaların güvenliğini değerlendirme ve iyileştirme yeteneği.',
        'uygulama seviyesi güvenlik  -  uygulama tabanlı güvenlik açıklarını tespit etme ve düzeltme becerisi.',
        'proje yönetim bilgisi',
        'container security bilgisi',
        'güvenlik platformları bilgisi',
        'güvenlik değerlendirmesi ve test bilgisi',
        'konfigürasyon yönetimi bilgisi',
        'zafiyet ve uyumluluk tarama sistemleri',
        'güvenlik donanım ve yazılımı bilgisi',
        'analiz ve raporlama bilgisi',
        'teknik şartname hazırlama bilgisi',
        'genel mimari bilgisi',
        'altyapı ve platform bilgisi',
        'siber kriz yönetimi bilgisi',
        'altyapı ve topoloji mimarisi bilgisi'
    ]
}

"""
skill_id ile item.sub_topic eşleşmedi!!!!!!!!!!!!!!!!!!
"""
# Skill ID
skill_id_to_text = {}
skill_to_domain = {}

for i, (domain, skills) in enumerate(skills_by_domain.items()):
    for j, skill in enumerate(skills):
        skill_id = f"SK{i*100 + j + 1:03d}"  # SK001, SK002, ...
        skill_id_to_text[skill_id] = skill
        skill_to_domain[skill_id] = domain


G = nx.DiGraph()

# Domain ve skill node ekleme + edge
for domain, skill_list in skills_by_domain.items():
    G.add_node(domain, type="domain")
    for skill_id, domain in skill_to_domain.items():
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

# skills lists
all_skill_texts = list(skill_id_to_text.values())
all_skill_ids = list(skill_id_to_text.keys())

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
