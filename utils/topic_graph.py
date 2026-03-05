from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx


skills_by_domain = {
    "Network Security": [
        "network - ağ yapılandırması bilgisi",
        "network - ağ altyapı bilgisi",
        "network - ağ mimarisi bilgisi",
        "network - ağ performansı iyileştirme araçları bilgisi (network cem, helix, massive)",
        "network - ağ güvenliği bilgisi",
        "network - ağ güvenlik teknolojileri",
        "network - ağ bakımı bilgisi",
        "network - ağ mimarisi sanallaştırma konsept bilgisi (nfv)",
        "network - data şebekesindeki cihazların ve altyapılıların bilgisi (router, switch, wlan)",
        "ip, mpls ve internet teknolojileri bilgisi"
    ],
    "DNS Management": [
        "dns yönetimi - dns güvenlik açıklarını tespit etme ve düzeltme becerisi",
        "dns yönetimi - dns saldırılarını tespit etmek ve önlemek için güvenlik izleme ve uyarı sistemlerini kullanma becerisi",
        "dns yönetimi - dns güvenliği konularında bilgi sahibi olma",
        "dns yönetimi - dns güvenliğini sağlamak için güvenlik politikaları ve prosedürleri oluşturma ve uygulama becerisi",
        "dns yönetimi - dns'nin çalışma şeklini ve işlevlerini anlama becerisi",
        "dns yönetimi - dns güvenliğini sağlamak için kullanılan güvenlik çözümlerini anlama becerisi"
    ],
    "Firewall Management": [
        "firewall yönetimi - güvenlik duvarı kayıtlarını analiz etme ve şüpheli aktiviteleri belirleme becerisi",
        "firewall yönetimi - farklı firewall çözümlerini konfigüre etme ve yönetme becerisi",
        "firewall yönetimi - ağ trafiğini analiz etme ve şüpheli aktiviteleri belirleme becerisi",
        "firewall yönetimi - ağ güvenliği politikalarını ve prosedürlerini oluşturma ve uygulama becerisi",
        "firewall yönetimi - ağ güvenliği çözümlerinin performansını izleme ve analiz etme becerisi",
        "firewall yönetimi - güvenlik duvarı performansını izleme ve analiz etme",
        "firewall yönetimi - güvenlik duvarı etkinliğini değerlendirme becerisi",
        "firewall yönetimi - ağdaki kimlik ve erişim yönetimini anlama becerisi",
        "firewall yönetimi - ağ erişim kontrollerini tanımlama ve uygulama becerisi",
        "firewall yönetimi - farklı türdeki güvenlik duvarlarının özelliklerini ve yeteneklerini anlama becerisi",
        "firewall yönetimi - güvenlik duvarı kurallarını oluşturma, yönetme ve denetleme becerisi",
        "firewall yönetimi - ağdaki saldırıları tespit etme ve önleme becerisi",
        "firewall yönetimi - ips cihazlarını yapılandırma ve güncelleme becerisi"  # opsiyonel overlap
    ],
    "IPS Management": [
        "ips yönetimi - ips performansını izleme ve analiz etme becerisi",
        "ips yönetimi - ips olaylarını soruşturma ve yanıt verme becerisi",
        "ips yönetimi - farklı türdeki ips (örneğin, imza tabanlı, davranışsal) özelliklerini ve yeteneklerini anlama becerisi",
        "ips yönetimi - ips kayıtlarını analiz etme ve şüpheli aktiviteleri belirleme becerisi",
        "ips yönetimi - ips etkinliğini değerlendirme becerisi",
        "ips yönetimi - ips kurallarını oluşturma, yönetme ve denetleme becerisi"
    ],
    "WAF Management": [
        "waf yönetimi - farklı türdeki waf (örneğin, statik, dinamik, içerik tabanlı) özelliklerini ve yeteneklerini anlama becerisi",
        "waf yönetimi - waf performansını izleme ve analiz etme",
        "waf yönetimi - waf olaylarını soruşturma ve yanıt verme becerisi",
        "waf yönetimi - web uygulamalarını koruma stratejilerini belirleme yeteneği",
        "waf yönetimi - waf kurallarını oluşturma, yönetme ve denetleme becerisi",
        "waf yönetimi - waf'ın konfigürasyonunu ve güncellemelerini yönetme becerisi",
        "waf yönetimi - waf etkinliğini değerlendirme becerisi",
        "waf yönetimi - waf kayıtlarını analiz etme ve şüpheli aktiviteleri belirleme becerisi"
    ],
    "Proxy Management": [
        "proxy sistemleri yönetimi - internet trafiğini filtreleme ve yönlendirme yeteneği",
        "proxy sistemleri yönetimi - proxy sunucularını konfigüre etme ve güncelleme becerisi",
        "proxy sistemleri yönetimi - proxy sistem etkinliğini değerlendirme becerisi",
        "proxy sistemleri yönetimi - farklı türdeki proxy sistemlerinin (örneğin, http, ftp, dns) özelliklerini ve yeteneklerini anlama becerisi",
        "proxy sistemleri yönetimi - proxy sistem performansını izleme ve analiz etme becerisi",
        "proxy sistemleri yönetimi - proxy sistemlerini kurma, yapılandırma ve yönetme becerisi",
        "proxy sistemleri yönetimi - proxy sistem olaylarını soruşturma ve yanıt verme becerisi"
    ],
    "DDOS Protection": [
        "ddos koruma yönetimi - ddos saldırılarına karşı koruma sağlamak için kullanılan güvenlik çözümlerini anlama becerisi",
        "ddos koruma yönetimi - ddos saldırılarını tespit etme ve önleme becerisi",
        "ddos koruma yönetimi - ddos koruma çözümlerini konfigüre etme yeteneği",
        "ddos koruma yönetimi - ddos saldırılarının nasıl çalıştığını anlama becerisi",
        "ddos koruma yönetimi - ddos saldırılarını tespit etmek ve önlemek için güvenlik izleme ve uyarı sistemlerini kullanma becerisi",
        "ddos koruma yönetimi - ddos saldırılarına karşı koruma sağlamak için güvenlik politikaları ve prosedürleri oluşturma ve uygulama becerisi"
    ],
    "Bot Protection": [
        "bot koruma yönetimi - zararlı bot trafiğini tespit ve engelleme becerisi",
        "bot koruma yönetimi - botların nasıl çalıştığını anlama becerisi",
        "bot koruma yönetimi - botlara karşı koruma sağlamak için kullanılan güvenlik çözümlerini anlama becerisi",
        "bot koruma yönetimi - botlara karşı koruma sağlamak için güvenlik politikaları ve prosedürleri oluşturma ve uygulama becerisi",
        "bot koruma yönetimi - bot saldırılarını tespit etmek ve önlemek için güvenlik izleme ve uyarı sistemlerini kullanma becerisi",
        "bot koruma yönetimi - bot ağlarına karşı koruma stratejilerini geliştirme yeteneği"
    ],
    "APT Management": [
        "apt yönetimi - apt saldırılarını tespit etmek ve önlemek için güvenlik izleme ve uyarı sistemlerini kullanma",
        "apt yönetimi - özellikle gelişmiş tehditler için kullanılan teknikleri ve taktikleri anlama",
        "apt yönetimi - apt tespiti ve müdahale becerisi",
        "apt yönetimi - gelişmiş kalıcı tehditlere karşı savunma stratejilerini belirleme yeteneğini anlama",
        "apt yönetimi - apt'lere karşı koruma sağlamak için güvenlik politikaları ve prosedürleri oluşturma ve uygulama",
        "apt yönetimi - apt'lere karşı koruma sağlamak için kullanılan güvenlik çözümlerini anlama becerisi"
    ],
    "Mobile Security": [
        "mobil cihaz güvenliği - mobil cihaz güvenliği tehditlerini tespit etme ve önleme becerisi",
        "mobil cihaz güvenliği - mobil cihazlar üzerinde güvenlik politikalarını uygulama yeteneği"
    ],
    "Identity & Access": [
        "kimlik ve erişim yönetimi bilgisi"
    ],
    "Compliance & Standards": [
        "denetim ve uyum bilgisi (iso 27001 vb.)",
        "itil, sox, cobit, btk, kvkk ve iso27001 standartları bilgisi",
        "iso 22301 bilgisi"
    ],
    "Certificates & Protocols": [
        "güvenlik sertifikası yönetimi - ssl/tls sertifikalarını yönetme ve güncelleme becerisi",
        "güvenlik sertifikası yönetimi - sertifika tabanlı güvenlik politikalarını uygulama yeteneği",
        "güvenlik protokolleri bilgisi"
    ],
    "Other Security Knowledge": [
        "güvenlik senaryo dizaynı bilgisi",
        "güvenlik platformları bilgisi",
        "güvenlik değerlendirmesi ve test bilgisi",
        "uygulama seviyesi güvenlik - uygulamaların güvenliğini değerlendirme ve iyileştirme yeteneği",
        "uygulama seviyesi güvenlik - uygulama tabanlı güvenlik açıklarını tespit etme ve düzeltme becerisi",
        "konfigürasyon yönetimi bilgisi",
        "zafiyet ve uyumluluk tarama sistemleri",
        "güvenlik donanım ve yazılımı bilgisi",
        "analiz ve raporlama bilgisi",
        "proje yönetim bilgisi",
        "teknik şartname hazırlama bilgisi",
        "genel mimari bilgisi",
        "altyapı ve topoloji mimarisi bilgisi",
        "altyapı ve platform bilgisi",
        "siber kriz yönetimi bilgisi",
        "container security bilgisi"
    ]
}

G = nx.DiGraph()

# Domain ve skill node ekleme + edge
for domain, skill_list in skills_by_domain.items():
    G.add_node(domain, type="domain")
    for skill in skill_list:
        G.add_node(skill, type="skill")
        G.add_edge(domain, skill, weight=1.0)

# Örnek Domain ↔ Domain ilişkileri (weight 0.4-0.7 arası)
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
all_skills = []
skill_to_domain = {}
for domain, skills in skills_by_domain.items():
    for skill in skills:
        all_skills.append(skill)
        skill_to_domain[skill] = domain

# 1. TF-IDF vectors
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(all_skills)

# 2. Cosine similarity matrix
sim_matrix = cosine_similarity(X)

# 3. Graph oluştur
G = nx.DiGraph()


# 4. Skill - Skill relationship (cosine similarity)
n = len(all_skills)
for i in range(n):
    for j in range(i+1, n):
        weight = sim_matrix[i, j]
        if weight > 0.2:  # çok düşük benzerlikleri atla
            G.add_edge(all_skills[i], all_skills[j], weight=weight)
            G.add_edge(all_skills[j], all_skills[i], weight=weight)



#burdayızzzzzzzzzzzzz!!!!!!!!!!!!!!!!!!!!!!!!!1
def propagate_theta(graph, student, skill, alpha=0.2):

    theta_i = student.get_theta(skill)

    for neighbor in graph.successors(skill):

        weight = graph[skill][neighbor]["weight"]

        theta_j = student.get_theta(neighbor)

        new_theta = theta_j + alpha * weight * (theta_i - theta_j)

        student.set_theta(neighbor, new_theta)
