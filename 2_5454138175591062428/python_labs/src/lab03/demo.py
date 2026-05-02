"""Демонстрация ЛР-3: наследование и иерархия книг."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.lab03.models import AudioBook, EBook, MediaLibrary, PrintedBook, sample_books


def print_header(title: str) -> None:
    print(f"\n{'=' * 12} {title} {'=' * 12}")


def print_library(title: str, library: MediaLibrary) -> None:
    print(f"\n{title} ({len(library)}):")
    for index, book in enumerate(library, start=1):
        print(f"{index}. {book}")


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    library = MediaLibrary(sample_books())

    print_header("Сценарий 1. Единая коллекция разных наследников")
    print_library("Медиатека", library)

    print_header("Сценарий 2. Полиморфный метод process()")
    for line in library.process_all():
        print("-", line)

    print_header("Сценарий 3. Методы дочерних классов")
    printed = library.get_only_printed()[0]
    ebook = library.get_only_ebooks()[0]
    audio = library.get_only_audio()[0]
    print(printed.reserve_shelf_place())
    print(ebook.generate_download_link())
    print(audio.listen_preview(7))

    print_header("Сценарий 4. Фильтрация по типам и isinstance()")
    print_library("Только электронные книги", library.get_only_ebooks())
    print_library("Только аудиокниги", library.get_only_audio())
    for book in library:
        print(
            f"{book.title}: PrintedBook={isinstance(book, PrintedBook)}, "
            f"EBook={isinstance(book, EBook)}, AudioBook={isinstance(book, AudioBook)}"
        )

    print_header("Сценарий 5. Общий метод access_description()")
    for book in library.sort_by_access_cost():
        print("-", book.access_description())


if __name__ == "__main__":
    main()
