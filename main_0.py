from core.item_selector import select_next_item_max_FI, select_next_item_topic_based
#from core.theta_estimator import theta_update_general
from session.student import StudentState
from utils.loader import build_item_bank


item_bank = build_item_bank("data/erisim_guvenligi_sorulari.json")


max_questions = 10
used_item_ids = set()

student  = StudentState()
letters = ["A", "B", "C", "D", "E"]

while True:
    item = select_next_item_topic_based(student,item_bank)

    #MPI and DISTANCE FOR NEXT ITEM SELECTION CONTINUING...

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
    used_item_ids.add(item.id)
    current_theta = student.update_theta_general()

    correct_text = "DOĞRU" if response == 1 else "YANLIŞ"
    print(f"Cevabınız: {correct_text}")
    print("güncel theta",current_theta)

    #print(type[student.asked_items_by_topic.values()[0]])
    subtopic_thetas = student.update_subtopic_thetas()

    for topic, theta in subtopic_thetas.items():
        print(topic, theta)

    # Kaç soru soruldu?
    total_asked = student.total_items_asked()

    if total_asked >= max_questions:
        print("theta score: ", current_theta)
        break