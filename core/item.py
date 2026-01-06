class Item:
    def __init__(
        self,
        id: int,
        main_topic: str,
        sub_topic: str,
        difficulty_level: str,
        content: str,
        options: list,
        answer: str,
        a: float,
        b: float,
        c: float = 0.2  # sabit c parametresi
    ):
        self.id = id
        self.main_topic = main_topic
        self.sub_topic = sub_topic.lower().strip()
        self.difficulty_level = difficulty_level
        self.content = content
        self.options = options
        self.answer = answer
        self.a = a
        self.b = b
        self.c = c
