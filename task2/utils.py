import os
from prettytable import PrettyTable


def create_folder():
    while True:
        path = input()

        absolute_path = os.path.abspath(path)
        current_directory = os.getcwd()

        if not absolute_path.startswith(current_directory):
            print("Можно создать папку только внутри текущей директории")
            continue

        try:
            os.makedirs(path, exist_ok=True)

            if os.access(path, os.W_OK):
                return path

            print("Недостаточно прав для записи")

        except OSError:
            print("Не удалось создать папку, попробуйте еще раз")


def print_results(results):
    results.sort(
        key=lambda item: item["number"]
    )

    table = PrettyTable()

    table.field_names = [
        "Ссылка",
        "Статус"
    ]

    table.align["Ссылка"] = "l"

    for item in results:
        table.add_row(
            [
                item["url"],
                item["status"]
            ]
        )

    print(table)