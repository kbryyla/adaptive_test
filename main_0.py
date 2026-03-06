from core.irt_model import map_estimate
from core.item_selector import select_next_item_topic_based
from session.student import StudentState
from utils.loader import build_item_bank
from utils.topic_graph import propagate_theta, G, skill_id_to_text

item_bank = build_item_bank("data/erisim_guvenligi_sorulari.json")
"""topics = set()
for item in item_bank:
    topics.add(item.sub_topic)
print(topics)"""

max_questions = 10
used_item_ids = set()

student  = StudentState()
letters = ["A", "B", "C", "D", "E"]

while True:
    item = select_next_item_topic_based(student,item_bank)



    if item is None:
        print("item not found!")
        break


    print(f"\nSoru {item.id} ({item.sub_topic})")
    print(item.content)
    print(item.answer)
    print(student.total_items_asked())

    for idx, opt in enumerate(item.options, 1):
        print(f"{idx}. {opt}")

    while True:
        try:
            ans = int(input("Cevabınız (1/2/3/...): ").strip())
            if 1 <= ans <= len(item.options):
                break
        except ValueError:
            pass
        print("Geçersiz giriş!")
    # Kullanıcının girdiği numarayı harfe çevir
    if not item.answer or len(item.answer.strip()) == 0:
        print("Geçersiz answer formatı!")
        break
    correct_letter = item.answer.strip()[0]  # B) … → 'B'
    user_letter = letters[ans - 1]
    response = 1 if user_letter == correct_letter else 0
    # cevabı kaydet
    student.register_response(item, response)
    # 1. item.sub_topic → skill_id map
    subtopic_to_id = {v: k for k, v in skill_id_to_text.items()}

    # 2. Cevap sonrası theta güncelle
    for topic, responses in student.responses_by_topic.items():
        items = student.asked_items_by_topic[topic]
        for item, response in zip(items, responses):
            skill_id = subtopic_to_id.get(item.sub_topic)
            if skill_id:
                # burada compute_theta_for_item senin MLE veya MAP fonksiyonun
                student.set_theta(skill_id, map_estimate(item, response))
    used_item_ids.add(item.id)
    current_theta = student.update_theta_general()

    correct_text = "DOĞRU" if response == 1 else "YANLIŞ"
    print(f"Cevabınız: {correct_text}")
    print(f"güncel theta {current_theta:.3f}")

    #print(type[student.asked_items_by_topic.values()[0]])
    subtopic_thetas = student.update_subtopic_thetas()
    print(item.sub_topic in G.nodes)
    print(item.sub_topic)

    for skill_id in student.theta_topic:
        propagate_theta(G, student, skill_id)

    for topic, theta in subtopic_thetas.items():
        print(topic, f"{theta:.3f}")

    # Kaç soru soruldu?
    total_asked = student.total_items_asked()

    if total_asked >= max_questions:
        print(f"theta score: {current_theta:.3f}")
        break