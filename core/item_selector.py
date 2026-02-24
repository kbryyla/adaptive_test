from core.irt_model import fisher_information_3pl


def select_next_item_max_FI(
        used_item_ids,
        item_bank,
        theta):

    unused_items = [
        item for item in item_bank
        if item.id not in used_item_ids]

    infos = []
    for item in unused_items:
        info = fisher_information_3pl(theta, item.a, item.b, item.c)
        infos.append((info, item))

    return max(infos, key=lambda x:x[0])[1]

