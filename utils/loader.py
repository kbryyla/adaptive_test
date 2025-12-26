import json
from core.item import Item


def build_item_bank(json_path: str) -> list[Item]:
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    item_bank = []
    item_id = 1

    difficulty_map = {
        "KOLAY": -2.0,
        "ORTA": 0.0,
        "ZOR": 2.0
    }

    for main_topic, sub_dict in data.items():
        for sub_topic, levels in sub_dict.items():
            for level_name, questions in levels.items():
                for q in questions:

                    item = Item(
                        id=item_id,
                        main_topic=main_topic,
                        sub_topic=sub_topic,
                        difficulty_level=level_name,
                        content=q["content"],
                        options=q["options"],
                        answer=q["answer"],
                        a=float(q["discrimination"]),
                        b=difficulty_map.get(level_name.upper(), 0.0),
                        c=float(q.get("guessing", 0.0))
                    )

                    item_bank.append(item)
                    item_id += 1

    return item_bank
