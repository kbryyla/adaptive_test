from core.irt_model import fisher_information_3pl

# ITEM SELECTION FOR MIRT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! HERE!!!!!!!!!

def topic_selection(student, all_topics ):
    for topic in all_topics:
        if student.asked_count(topic) == 0:
            return topic

    return min(
        student.information_by_topic,
        key=student.information_by_topic.get
    )

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

def select_next_item_topic_based(student,item_bank):
    all_topics = list({item.sub_topic for item in item_bank})
    tried = set()

    while len(tried) < len(all_topics):

        topic = topic_selection(student,all_topics)
        theta = student.get_theta(topic)

        used_ids = {item.id for item in student.asked_items}
        topic_items = [item for item in item_bank
                       if item.sub_topic == topic and item.id not in used_ids]
        if topic_items:
            return select_next_item_max_FI(used_ids,topic_items,theta)
        else:
            tried.add(topic) # try another min info topic

    return None    #all topics finished