from utils.loader import build_item_bank

item_bank = build_item_bank("data/erisim_guvenligi_sorulari.json")

from core.irt_model import p_3pl

theta = [0.0, 0.0, 0.0]   # öğrenci ortalama
item = item_bank[0]      # herhangi bir soru

p = p_3pl(theta, item)
print(p)
