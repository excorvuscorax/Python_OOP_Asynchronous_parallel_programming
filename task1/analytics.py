from models.entities import Examiner, Question, Student


def best_student(students: list[Student]) -> str:
    passed_students = [
        student for student in students
        if student.status == "Сдал"
    ]

    if not passed_students:
        return ""

    fastest_time = min(
        student.exam_time
        for student in passed_students
    )

    best_students = [
        student.name
        for student in passed_students
        if student.exam_time == fastest_time
    ]

    return ", ".join(best_students)


def student_expelled(students: list[Student]) -> str:
    failed_students = [
        student for student in students
        if student.status == "Провалил"
    ]

    if not failed_students:
        return ""

    fastest_failed_time = min(
        student.exam_time
        for student in failed_students
    )

    expelled_students = [
        student.name
        for student in failed_students
        if student.exam_time == fastest_failed_time
    ]

    return ", ".join(expelled_students)


def best_examiner_names(examiners: list[Examiner]) -> str:
    working_examiners = [
        examiner
        for examiner in examiners
        if examiner.students_handled > 0
    ]

    if not working_examiners:
        return ""

    minimum_failure_rate = min(
        examiner.failed / examiner.students_handled
        for examiner in working_examiners
    )

    best_examiners = [
        examiner.name
        for examiner in working_examiners
        if (
            examiner.failed / examiner.students_handled
            == minimum_failure_rate
        )
    ]

    return ", ".join(best_examiners)


def best_questions(questions: list[Question]) -> str:
    if not questions:
        return ""

    max_correct_answers = max(
        question.correct_count
        for question in questions
    )

    best_questions_list = [
        question.text
        for question in questions
        if question.correct_count == max_correct_answers
    ]

    return ", ".join(best_questions_list)


def exam_status(students: list[Student]) -> str:
    passed_count = sum(
        student.status == "Сдал"
        for student in students
    )

    total_students = len(students)

    if total_students == 0:
        return "Экзамен не удался"

    success_percent = passed_count / total_students * 100

    if success_percent > 85:
        return "Экзамен удался"

    return "Экзамен не удался"