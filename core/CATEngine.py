from session.student import StudentSession
from core.item_selector import select_next_item_3pl
from core.theta_estimator import update_theta_3pl
from core.score import compute_final_score

class CATEngine:
    def __init__(self, item_bank, max_questions=20):
        self.item_bank = item_bank
        self.max_questions = max_questions

        self.session = StudentSession()
        self.theta = 0.0
        self.used_item_ids = set()

        self.step = 0
        self.current_item = None

    def get_current_item(self):
        if self.current_item is None and self.step < self.max_questions:
            self.current_item = select_next_item_3pl(
                theta=self.theta,
                item_bank=self.item_bank,
                used_item_ids=self.used_item_ids,
                top_k=5
            )

            if self.current_item:
                self.used_item_ids.add(self.current_item.id)

        return self.current_item

    def submit_answer(self, response_binary: int):
        item = self.current_item

        self.session.register_answer(item, response_binary)

        responses = self.session.responses_by_subtopic[item.sub_topic]
        items = self.session.items_by_subtopic[item.sub_topic]

        self.theta = update_theta_3pl(
            responses=responses,
            items=items,
            theta_init=self.theta
        )

        self.step += 1
        self.current_item = None   # ⬅️ BİR SONRAKİ SORUYA GEÇ

        return self.theta

    def is_finished(self):
        return self.step >= self.max_questions

    def get_final_score(self):
        return compute_final_score(
            self.session.items_by_subtopic,
            self.session.responses_by_subtopic
        )
