from models.entities import Examiner, Question, Student


def read_examiners(path: str) -> list[Examiner]:
    with open(path, encoding="utf-8") as file:
        data = file.read().split()

    return [
        Examiner(data[index], data[index + 1])
        for index in range(0, len(data), 2)
    ]


def read_students(path: str) -> list[Student]:
    with open(path, encoding="utf-8") as file:
        data = file.read().split()

    return [
        Student(data[index], data[index + 1])
        for index in range(0, len(data), 2)
    ]


def read_questions(path: str) -> list[Question]:
    with open(path, encoding="utf-8") as file:
        return [
            Question(line)
            for line in file
            if line.strip()
        ]