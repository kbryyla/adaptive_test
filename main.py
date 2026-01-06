from utils.loader import build_item_bank
from session.student import StudentState
from core.item_selector import select_next_item_graph_aware
from core.theta_estimator import theta_update_single_item
from utils.topic_graph import propagate_theta, TOPIC_GRAPH
from core.stopping import should_stop, standard_error
from core.score import compute_final_score, compute_global_theta

#itembank
ITEM_BANK = build_item_bank("data/erisim_guvenligi_sorulari.json")

#öğrenci
student = StudentState()
used_item_ids = set()

#parametreler
TOP_K = 8
ALPHA = 0.6
BETA  = 0.3
GAMMA = 0.1
PROP_ALPHA = 0.1
SE_THRESHOLD = 0.3
MIN_ITEMS_PER_TOPIC = 2
MAX_ITEMS = 30


letters = ["A", "B", "C", "D", "E"]  # seçenek harfleri

while True:
    # next item seç
    item = select_next_item_graph_aware(
        student,
        ITEM_BANK,
        used_item_ids,
        top_k=TOP_K,
        alpha=ALPHA,
        beta=BETA,
        gamma=GAMMA
    )

    if item is None:
        print("Tüm sorular kullanıldı.")
        break

    # kullanıcı cevabı al (1/2/3/...)
    print(f"\nSoru {item.id} ({item.sub_topic})")
    print(item.content)
    print(item.answer)
    for idx, opt in enumerate(item.options, 1):
        print(f"{idx}. {opt}")

    while True:
        try:
            ans = int(input("Cevabınız (1/2/3/...): ").strip())
            if 1 <= ans <= len(item.options):
                break
        except:
            pass
        print("Geçersiz giriş!")

    # Kullanıcının girdiği numarayı harfe çevir
    correct_letter = item.answer.strip()[0]  # B) … → 'B'
    user_letter = letters[ans - 1]
    response = 1 if user_letter == correct_letter else 0

    correct_text = "DOĞRU" if response == 1 else "YANLIŞ"
    print(f"Cevabınız: {correct_text}")

    # cevabı kaydet
    student.register_response(item, response)
    used_item_ids.add(item.id)

    # Kaç soru soruldu?
    total_asked = student.total_items_asked()

    # İlk 5 soruda MAP açık
    use_map = total_asked < 5

    # topic bazlı theta update
    theta = student.get_theta(item.sub_topic)
    delta = theta_update_single_item(theta, item, response)

    print(
        f"[DEBUG] topic={item.sub_topic} "
        f"theta_before={theta:.3f} "
        f"delta={delta:.6f} "
        f"a={item.a} b={item.b} c={item.c} "
        f"response={response}"
    )
    student.set_theta(item.sub_topic, theta + delta)

    """"# propagation uygula
    student.theta_topic = propagate_theta(
        student.theta_topic,
        topic_graph=TOPIC_GRAPH,
        alpha=PROP_ALPHA
    )"""

    # propagation uygula (komşular etkilensin, ana topic korunur)
    propagated = propagate_theta(
        student.theta_topic,
        topic_graph=TOPIC_GRAPH,
        alpha=PROP_ALPHA
    )

    for topic, val in propagated.items():
        if topic != item.sub_topic:
            student.theta_topic[topic] = val

    #anlık durum
    print("\n--- Anlık Durum ---")
    for topic, theta in student.theta_topic.items():
        items = student.asked_items_by_topic.get(topic, [])
        se = standard_error(theta, items)
       # print(f"{topic}: θ={theta:.3f}, SE={se:.3f}")

    global_theta = compute_global_theta(student)
    print(f"Genel Theta (Fisher ağırlıklı): {global_theta:.3f}")
    print("--------------------\n")

    # durdurma kontrolü
    stop, reason = should_stop(
        student,
        student.asked_items_by_topic,
        se_threshold=SE_THRESHOLD,
        min_items_per_topic=MIN_ITEMS_PER_TOPIC,
        max_items=MAX_ITEMS
    )

    if stop:
        print(f"\nCAT durduruldu ({reason}).")
        break

#final score
final_score = compute_final_score(student.theta_topic, student.asked_items_by_topic)
global_theta = compute_global_theta(student)

print(f"\nFinal Skor: {final_score:.2f}")
print("\nTopic bazlı theta:")
for topic, theta in student.theta_topic.items():
    print(f"{topic}: {theta:.3f}")
print(f"\nGenel Theta (Fisher ağırlıklı): {global_theta:.3f}")
