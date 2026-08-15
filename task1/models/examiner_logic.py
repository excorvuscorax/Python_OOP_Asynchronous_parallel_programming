import random
import time
from queue import Queue
from threading import Lock

from models.entities import Examiner, Question


def choose_question(examiner: Examiner, question: Question) -> list[str]:
    words = question.get_words()

    correct_answers = [random.choice(words)]

    while True:
        remaining_words = [
            word for word in words
            if word not in correct_answers
        ]

        if not remaining_words:
            break

        if random.random() < 1 / 3:
            correct_answers.append(random.choice(remaining_words))
        else:
            break

    return correct_answers


def evaluate(
    examiner: Examiner,
    student_answers: list[str],
    correct_answers: list[list[str]],
    questions: list[Question]
) -> bool:

    correct = 0
    wrong = 0

    for student_word, correct_list, question in zip(
            student_answers,
            correct_answers,
            questions
    ):

        if student_word in correct_list:
            correct += 1
            question.correct_count += 1
        else:
            wrong += 1

    return correct >= wrong


def run_exam(
    examiner: Examiner,
    student_queue: Queue,
    start_time: float,
    exam_questions: list[Question],
    lock: Lock,

):

    while True:

        student = None

        with lock:
            if not student_queue.empty():
                student = student_queue.get_nowait()
                examiner.current_student = student.name

        if student is None:
            break

        elapsed_time = time.time() - start_time

        if not examiner.on_lunch and elapsed_time > 30:
            examiner.on_lunch = True
            time.sleep(random.uniform(12, 18))

        exam_start_time = time.time()

        mood = random.random()

        name_length = len(examiner.name)
        exam_duration = random.uniform(name_length - 1, name_length + 1)

        if mood < 1 / 8:

            exam_passed = False

        elif mood < 3 / 8:

            exam_passed = True

        else:

            student_answers = []
            correct_answers = []

            for question in exam_questions:
                answer = student.choose_answer(question)[0]

                student_answers.append(answer)
                correct_answers.append(
                    choose_question(examiner, question)
                )

            exam_passed = evaluate(
                examiner,
                student_answers,
                correct_answers,
                exam_questions
            )

        time.sleep(exam_duration)

        exam_time = time.time() - exam_start_time

        student.exam_time = exam_time
        student.status = "Сдал" if exam_passed else "Провалил"

        examiner.work_time += exam_time
        examiner.students_handled += 1

        if not exam_passed:
            examiner.failed += 1

        examiner.current_student = "-"