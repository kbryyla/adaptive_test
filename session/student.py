from collections import defaultdict

class StudentState:
    def __init__(self):
        self.theta_topic = defaultdict(float)
        self.responses_by_topic = defaultdict(list)
        self.asked_items_by_topic = defaultdict(list)
        self.se = {}


    @property
    def theta_global(self):
        if not self.theta_topic:
            return 0.0
        return sum(self.theta_topic.values()) / len(self.theta_topic)

    def register_response(self, item, response):
        topic = item.sub_topic
        self.responses_by_topic[topic].append(response)
        self.asked_items_by_topic[topic].append(item)

    def asked_count(self, topic):
        return len(self.asked_items_by_topic.get(topic, []))

    def total_items_asked(self):
        return sum(len(v) for v in self.asked_items_by_topic.values())

    def get_theta(self, topic):
        return self.theta_topic.get(topic, 0.0)

    def set_theta(self, topic, value):
        self.theta_topic[topic] = value

    def get_se(self, topic):
        return self.se.get(topic, float("inf"))
