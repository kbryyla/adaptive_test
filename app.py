import streamlit as st
from utils.loader import build_item_bank
from session.student import StudentState
from core.item_selector import select_next_item_graph_aware
from core.theta_estimator import theta_update_single_item
from utils.topic_graph import propagate_theta, TOPIC_GRAPH
from core.stopping import should_stop, standard_error
from core.score import compute_final_score, compute_global_theta


# CAT PARAMETRELERİ

TOP_K = 8
ALPHA = 0.6
BETA  = 0.3
GAMMA = 0.1
PROP_ALPHA = 0.4
SE_THRESHOLD = 0.3
MIN_ITEMS_PER_TOPIC = 2
MAX_ITEMS = 50

LETTERS = ["A", "B", "C", "D", "E"]

# ===========================
# SAYFA AYARI
# ===========================
st.set_page_config(page_title="Adaptive CAT", layout="centered")
st.title("Adaptif Sınav")

# ===========================
# SESSION STATE INIT
# ===========================
if "initialized" not in st.session_state:
    st.session_state.ITEM_BANK = build_item_bank(
        "data/erisim_guvenligi_sorulari.json"
    )
    st.session_state.student = StudentState()
    st.session_state.used_item_ids = set()
    st.session_state.current_item = None
    st.session_state.finished = False
    st.session_state.initialized = True


# NEXT ITEM SEÇ

def load_next_item():
    item = select_next_item_graph_aware(
        st.session_state.student,
        st.session_state.ITEM_BANK,
        st.session_state.used_item_ids,
        top_k=TOP_K,
        alpha=ALPHA,
        beta=BETA,
        gamma=GAMMA
    )
    st.session_state.current_item = item


# BAŞLAT

if st.session_state.current_item is None and not st.session_state.finished:
    load_next_item()


# TEST BİTTİYSE

if st.session_state.finished:
    student = st.session_state.student

    final_score = compute_final_score(
        student.theta_topic,
        student.asked_items_by_topic
    )
    global_theta = compute_global_theta(student)

    st.success("Sınav Tamamlandı!")
    st.metric("Final Skor", f"{final_score:.2f}")
    st.metric("Genel Theta", f"{global_theta:.3f}")

    st.subheader("Topic Bazlı Theta")
    for topic, theta in student.theta_topic.items():
        st.write(f"**{topic}** → θ = {theta:.3f}")

    st.stop()


# AKTİF SORU

item = st.session_state.current_item

if item is None:
    st.warning("Kullanılacak soru kalmadı.")
    st.stop()

st.subheader(f"Soru {item.id}")
st.caption(f"Alt konu: {item.sub_topic}")
st.write(item.content)
st.write(item.answer)

choice = st.radio(
    "Cevabınızı seçin:",
    options=list(range(len(item.options))),
    format_func=lambda i: f"{i+1}. {item.options[i]}"
)


# CEVAPLA BUTONU

if st.button("Cevabı Gönder"):
    correct_letter = item.answer.strip()[0]
    user_letter = LETTERS[choice]

    response = 1 if user_letter == correct_letter else 0

    st.write(
        " **DOĞRU**" if response == 1 else " **YANLIŞ**"
    )

    # cevabı kaydet
    student = st.session_state.student
    student.register_response(item, response)
    st.session_state.used_item_ids.add(item.id)

    # theta update
    theta = student.get_theta(item.sub_topic)
    delta = theta_update_single_item(theta, item, response)
    student.set_theta(item.sub_topic, theta + delta)

    # propagation
    student.theta_topic = propagate_theta(
        student.theta_topic,
        topic_graph=TOPIC_GRAPH,
        alpha=PROP_ALPHA
    )


    # ANLIK RAPOR

    st.divider()
    st.subheader(" Anlık Durum")

    for topic, t in student.theta_topic.items():
        items = student.asked_items_by_topic.get(topic, [])
        se = standard_error(t, items)
        st.write(f"**{topic}** → θ={t:.3f}, SE={se:.3f}")

    global_theta = compute_global_theta(student)
    st.metric("Genel Theta", f"{global_theta:.3f}")


    # DURDURMA KRİTERİ

    stop, reason = should_stop(
        student,
        student.asked_items_by_topic,
        se_threshold=SE_THRESHOLD,
        min_items_per_topic=MIN_ITEMS_PER_TOPIC,
        max_items=MAX_ITEMS
    )

    if stop:
        st.session_state.finished = True
        st.success(f"CAT durduruldu: {reason}")
    else:
        load_next_item()

    st.rerun()
