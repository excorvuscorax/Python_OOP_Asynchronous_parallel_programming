import asyncio

from downloader import collect_links
from utils import create_folder, print_results


def main():

    results = []

    save_path = create_folder()

    results = asyncio.run(
        collect_links(
            save_path,
            results
        )
    )

    print_results(results)


if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:
        print("Программа остановлена пользователем")