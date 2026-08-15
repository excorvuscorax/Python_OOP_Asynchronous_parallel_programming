import random
import threading
import time
from queue import Queue

from analytics import (
    best_examiner_names,
    best_questions,
    best_student,
    exam_status,
    student_expelled,
)
from loader import (
    read_examiners,
    read_questions,
    read_students,
)
from models.examiner_logic import run_exam
from visuals import (
    render_final_report,
    update_display,
)


def main():
    examiners = read_examiners("examiners.txt")
    students = read_students("students.txt")
    questions = read_questions("questions.txt")

    start_time = time.time()

    exam_finished_event = threading.Event()
    queue_lock = threading.Lock()

    exam_questions = random.sample(
        questions,
        3
    )

    student_queue = Queue()

    for student in students:
        student_queue.put(student)

    original_order = list(students)

    display_thread = threading.Thread(
        target=update_display,
        args=(
            students,
            examiners,
            student_queue,
            start_time,
            original_order,
            exam_finished_event,
        ),
    )

    display_thread.start()

    examiner_threads = []

    for examiner in examiners:
        thread = threading.Thread(
            target=run_exam,
            args=(
                examiner,
                student_queue,
                start_time,
                exam_questions,
                queue_lock,
            ),
        )

        thread.start()
        examiner_threads.append(thread)

    for thread in examiner_threads:
        thread.join()

    exam_finished_event.set()

    display_thread.join()

    render_final_report(
        students=students,
        examiners=examiners,
        questions=questions,
        start_time=start_time,
        best_student=best_student,
        best_examiner_names=best_examiner_names,
        student_expelled=student_expelled,
        best_questions=best_questions,
        exam_status=exam_status,
    )


if __name__ == "__main__":
    main()