import os
import time

from prettytable import PrettyTable


def clear_console():
    os.system("cls" if os.name == "nt" else "clear")


def get_sorted_students(
    students,
    student_queue,
    original_order
):
    queue_students = list(student_queue.queue)

    active_students = [
        student
        for student in original_order
        if (
            student.status == "Очередь"
            and student not in queue_students
        )
    ]

    passed_students = [
        student
        for student in students
        if student.status == "Сдал"
    ]

    failed_students = [
        student
        for student in students
        if student.status == "Провалил"
    ]

    return (
        queue_students
        + active_students
        + passed_students
        + failed_students
    )


def create_students_table(students):
    table = PrettyTable()

    table.field_names = [
        "Студент",
        "Статус"
    ]

    for student in students:
        table.add_row(
            [
                student.name,
                student.status
            ]
        )

    return table


def create_examiners_table(examiners):
    table = PrettyTable()

    table.field_names = [
        "Экзаменатор",
        "Текущий студент",
        "Всего студентов",
        "Завалил",
        "Время работы"
    ]

    for examiner in examiners:
        table.add_row(
            [
                examiner.name,
                examiner.current_student,
                examiner.students_handled,
                examiner.failed,
                f"{examiner.work_time:.2f}"
            ]
        )

    return table


def draw_state(
    students,
    examiners,
    student_queue,
    start_time,
    original_order
):
    clear_console()

    sorted_students = get_sorted_students(
        students,
        student_queue,
        original_order
    )

    print(create_students_table(sorted_students))

    print(create_examiners_table(examiners))

    remaining_students = sum(
        student.status == "Очередь"
        for student in students
    )

    print(
        f"Осталось в очереди: "
        f"{remaining_students} из {len(students)}"
    )

    print(
        "Время с момента начала экзамена: "
        f"{time.time() - start_time:.2f}"
    )

    return sorted_students


def update_display(
    students,
    examiners,
    student_queue,
    start_time,
    original_order,
    exam_finished_event
):
    while not exam_finished_event.is_set():

        draw_state(
            students,
            examiners,
            student_queue,
            start_time,
            original_order
        )

        time.sleep(0.2)


def create_final_examiners_table(examiners):
    table = PrettyTable()

    table.field_names = [
        "Экзаменатор",
        "Всего студентов",
        "Завалил",
        "Время работы"
    ]

    for examiner in examiners:
        table.add_row(
            [
                examiner.name,
                examiner.students_handled,
                examiner.failed,
                f"{examiner.work_time:.2f}"
            ]
        )

    return table


def render_final_report(
    students,
    examiners,
    questions,
    start_time,
    best_student,
    best_examiner_names,
    student_expelled,
    best_questions,
    exam_status
):
    clear_console()

    passed_students = [
        student
        for student in students
        if student.status == "Сдал"
    ]

    failed_students = [
        student
        for student in students
        if student.status == "Провалил"
    ]

    final_students = (
        passed_students
        + failed_students
    )

    print(create_students_table(final_students))

    print(create_final_examiners_table(examiners))

    total_time = time.time() - start_time

    print(
        "Время с момента начала экзамена "
        f"и до момента его завершения: {total_time:.2f}"
    )

    print(
        f"Имена лучших студентов: "
        f"{best_student(students)}"
    )

    print(
        f"Имена лучших экзаменаторов: "
        f"{best_examiner_names(examiners)}"
    )

    print(
        f"Имена студентов, которых после экзамена "
        f"отчислят: {student_expelled(students)}"
    )

    print(
        f"Лучшие вопросы: {best_questions(questions)}"
    )

    print(
        f"Вывод: {exam_status(students)}"
    )