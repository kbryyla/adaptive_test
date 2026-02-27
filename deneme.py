from utils.loader import build_item_bank
from core.irt_model import irt_3pl

from core.score import compute_final_score

item_bank = build_item_bank("data/erisim_guvenligi_sorulari.json")
unique_sub_topics = set()

for item in item_bank:
    unique_sub_topics.add(item.sub_topic)
for sub_topic in unique_sub_topics:
    print(sub_topic)
