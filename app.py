import streamlit as st

from utils.loader import build_item_bank
from session.student import StudentState
from core.item_selector import select_next_item_graph_aware
from core.theta_estimator import theta_update_single_item
from utils.topic_graph import propagate_theta, TOPIC_GRAPH
from core.stopping import should_stop
from core.score import (
    compute_final_score,
    compute_global_theta,
    compute_se_by_topic,
    compute_confidence,
    compute_fisher_weights
)

# ===========================
# CAT PARAMETRELERİ
# ===========================

TOP_K = 12
ALPHA = 0.8
BETA  = 0.3
GAMMA = 0.1

PROP_ALPHA = 0.4

SE_THRESHOLD = 0.3
MIN_ITEMS_PER_TOPIC = 2
MAX_ITEMS = 30

LETTERS = ["A", "B", "C", "D", "E"]

# ===========================
# SAYFA AYARI
# ===========================

st.set_page_config(page_title="Adaptive CAT", layout="centered")
st.title("Adaptif Sınav")

theta_box = st.empty()

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

# ===========================
# NEXT ITEM
# ===========================

def load_next_item():
    item = select_next_item_graph_aware(
        student=st.session_state.student,
        item_bank=st.session_state.ITEM_BANK,
        used_item_ids=st.session_state.used_item_ids,
        top_k=TOP_K,
        alpha=ALPHA,
        beta=BETA,
        gamma=GAMMA
    )
    st.session_state.current_item = item

# ===========================
# BAŞLAT
# ===========================

if st.session_state.current_item is None and not st.session_state.finished:
    load_next_item()

# ===========================
# SINAV BİTTİYSE
# ===========================

if st.session_state.finished:
    student = st.session_state.student

    # 1️⃣ SE hesapları
    se_by_topic = compute_se_by_topic(student)
    weights = compute_fisher_weights(se_by_topic)

    # 2️⃣ Fisher ağırlıklı global theta
    global_theta = compute_global_theta(
        student.theta_topic,
        weights
    )

    # 3️⃣ Final skor
    final_score = compute_final_score(global_theta)

    # 4️⃣ Güven
    se_global = max(se_by_topic.values())
    confidence = compute_confidence(se_global)

    st.success("Sınav Tamamlandı")

    st.metric("Final Skor", f"{final_score:.2f}")
    st.metric("Genel Theta", f"{global_theta:.3f}")
    st.metric("Ölçüm Güveni", f"%{confidence:.1f}")

    st.subheader("Topic Bazlı Sonuçlar")
    for topic, theta in student.theta_topic.items():
        st.write(
            f"**{topic}** → θ={theta:.3f} | SE={se_by_topic[topic]:.3f}"
        )

    st.stop()

# ===========================
# ANLIK GLOBAL THETA
# ===========================

student = st.session_state.student
se_by_topic = compute_se_by_topic(student)
weights = compute_fisher_weights(se_by_topic)

global_theta = compute_global_theta(
    student.theta_topic,
    weights
)

theta_box.markdown(
    f"### 📊 Genel Yetenek Düzeyi (θ): `{global_theta:.3f}`"
)

st.divider()

# ===========================
# AKTİF SORU
# ===========================

item = st.session_state.current_item

if item is None:
    st.warning("Kullanılabilir soru kalmadı.")
    st.stop()

question_no = len(st.session_state.used_item_ids) + 1

st.subheader(f"Soru {question_no}")
st.caption(f"Alt konu: {item.sub_topic}")
st.write(item.content)
st.write(item.answer)
choice = st.radio(
    "Cevabınızı seçin:",
    options=list(range(len(item.options))),
    format_func=lambda i: f"{i+1}. {item.options[i]}"
)

# ===========================
# CEVAPLA
# ===========================

if st.button("Cevabı Gönder"):
    correct_letter = item.answer.strip()[0]
    user_letter = LETTERS[choice]

    response = 1 if user_letter == correct_letter else 0
    st.write("**DOĞRU** ✅" if response else "**YANLIŞ** ❌")

    student = st.session_state.student

    # 1️⃣ cevabı kaydet
    student.register_response(item, response)
    st.session_state.used_item_ids.add(item.id)

    # 2️⃣ theta update (tek topic)
    old_theta = student.get_theta(item.sub_topic)
    total_items = student.total_items_asked()

    delta = theta_update_single_item(
        theta=old_theta,
        item=item,
        response=response,
        total_items=total_items
    )

    student.set_theta(item.sub_topic, old_theta + delta)

    # 3️⃣ topic graph propagation
    items_count_by_topic = {
        topic: len(items)
        for topic, items in student.asked_items_by_topic.items()
    }

    student.theta_topic = propagate_theta(
        theta_by_topic=student.theta_topic,
        topic_graph=TOPIC_GRAPH,
        alpha=PROP_ALPHA,
        min_items_by_topic=items_count_by_topic
    )

    # ===========================
    # ANLIK DURUM
    # ===========================

    st.divider()
    st.subheader("Anlık Durum")

    se_by_topic = compute_se_by_topic(student)
    weights = compute_fisher_weights(se_by_topic)

    for topic, theta in student.theta_topic.items():
        st.write(
            f"**{topic}** → θ={theta:.3f} | SE={se_by_topic[topic]:.3f}"
        )

    # ===========================
    # DURDURMA KRİTERİ
    # ===========================

    stop, reason = should_stop(
        student=student,
        asked_items_by_topic=student.asked_items_by_topic,
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
