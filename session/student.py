from core.irt_model import mle, fisher_information_3pl


class StudentState:
    def __init__(self):
        # Topic bazlı yetenek
        self.theta_topic = {}
        self.theta_general = 0.0      #LAZY PROPERTY!!!!!!!! BURDASINNN.

        # Cevap ve madde geçmişi
        self.responses_by_topic = {}
        self.asked_items_by_topic = {}

        self.responses = []
        self.asked_items = []


        #topic based total FI
        self.information_by_topic = {}



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


        if topic not in self.information_by_topic:
            self.information_by_topic[topic] = 0.0
        info = fisher_information_3pl(self.get_theta(topic),item.a,item.b,item.c)
        self.information_by_topic[topic] += info


    def update_theta_general(self):
        if len(self.asked_items) == 0:
            return 0.0
        else:
            self.theta_general = mle(self.asked_items, self.responses)

        return self.theta_general

    def update_subtopic_thetas(self):

        for topic in self.asked_items_by_topic:
            items = self.asked_items_by_topic[topic]
            responses = self.responses_by_topic[topic]

            if len(items) == 0:
                self.theta_topic[topic] = 0.0
            else:
                self.theta_topic[topic] = mle(items,responses)

        return self.theta_topic

    def asked_count(self, topic):
        return len(self.asked_items_by_topic.get(topic, []))

    def total_items_asked(self):
        return len(self.asked_items)


    def get_theta(self, topic):
        return self.theta_topic.get(topic, 0.0)

    def set_theta(self, topic, value):
        self.theta_topic[topic] = float(value)
