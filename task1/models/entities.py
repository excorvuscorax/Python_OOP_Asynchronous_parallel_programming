import random


class Student:
    def __init__(self, name: str, gender: str, status: str = "Очередь"):
        self.name = name
        self.gender = gender
        self.status = status
        self.exam_time = 0.0

    def __repr__(self):
        return f"Student({self.name}, {self.gender})"

    def choose_answer(self, question):
        words = question.get_words()

        golden_ratio = 1.618
        weights = []
        remaining_probability = 1.0

        for _ in range(len(words)):
            current_weight = remaining_probability / golden_ratio
            weights.append(current_weight)
            remaining_probability -= current_weight

        if self.gender == "М":
            return random.choices(words, weights)

        return random.choices(words, list(reversed(weights)))


class Question:
    def __init__(self, text: str):
        self.text = text.strip()
        self.correct_count = 0

    def get_words(self):
        return self.text.split()

    def __repr__(self):
        return f"Question({self.text})"


class Examiner:
    def __init__(self, name: str, gender: str):
        self.name = name
        self.gender = gender
        self.students_handled = 0
        self.failed = 0
        self.work_time = 0.0
        self.current_student = "-"
        self.on_lunch = False

    def __repr__(self):
        return f"Examiner({self.name}, {self.gender})"