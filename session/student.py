from core.theta_estimator import theta_update_subtopic


class StudentState:
    def __init__(self):
        # Topic bazlı yetenek
        self.theta_topic = {}

        # Cevap ve madde geçmişi
        self.responses_by_topic = {}
        self.asked_items_by_topic = {}

        self.responses = []
        self.asked_items = []



    def register_response(self, item, response):
        topic = item.sub_topic

        if topic not in self.responses_by_topic:
            self.responses_by_topic[topic] = []
        if topic not in self.asked_items_by_topic:
            self.asked_items_by_topic[topic] = []

        #subtopic record
        self.responses_by_topic[topic].append(response)
        self.asked_items_by_topic[topic].append(item)

        #global record
        self.asked_items.append(item)
        self.responses.append(response)

    def update_subtopic_thetas(self):
        thetas = {}

        for topic in self.asked_items_by_topic:
            items = self.asked_items_by_topic[topic]
            responses = self.responses_by_topic[topic]

            if len(items) > 0:
                theta = theta_update_subtopic(items,responses)
                thetas[topic] = theta
        return thetas

    def asked_count(self, topic):
        return len(self.asked_items_by_topic.get(topic, []))

    def total_items_asked(self):
        return len(self.asked_items)


    def get_theta(self, topic):
        return self.theta_topic.get(topic, 0.0)

    def set_theta(self, topic, value):
        self.theta_topic[topic] = float(value)
